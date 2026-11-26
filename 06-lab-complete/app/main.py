"""Production mock AI agent."""
import json
import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, StringConstraints
from redis import RedisError
from typing import Annotated

from app.auth import verify_api_key
from app.config import settings
from app.cost_guard import check_budget, record_cost, token_cost
from app.rate_limiter import check_rate_limit
from app.redis_client import r, redis_healthy
from utils.mock_llm import MOCK_RESPONSES, ask as llm_ask


logger = logging.getLogger("day14.agent")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False

MAX_OUTPUT_TOKENS = max(len(answer.split()) for answers in MOCK_RESPONSES.values() for answer in answers)


def log_event(event: str, **fields):
    logger.info(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "event": event, **fields}))


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        r.close()
        log_event("shutdown")


app = FastAPI(title="Production AI Agent", lifespan=lifespan)


class AskRequest(BaseModel):
    question: Annotated[str, StringConstraints(strip_whitespace=True)] = Field(min_length=1, max_length=2000)


@app.middleware("http")
async def log_request(request: Request, call_next):
    started = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        route = request.scope.get("route")
        log_event("request", route=route.path if route else "unmatched",
                  status=status, ms=round((time.perf_counter() - started) * 1000, 2))


@app.exception_handler(RedisError)
async def redis_unavailable(request: Request, exc: RedisError):
    return JSONResponse(status_code=503, content={"detail": "Redis unavailable"})


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}


@app.get("/ready")
def ready():
    if redis_healthy():
        return {"status": "ready"}
    return JSONResponse(status_code=503, content={"status": "not_ready", "redis": "unavailable"})


@app.post("/ask")
def ask(body: AskRequest, key: str = Depends(verify_api_key)):
    check_rate_limit(key)
    input_tokens = len(body.question.split())
    reserved = token_cost(input_tokens, MAX_OUTPUT_TOKENS)
    budget_key = check_budget(reserved)
    actual = 0
    try:
        answer = llm_ask(body.question)
        actual = token_cost(input_tokens, len(answer.split()))
    finally:
        record_cost(budget_key, reserved, actual)
    return {"question": body.question, "answer": answer}

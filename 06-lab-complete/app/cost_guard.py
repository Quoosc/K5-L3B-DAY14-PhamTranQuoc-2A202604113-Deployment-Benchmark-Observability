"""Reserve monthly budget atomically, then settle the measured mock usage."""
from datetime import datetime, timezone

from fastapi import HTTPException

from app.config import settings
from app.redis_client import r


# At 0.00015/0.0006 USD per 1,000 tokens, each token costs 150/600 nanodollars.
INPUT_PRICE = 150
OUTPUT_PRICE = 600
NANODOLLARS_PER_USD = 1_000_000_000

RESERVE = r.register_script("""
local cost = tonumber(ARGV[1])
local spend = tonumber(redis.call('GET', KEYS[1]) or '0')
if spend + cost > tonumber(ARGV[2]) then
    return 0
end
redis.call('INCRBY', KEYS[1], cost)
redis.call('EXPIREAT', KEYS[1], ARGV[3])
return 1
""")

SETTLE = r.register_script("""
if redis.call('EXISTS', KEYS[1]) == 1 then
    redis.call('INCRBY', KEYS[1], ARGV[1])
end
""")


def token_cost(input_tokens: int, output_tokens: int) -> int:
    return input_tokens * INPUT_PRICE + output_tokens * OUTPUT_PRICE


def check_budget(max_cost: int) -> str:
    now = datetime.now(timezone.utc)
    next_year = now.year + (now.month == 12)
    reset = datetime(next_year, now.month % 12 + 1, 1, tzinfo=timezone.utc)
    key = f"day14:budget:{now:%Y-%m}"
    limit = int(settings.monthly_budget_usd * NANODOLLARS_PER_USD)
    if not RESERVE(keys=[key], args=[max_cost, limit, int(reset.timestamp())]):
        raise HTTPException(status_code=402, detail="Monthly LLM budget exceeded")
    return key


def record_cost(key: str, reserved: int, actual: int) -> None:
    if actual != reserved:
        SETTLE(keys=[key], args=[actual - reserved])

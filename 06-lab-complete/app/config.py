"""Configuration supplied by the process environment."""
import os
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Settings:
    port: int = int(os.getenv("PORT", "8000"))
    environment: str = os.getenv("ENVIRONMENT", "development")
    agent_api_key: str = os.getenv("AGENT_API_KEY", "")
    redis_url: str = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))
    monthly_budget_usd: Decimal = Decimal(os.getenv("MONTHLY_BUDGET_USD", "10"))

    def __post_init__(self):
        if not 1 <= self.port <= 65535 or self.rate_limit_per_minute < 1:
            raise ValueError("PORT and RATE_LIMIT_PER_MINUTE must be in range")
        if not self.monthly_budget_usd.is_finite() or not 0 <= self.monthly_budget_usd <= 1_000_000:
            raise ValueError("MONTHLY_BUDGET_USD must be between 0 and 1000000")


settings = Settings()

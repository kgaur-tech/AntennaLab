from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "AntennaLab")
    environment: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("APP_DEBUG", "false").lower() == "true"
    api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
    max_concurrent_jobs: int = int(os.getenv("SIM_WORKER_CONCURRENCY", "2"))
    job_timeout_seconds: int = int(os.getenv("MAX_JOB_TIMEOUT_SECONDS", "600"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def get_settings_dict() -> dict[str, Any]:
    settings = get_settings()
    return settings.__dict__.copy()

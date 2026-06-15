

import time
import os
import redis
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


# Redis connection (shared with existing services)
def _get_redis_client():
    return redis.Redis(
        host=os.environ.get("REDIS_HOST", "redis"),
        port=int(os.environ.get("REDIS_PORT", 6379)),
        password=os.environ.get("REDIS_PASSWORD") or None,
        decode_responses=True
    )


def is_rate_limited(
    redis_client: redis.Redis,
    identifier: str,
    limit: int = 100,
    window_seconds: int = 60
) -> tuple[bool, int, int]:
   
    now = time.time()
    window_start = now - window_seconds
    key = f"ratelimit:{identifier}"

    pipe = redis_client.pipeline()

    pipe.zremrangebyscore(key, 0, window_start)

    pipe.zadd(key, {str(now): now})

    pipe.zcard(key)

    pipe.expire(key, window_seconds)

    results = pipe.execute()
    current_count = results[2]  

    if current_count > limit:
        oldest = redis_client.zrange(key, 0, 0, withscores=True)
        if oldest:
            oldest_timestamp = oldest[0][1]
            retry_after = int(oldest_timestamp + window_seconds - now) + 1
        else:
            retry_after = window_seconds

        return True, current_count, retry_after

    return False, current_count, 0


class RateLimiter:
   
    def __init__(self, limit: int = 100, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self._redis = None

    def _get_client(self):
        if self._redis is None:
            self._redis = _get_redis_client()
        return self._redis

    async def __call__(self, request: Request):
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        else:
            ip = request.client.host if request.client else "unknown"

        try:
            redis_client = self._get_client()
            limited, count, retry_after = is_rate_limited(
                redis_client,
                identifier=ip,
                limit=self.limit,
                window_seconds=self.window_seconds
            )
        except Exception:
            return

        request.state.rate_limit_headers = {
            "X-RateLimit-Limit": str(self.limit),
            "X-RateLimit-Remaining": str(max(0, self.limit - count)),
            "X-RateLimit-Window": str(self.window_seconds),
        }

        if limited:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Too Many Requests",
                    "detail": f"Limit: {self.limit} requests/{self.window_seconds}s. Retry after {retry_after}s.",
                    "retry_after": retry_after,
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.limit),
                    "X-RateLimit-Remaining": "0",
                }
            )
strict_limiter = RateLimiter(limit=10, window_seconds=60)

standard_limiter = RateLimiter(limit=100, window_seconds=60)

relaxed_limiter = RateLimiter(limit=300, window_seconds=60)

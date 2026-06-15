import os
import json
import httpx
from shared.redis_client import redis_client
from dotenv import load_dotenv
from shared.logger import get_logger
load_dotenv()

logger = get_logger("feed-service")

FOLLOW_SERVICE_URL = os.environ.get(
    "FOLLOW_SERVICE_URL")

POST_SERVICE_URL = os.environ.get(
    "POST_SERVICE_URL")

CACHE_TTL = int(os.environ.get("CACHE_TTL", 300))


async def generate_feed(user_id: int, limit: int = 20, offset: int = 0):
    cache_key = f"feed:user:{user_id}:limit:{limit}:offset:{offset}"

    cached_feed = redis_client.get(cache_key)
    if cached_feed:
        return json.loads(cached_feed)

    try:
       

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{FOLLOW_SERVICE_URL}/follow/{user_id}/following",
                timeout=3
            )
    
        response.raise_for_status()
        data = response.json()
        following_ids = data.get("following_ids", [])
    except Exception as e:
       
            logger.warning(
                "Failed to fetch following list",
                extra={
                    "error": str(e),
                    "user_id": user_id
        }
    )
            return []

    if not following_ids:
        return []

    
    try:
        user_ids_str = ",".join(map(str, following_ids))
        async with httpx.AsyncClient() as client:
            post_response = await client.get(
                f"{POST_SERVICE_URL}/posts/bulk",
                params={
                    "user_ids": user_ids_str,
                    "limit": limit + offset
                },
                headers={
                    "X-Internal-Token": os.getenv("INTERNAL_SERVICE_TOKEN")
                },
                timeout=3
                )
        post_response.raise_for_status()
        feed = post_response.json()
    except Exception as e:
       
        logger.warning(
            "Failed to fetch posts",
            extra={
                "error": str(e),
                "user_id": user_id
            }
        )
        return []

    feed.sort(
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )

    feed = feed[offset: offset + limit]

    redis_client.setex(
        cache_key,
        CACHE_TTL,
        json.dumps(feed)
    )

    return feed
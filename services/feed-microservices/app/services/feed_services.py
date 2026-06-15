import os
import json
import requests
from app.cache.redis_client import redis_client
from dotenv import load_dotenv
load_dotenv()

FOLLOW_SERVICE_URL = os.environ.get(
    "FOLLOW_SERVICE_URL",
    "http://follower-microservice:8002"
)

POST_SERVICE_URL = os.environ.get(
    "POST_SERVICE_URL",
    "http://post-microservices:8003"
)

CACHE_TTL = int(os.environ.get("CACHE_TTL", 300))


def generate_feed(user_id: int, limit: int = 20, offset: int = 0):
    cache_key = f"feed:user:{user_id}:limit:{limit}:offset:{offset}"

    # ✅ check cache first
    cached_feed = redis_client.get(cache_key)
    if cached_feed:
        return json.loads(cached_feed)

    try:
        response = requests.get(
            f"{FOLLOW_SERVICE_URL}/follow/{user_id}/following",
            timeout=3
        )
        response.raise_for_status()
        data = response.json()
        following_ids = data.get("following_ids", [])
    except Exception as e:
        print(f"Failed to fetch following list: {e}")
        return []

    if not following_ids:
        return []

    
    try:
        user_ids_str = ",".join(map(str, following_ids))
        post_response = requests.get(
            f"{POST_SERVICE_URL}/posts/bulk",
            params={
                "user_ids": user_ids_str,
                "limit": limit + offset  # fetch enough to paginate
            },
            timeout=3
        )
        post_response.raise_for_status()
        feed = post_response.json()
    except Exception as e:
        print(f"Failed to fetch posts: {e}")
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
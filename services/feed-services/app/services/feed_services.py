import requests
import json
import redis

USER_SERVICE_URL = "http://localhost:8000"
POST_SERVICE_URL = "http://localhost:8001"

# Redis client
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

CACHE_TTL = 300  # 5 minutes


def generate_feed(user_id: int):

    cache_key = f"feed:user:{user_id}"

    # 1. CHECK CACHE FIRST
    cached_feed = redis_client.get(cache_key)

    if cached_feed:
        print("🔥 CACHE HIT")
        return json.loads(cached_feed)

    print("❌ CACHE MISS")

    # 2. FETCH FOLLOWING IDS
    response = requests.get(
        f"{USER_SERVICE_URL}/users/following-ids/{user_id}"
    )

    following_ids = response.json()

    feed = []

    # 3. FETCH POSTS FROM POST SERVICE
    for followed_user in following_ids:

        post_response = requests.get(
            f"{POST_SERVICE_URL}/posts/user/{followed_user}"
        )

        posts = post_response.json()
        feed.extend(posts)

    print("FOLLOWING IDS:", following_ids)
    print("FEED DATA:", feed)

    # 4. SORT FEED (latest first)
    feed.sort(
        key=lambda x: x["id"],
        reverse=True
    )

    # 5. STORE IN REDIS CACHE
    redis_client.setex(
        cache_key,
        CACHE_TTL,
        json.dumps(feed)
    )

    return feed
import requests
import json
import redis

import os
USER_SERVICE_URL = os.environ.get("USER_SERVICE_URL", "http://user-service:8000")
POST_SERVICE_URL = os.environ.get("POST_SERVICE_URL", "http://post-service:8001")



redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=int(os.environ.get("REDIS_PORT", 6379))
)

CACHE_TTL = 300  


def generate_feed(user_id: int):

    cache_key = f"feed:user:{user_id}"

    cached_feed = redis_client.get(cache_key)

    if cached_feed:
        return json.loads(cached_feed)


    response = requests.get(
        f"{USER_SERVICE_URL}/users/following-ids/{user_id}"
    )

    following_ids = response.json()

    feed = []

    for followed_user in following_ids:

        post_response = requests.get(
            f"{POST_SERVICE_URL}/posts/user/{followed_user}"
        )

        posts = post_response.json()
        feed.extend(posts)


    feed.sort(
        key=lambda x: x["id"],
        reverse=True
    )

    redis_client.setex(
        cache_key,
        CACHE_TTL,
        json.dumps(feed)
    )

    return feed
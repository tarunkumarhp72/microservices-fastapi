# import os
# import requests
# from app.models.post_model import Post
# from app.redis_client import redis_client

# FOLLOW_SERVICE_URL = os.environ.get(
#     "FOLLOW_SERVICE_URL",
#     "http://localhost:8002"
# )


# def _invalidate_follower_feeds(user_id: int):
#     """
#     Fetches follower IDs from follow-service
#     and deletes their cached feeds from Redis.
#     Wrapped in try/except so it never blocks the main response.
#     """
#     try:
#         response = requests.get(
#             f"{FOLLOW_SERVICE_URL}/follow/{user_id}/followers",
#             timeout=2  
#         )
#         data = response.json()
#         follower_ids = data.get("follower_ids", [])

#         for follower_id in follower_ids:
#             redis_client.delete(f"feed:user:{follower_id}")

#     except Exception as e:
#         print(f"Cache invalidation failed: {e}")


# def create_post(post_data, user_id: int, db):
#     post = Post(
#         content=post_data.content,
#         user_id=user_id
#     )
#     db.add(post)
#     db.commit()
#     db.refresh(post)

#     _invalidate_follower_feeds(user_id)

#     return post


# def get_post(post_id: int, db):
#     return db.query(Post).filter(Post.id == post_id).first()


# def get_user_posts(user_id: int, db):
#     return db.query(Post).filter(
#         Post.user_id == user_id
#     ).order_by(Post.created_at.desc()).all()


# def get_posts_by_user_ids(user_ids: list[int], limit: int, db):
#     """
#     Bulk fetch posts for multiple users in ONE query.
#     This fixes the N+1 problem in feed-service.
#     """
#     return db.query(Post).filter(
#         Post.user_id.in_(user_ids)
#     ).order_by(
#         Post.created_at.desc()
#     ).limit(limit).all()


# def delete_post(post_id: int, user_id: int, db):
#     post = db.query(Post).filter(Post.id == post_id).first()

#     if not post:
#         return None

#     if post.user_id != user_id:
#         return False

#     db.delete(post)
#     db.commit()

#     _invalidate_follower_feeds(user_id)

#     return True


import os
import requests
from app.models.post_model import Post
from app.redis_client import redis_client

FOLLOW_SERVICE_URL = os.environ.get(
    "FOLLOW_SERVICE_URL",
    "http://localhost:8002"
)


def _invalidate_follower_feeds(user_id: int):
    """
    Fetches follower IDs from follow-service
    and deletes their cached feeds from Redis.
    Wrapped in try/except so it never blocks the main response.
    """
    try:
        response = requests.get(
            f"{FOLLOW_SERVICE_URL}/follow/{user_id}/followers",
            timeout=2
        )

        # Status check — agar 200 nahi aaya toh json() mat karo
        if response.status_code != 200:
            print(f"Cache invalidation skipped: follower service returned "
                  f"{response.status_code} — body: {response.text[:200]}")
            return

        data = response.json()
        follower_ids = data.get("follower_ids", [])

        if follower_ids:
            for follower_id in follower_ids:
                redis_client.delete(f"feed:user:{follower_id}")
            print(f"Cache invalidated for {len(follower_ids)} followers of user {user_id}")
        else:
            print(f"No followers found for user {user_id} — nothing to invalidate")

    except Exception as e:
        print(f"Cache invalidation failed: {e}")


def create_post(post_data, user_id: int, db):
    post = Post(
        content=post_data.content,
        user_id=user_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    _invalidate_follower_feeds(user_id)

    return post


def get_post(post_id: int, db):
    return db.query(Post).filter(Post.id == post_id).first()


def get_user_posts(user_id: int, db):
    return db.query(Post).filter(
        Post.user_id == user_id
    ).order_by(Post.created_at.desc()).all()


def get_posts_by_user_ids(user_ids: list[int], limit: int, db):
    """
    Bulk fetch posts for multiple users in ONE query.
    This fixes the N+1 problem in feed-service.
    """
    return db.query(Post).filter(
        Post.user_id.in_(user_ids)
    ).order_by(
        Post.created_at.desc()
    ).limit(limit).all()


def delete_post(post_id: int, user_id: int, db):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return None

    if post.user_id != user_id:
        return False

    db.delete(post)
    db.commit()

    _invalidate_follower_feeds(user_id)

    return True
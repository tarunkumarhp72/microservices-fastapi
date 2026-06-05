from app.models.post_model import Post

from app.redis_client import redis_client
import requests
import os


USER_SERVICE_URL = os.environ.get("USER_SERVICE_URL", "http://user-service:8000")
POST_SERVICE_URL = os.environ.get("POST_SERVICE_URL", "http://post-service:8001")



def create_post(post_data, user_id, db):

    post = Post(
        content=post_data.content,
        user_id=user_id
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    try:
        response = requests.get(
            f"{USER_SERVICE_URL}/users/followers-ids/{user_id}"
        )

        followers = response.json()

        for follower_id in followers:
            cache_key = f"feed:user:{follower_id}"
            redis_client.delete(cache_key)

    except Exception as e:
        print("Cache invalidation failed:", str(e))
    return post

def get_post(post_id, db):

    return db.query(Post).filter(
        Post.id == post_id
    ).first()

def get_user_posts(
    user_id,
    db
):

    return db.query(Post).filter(
        Post.user_id == user_id
    ).all()

def delete_post(post_id, user_id, db):

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return None

    if post.user_id != user_id:
        return False

    db.delete(post)
    db.commit()

    try:
        response = requests.get(
            f"{USER_SERVICE_URL}/users/followers-ids/{user_id}"
        )

        followers = response.json()

        for follower_id in followers:
            cache_key = f"feed:user:{follower_id}"
            redis_client.delete(cache_key)

    except Exception as e:
        print("Cache invalidation failed:", str(e))

    return True

import os
from dotenv import load_dotenv
load_dotenv()

ROUTE_MAP = {
    "/users":  os.environ.get("USER_SERVICE_URL",   "http://user-microservice:8001"),
    "/posts":  os.environ.get("POST_SERVICE_URL",   "http://post-microservice:8003"),
    "/follow": os.environ.get("FOLLOW_SERVICE_URL", "http://follower-microservice:8002"),
    "/feed":   os.environ.get("FEED_SERVICE_URL",   "http://feed-microservice:8004"),
}
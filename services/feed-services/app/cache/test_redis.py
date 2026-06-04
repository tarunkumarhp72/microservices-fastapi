# You should be in: D:\Amandeep\self practise projects\social_media_feed_system\services\feed-services

# Create the test file with this content:

import redis
import json

try:
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )
    
    print("🔌 Testing Redis connection...")
    response = redis_client.ping()
    print(f"✅ PING response: {response}")
    
    print("\n💾 Testing SET (save data)...")
    redis_client.set("test_key", "Hello Redis!")
    print("✅ Saved test_key")
    
    print("\n📖 Testing GET (retrieve data)...")
    value = redis_client.get("test_key")
    print(f"✅ Retrieved: {value}")
    
    print("\n" + "="*50)
    print("✅ ALL TESTS PASSED! Redis is working!")
    print("="*50)

except Exception as e:
    print(f"❌ ERROR: {e}")

# Now run it

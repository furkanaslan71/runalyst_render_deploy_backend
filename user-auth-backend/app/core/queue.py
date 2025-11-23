import os
import redis
from rq import Queue
from dotenv import load_dotenv

load_dotenv()

# Get Redis URL from environment variables
REDIS_URL = os.environ.get("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL must be set in environment variables.")

# Establish a connection to Redis
redis_conn = redis.from_url(REDIS_URL)

# Create a queue instance that uses this connection
# The name 'default' is the queue it will listen to.
queue = Queue("default", connection=redis_conn)
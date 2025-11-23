# worker.py (Corrected and Improved Version)

import os
import redis
from rq import Worker, Queue

# This list defines which queues this worker will listen to.
# 'default' is a standard choice.
listen = ['default']

# Get the Redis connection URL from the environment variables
# provided by Render.
redis_url = os.environ.get('REDIS_URL')
if not redis_url:
    raise ValueError("REDIS_URL environment variable not set.")

# Create the Redis connection object.
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    # Create a list of Queue objects to listen to.
    # We pass the connection object directly to the Queue constructor.
    queues = [Queue(name, connection=conn) for name in listen]

    # Create the Worker. We pass it the list of queues.
    # The worker will use the connection from the queues it is given.
    worker = Worker(queues, connection=conn)

    # Start the worker process. It will now listen for jobs on the 'default' queue.
    print(f"Worker starting... Listening on queues: {', '.join(listen)}")
    worker.work()
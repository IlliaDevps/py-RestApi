import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL" ,  "redis://localhost:5379")
QUEUES= ["emails", "default"] rq worker -c settings
     
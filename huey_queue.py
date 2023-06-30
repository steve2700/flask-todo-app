from huey import RedisHuey
from app import huey

huey_consumer = huey.consumer()
huey_consumer.run()


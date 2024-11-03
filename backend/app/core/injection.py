from typing import TypeVar, Type, Callable
from aioredis import Redis
from injector import Injector, singleton
from app.core.redis import RedisManager

from .config import settings

injector = Injector()
T = TypeVar("T")

def on(dependency_class: Type[T]) -> callable[[], T]:
    """Bridge between FastApi injection and 'injector' DI frameworkk."""
    return lambda: injector.get(dependency_class)

class Cache(Redis):
    """Cache injection token with code completion for Redis instance."""
    pass

class PubSubStore(Redis):
    """PubSubStore injection token with code completion for Redis instance."""
    pass

async def configure():
    """Create dependency injection graph and init services."""
    cache, pubsub = RedisManager(settings.REDIS_URL), RedisManager(settings.REDIS_URL)
    await cache.start()
    await pubsub.start()
    injector.binder.bind(Cache, to=cache.redis, scope=singleton)
    injector.binder.bind(PubSubStore, to=cache.redis, scope=singleton)
    injector.binder.bind(AsyncGraphDatabase, to=AsyncGraphDatabase(settings.Neo4J_URI, settings.Neo4J_User, settings.Neo4J_password), scope=singleton)
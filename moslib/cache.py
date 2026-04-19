import os
from functools import lru_cache
from joblib import Memory
from cachetools import cached, TTLCache

# Localización estanca dentro de mos2
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_PATH, "var/cache")

# 1. RAM Cache
memo = lru_cache(maxsize=128)

# 2. Disk Cache (FHS Compliant)
memory = Memory(CACHE_DIR, verbose=0)
disk = memory.cache

# 3. TTL Cache
def ttl(seconds=300, max_entries=100):
    return cached(cache=TTLCache(maxsize=max_entries, ttl=seconds))

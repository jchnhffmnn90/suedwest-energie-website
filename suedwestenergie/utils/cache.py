"""Caching utilities for production performance optimization"""

import time
import pickle
import hashlib
from typing import Any, Optional
from functools import wraps


class SimpleCache:
    """Simple in-memory cache for storing processed data"""
    
    def __init__(self):
        self._cache = {}
        self.default_ttl = 3600  # 1 hour default TTL
    
    def _make_key(self, *args, **kwargs) -> str:
        """Create a unique key from function arguments"""
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                return value
            else:
                del self._cache[key]  # Clean up expired entry
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL"""
        if ttl is None:
            ttl = self.default_ttl
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """Delete a key from cache"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()


# Global cache instance
cache = SimpleCache()


def cached(ttl: Optional[int] = None):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = cache._make_key(func.__name__, *args, **kwargs)
            result = cache.get(key)
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator
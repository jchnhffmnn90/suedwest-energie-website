"""Konfiguration und Einstellungen für die Website"""

from .env_config import EnvironmentConfig


class Config(EnvironmentConfig):
    """Zentrale Konfigurationsklasse - erweitert EnvironmentConfig"""

    # Social Media (optional) - not typically in environment variables
    LINKEDIN = ""
    XING = ""

    # Performance settings
    CACHE_TTL = 3600  # 1 hour cache for static content
    ENABLE_COMPRESSION = True
    ENABLE_HTTPS_REDIRECT = True
    ENABLE_HSTS = True

    @classmethod
    def get_db_url(cls) -> str:
        """Get database URL based on environment"""
        if cls.is_production():
            # In production, always use the environment variable
            if not cls.DB_URL or cls.DB_URL == "sqlite:///reflex.db":
                raise ValueError("DB_URL environment variable must be set in production")
        return cls.DB_URL
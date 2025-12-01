"""Environment configuration for production deployment"""

import os
from typing import Optional


class EnvironmentConfig:
    """Configuration class that loads settings from environment variables"""
    
    # Database configuration
    DB_URL: str = os.getenv("DB_URL", "sqlite:///reflex.db")
    
    # Application settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # External services
    EMAIL_HOST: Optional[str] = os.getenv("EMAIL_HOST")
    EMAIL_PORT: Optional[int] = int(os.getenv("EMAIL_PORT", "587")) if os.getenv("EMAIL_PORT") else None
    EMAIL_HOST_USER: Optional[str] = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD: Optional[str] = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS: bool = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
    
    # Google Analytics
    GOOGLE_ANALYTICS_ID: str = os.getenv("GOOGLE_ANALYTICS_ID", "")
    
    # Contact information
    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Südwest-Energie")
    EMAIL: str = os.getenv("CONTACT_EMAIL", "kontakt@suedwest-energie.de")
    PHONE: str = os.getenv("CONTACT_PHONE", "+49 711 12345678")
    ADDRESS: str = os.getenv("CONTACT_ADDRESS", "Stuttgart, Deutschland")
    
    # Branding - Natural, sustainable color palette
    PRIMARY_COLOR: str = os.getenv("PRIMARY_COLOR", "#2D5016")  # Forest green (deep, natural)
    SECONDARY_COLOR: str = os.getenv("SECONDARY_COLOR", "#7CB342")  # Fresh leaf green (vibrant, organic)
    ACCENT_COLOR: str = os.getenv("ACCENT_COLOR", "#8BC34A")  # Light eco green (bright, hopeful)
    TEXT_DARK: str = os.getenv("TEXT_DARK", "#1B3409")  # Deep forest (for headings)
    TEXT_LIGHT: str = os.getenv("TEXT_LIGHT", "#5D7A4A")  # Sage green (for body text)
    BG_LIGHT: str = os.getenv("BG_LIGHT", "#F1F8E9")  # Soft cream/light green (nature-light)
    BG_DARK: str = os.getenv("BG_DARK", "#E8F5E0")  # Pale green (subtle earth)
    CARD_BG: str = os.getenv("CARD_BG", "#FFFFFF")  # Clean white (purity)
    SKY_BLUE: str = os.getenv("SKY_BLUE", "#81C784")  # Soft sky/water
    EARTH_BROWN: str = os.getenv("EARTH_BROWN", "#A1887F")  # Natural earth tone
    
    # SEO
    SITE_TITLE: str = os.getenv("SITE_TITLE", "Südwest-Energie - Energievermittlung für Unternehmen")
    SITE_DESCRIPTION: str = os.getenv("SITE_DESCRIPTION",
        "Professionelle Energievermittlung für Unternehmen. Wir senken Ihre Strom- und Gaskosten um durchschnittlich 20-30% - transparent, unabhängig und kostenfrei.")
    
    # Tarifrechner (Tariff Calculator) Embed
    TARIFRECHNER_ENABLED: bool = os.getenv("TARIFRECHNER_ENABLED", "True").lower() == "true"
    TARIFRECHNER_TYPE: str = os.getenv("TARIFRECHNER_TYPE", "iframe")  # "iframe" or "script"
    TARIFRECHNER_URL: str = os.getenv("TARIFRECHNER_URL", "")  # URL for iframe embed
    TARIFRECHNER_SCRIPT: str = os.getenv("TARIFRECHNER_SCRIPT", "")  # Script code for script embed
    TARIFRECHNER_HEIGHT: str = os.getenv("TARIFRECHNER_HEIGHT", "600px")  # Height of embed
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.ENVIRONMENT.lower() in ['prod', 'production']
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment"""
        return cls.ENVIRONMENT.lower() in ['dev', 'development', 'local']
    
    @classmethod
    def is_test(cls) -> bool:
        """Check if running in test environment"""
        return cls.ENVIRONMENT.lower() in ['test', 'testing']
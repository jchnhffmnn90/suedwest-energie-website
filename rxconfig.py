import reflex as rx
import os

# Determine if we're in production mode
IS_PRODUCTION = os.environ.get("REFLEX_ENV") == "prod"

config = rx.Config(
    app_name="suedwestenergie",
    # Use environment variable for database URL in production
    db_url=os.getenv("DB_URL", "sqlite:///reflex.db") if IS_PRODUCTION else "sqlite:///reflex.db",
    # Compression settings
    compress_response=True,
    # Other production settings
    admin_dash=rx.AdminDash(
        # Optional: Add admin dash if needed
    ),
)
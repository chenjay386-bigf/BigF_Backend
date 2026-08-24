import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "super-secret-key",
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt-secret-key",
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
    )

    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError(
            "DATABASE_URL is not set. "
            "Check your backend/.env file."
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JSON_SORT_KEYS = False

    PROPAGATE_EXCEPTIONS = True

    # ============================================================
    # COOKIE SECURITY CONFIGURATIONS (LOCAL HTTP SETUP)
    # ============================================================
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # Keep False for local HTTP development; set to True later in production with HTTPS
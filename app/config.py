import os


class Settings:
    PROJECT_NAME: str = "Excel Project Backend"
    VERSION: str = "1.0.0"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./excel_project.db",
    )

    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "change-this-to-a-secure-random-secret-key-in-production",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours


settings = Settings()

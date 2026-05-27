import os


class Settings:
    PROJECT_NAME: str = "Excel Project Backend"
    VERSION: str = "1.0.0"

    # MongoDB
    MONGODB_URL: str = os.getenv(
        "MONGODB_URL",
        "mongodb://localhost:27017",
    )
    MONGODB_DB_NAME: str = os.getenv(
        "MONGODB_DB_NAME",
        "excel_project",
    )

    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "change-this-to-a-secure-random-secret-key-in-production",
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours


settings = Settings()

from pydantic_settings import BaseSettings
import os
class Settings(BaseSettings):
    # MySQL connection settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "ta589ha707CAN*"
    DB_NAME: str = "iuc_etkinlik"
    
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

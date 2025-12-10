"""
Shared configuration settings for VetrAI Platform
"""
from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # General
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    secret_key: str = "change-me-in-production"
    api_version: str = "v1"
    
    # Database
    database_url: str = "postgresql://vetrai:vetrai_password@localhost:5432/vetrai_db"
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_echo: bool = False
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_password: Optional[str] = None
    redis_db: int = 0
    redis_max_connections: int = 50
    
    # MinIO/S3
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "vetrai_minio_access"
    minio_secret_key: str = "vetrai_minio_secret"
    minio_secure: bool = False
    minio_bucket_name: str = "vetrai-storage"
    
    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Password
    password_min_length: int = 8
    password_reset_token_expire_hours: int = 24
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000"
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from_email: str = "noreply@vetrai.io"
    smtp_from_name: str = "VetrAI Platform"
    smtp_use_tls: bool = True
    smtp_use_ssl: bool = False
    
    # Stripe
    stripe_secret_key: Optional[str] = None
    stripe_publishable_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    stripe_api_version: str = "2023-10-16"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    rate_limit_per_day: int = 10000
    
    # API Keys
    api_key_prefix: str = "vetrai_"
    api_key_length: int = 32
    api_key_expiry_days: int = 365
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    celery_task_track_started: bool = True
    celery_task_time_limit: int = 3600
    celery_worker_concurrency: int = 4
    
    # Feature Flags
    feature_stripe_enabled: bool = True
    feature_razorpay_enabled: bool = False
    feature_sms_enabled: bool = False
    feature_analytics_enabled: bool = True
    feature_audit_logging_enabled: bool = True
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment.lower() == "development"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

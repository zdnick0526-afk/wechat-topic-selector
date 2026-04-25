"""
配置管理模块
"""
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""

    # 应用基本配置
    APP_NAME: str = "WeChat Topic Selector"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # API服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # CORS配置
    FRONTEND_URL: str = "http://localhost:5173"
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:8000",
    ]

    # 数据库配置
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/wechat_topics"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis缓存配置
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600

    # NLP配置
    MAX_KEYWORDS: int = 10
    MIN_KEYWORD_LENGTH: int = 2

    # 安全配置
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_SECRET_KEY: str = "your-jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # 功能开关
    FEATURE_AI_RECOMMENDATIONS: bool = True
    FEATURE_COMPETITOR_ANALYSIS: bool = True
    FEATURE_SENTIMENT_ANALYSIS: bool = True
    FEATURE_TREND_PREDICTION: bool = True

    class Config:
        """Pydantic配置"""
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# 导出配置实例
settings = get_settings()

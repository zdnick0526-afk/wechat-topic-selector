"""
主应用入口
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.models import TopicCreate

# 配置日志
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# 生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("Application starting...")
    yield
    logger.info("Application shutting down...")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="WeChat Official Account Topic Selection Tool",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "version": settings.APP_VERSION}


# 根路由
@app.get("/")
async def root():
    """根路由"""
    return {
        "message": "Welcome to WeChat Topic Selector API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


# 推荐选题
@app.get("/api/v1/topics/recommendations")
async def get_recommendations(
    user_id: str,
    limit: int = 10,
    category: str = None
):
    """获取推荐选题"""
    logger.info(f"Getting recommendations for user {user_id}")
    return {
        "user_id": user_id,
        "topics": [],
        "count": 0,
        "timestamp": "2024-01-01T00:00:00Z"
    }


# 创建选题
@app.post("/api/v1/topics")
async def create_topic(topic: TopicCreate):
    """创建选题"""
    logger.info(f"Creating topic: {topic.title}")
    return {
        "id": 1,
        "title": topic.title,
        "category": topic.category,
        "status": "new",
        "created_at": "2024-01-01T00:00:00Z"
    }


# 热点话题
@app.get("/api/v1/trending")
async def get_trending(source: str = None, limit: int = 20):
    """获取热点数据"""
    logger.info(f"Getting trending topics from {source or 'all sources'}")
    return {
        "source": source,
        "topics": [],
        "count": 0,
        "timestamp": "2024-01-01T00:00:00Z"
    }


# 竞品分析
@app.get("/api/v1/competitors/analysis")
async def analyze_competitors(accounts: list[str]):
    """竞品分析"""
    logger.info(f"Analyzing competitors: {accounts}")
    return {
        "competitors": accounts,
        "analysis": {},
        "timestamp": "2024-01-01T00:00:00Z"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS,
        reload=settings.DEBUG
    )

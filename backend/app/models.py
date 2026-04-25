"""
数据模型定义
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class TopicStatus(str, Enum):
    """选题状态"""
    NEW = "new"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ContentType(str, Enum):
    """内容类型"""
    ARTICLE = "article"
    INFOGRAPHIC = "infographic"
    VIDEO = "video"
    INTERACTIVE = "interactive"
    OTHER = "other"


class SentimentType(str, Enum):
    """情感类型"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class SourceType(str, Enum):
    """数据源类型"""
    WEIBO = "weibo"
    ZHIHU = "zhihu"
    DOUYIN = "douyin"
    XIAOHONGSHU = "xiaohongshu"
    BAIDU = "baidu"
    NEWS = "news"


class TopicBase(BaseModel):
    """选题基础模型"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: str
    keywords: List[str] = Field(default_factory=list)


class TopicCreate(TopicBase):
    """创建选题"""
    user_id: str


class Topic(TopicBase):
    """选题模型"""
    id: str
    user_id: str
    status: TopicStatus = TopicStatus.NEW
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrendingTopic(BaseModel):
    """热点话题"""
    id: str
    title: str
    description: Optional[str]
    category: str
    heat_score: float
    trend_direction: str
    mention_count: int
    growth_rate: float
    first_seen_at: datetime
    peak_at: datetime
    is_trending: bool
    source: SourceType
    source_url: Optional[str]
    sentiment: SentimentType
    sentiment_score: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class KeywordAnalysis(BaseModel):
    """关键词分析"""
    keyword: str
    frequency: int
    heat_score: float
    trend: str
    category: str
    sentiment: SentimentType
    related_keywords: List[str]


class EntityInfo(BaseModel):
    """实体信息"""
    text: str
    entity_type: str
    mention_count: int
    importance_score: float

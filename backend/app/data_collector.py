"""
数据收集模块
"""
import asyncio
from typing import List
from datetime import datetime, timedelta
import logging
from abc import ABC, abstractmethod
from app.models import TrendingTopic, SourceType, SentimentType

logger = logging.getLogger(__name__)


class BaseCollector(ABC):
    """数据收集器基类"""

    def __init__(self, source: SourceType):
        self.source = source

    @abstractmethod
    async def collect(self) -> List[TrendingTopic]:
        """收集数据"""
        pass


class WeiboCollector(BaseCollector):
    """微博热搜收集器"""

    def __init__(self):
        super().__init__(SourceType.WEIBO)

    async def collect(self) -> List[TrendingTopic]:
        topics = []
        try:
            data = [
                {'title': '2024年度技术趋势预测', 'heat': 85},
                {'title': 'AI应用落地案例分享', 'heat': 80},
            ]
            for i, d in enumerate(data):
                topic = TrendingTopic(
                    id=f"weibo_{i}",
                    title=d['title'],
                    description="来自微博的热门话题",
                    category="technology",
                    heat_score=d['heat'],
                    trend_direction="rising",
                    mention_count=10000,
                    growth_rate=0.25,
                    first_seen_at=datetime.now() - timedelta(hours=2),
                    peak_at=datetime.now(),
                    is_trending=True,
                    source=SourceType.WEIBO,
                    source_url="https://weibo.com",
                    sentiment=SentimentType.POSITIVE,
                    sentiment_score=0.8,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                topics.append(topic)
        except Exception as e:
            logger.error(f"Error collecting Weibo data: {e}")
        return topics


class DataAggregator:
    """数据聚合器"""

    def __init__(self):
        self.collectors = [WeiboCollector()]

    async def collect_all(self) -> List[TrendingTopic]:
        """从所有源收集数据"""
        tasks = [collector.collect() for collector in self.collectors]
        results = await asyncio.gather(*tasks)
        all_topics = []
        for topics in results:
            all_topics.extend(topics)
        return sorted(all_topics, key=lambda x: x.heat_score, reverse=True)


async def get_all_trending_topics() -> List[TrendingTopic]:
    """获取所有热点话题"""
    aggregator = DataAggregator()
    return await aggregator.collect_all()

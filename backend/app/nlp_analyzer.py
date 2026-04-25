"""
NLP分析模块
"""
import jieba
from typing import List, Dict, Tuple
from collections import Counter
from app.models import SentimentType, KeywordAnalysis, EntityInfo


class NLPAnalyzer:
    """NLP分析器"""

    def __init__(self):
        """初始化"""
        self.stopwords = self._load_stopwords()

    def _load_stopwords(self) -> set:
        """加载停用词"""
        return {
            '的', '了', '和', '是', '在', '不', '有', '一', '这', '为'
        }

    def extract_keywords(self, text: str, top_k: int = 10) -> List[KeywordAnalysis]:
        """提取关键词"""
        words = jieba.cut(text)
        filtered_words = [
            word for word in words
            if len(word) >= 2 and word not in self.stopwords
        ]

        word_freq = Counter(filtered_words)
        total_words = len(filtered_words)

        keywords = []
        for word, freq in word_freq.most_common(top_k):
            tf = freq / total_words
            heat_score = min(tf * 100, 100)

            keyword_analysis = KeywordAnalysis(
                keyword=word,
                frequency=freq,
                heat_score=heat_score,
                trend="stable",
                category="general",
                sentiment=SentimentType.NEUTRAL,
                related_keywords=[]
            )
            keywords.append(keyword_analysis)

        return keywords

    def sentiment_analysis(self, text: str) -> Tuple[SentimentType, float]:
        """情感分析"""
        positive_words = {'好', '优秀', '棒', '成功'}
        negative_words = {'差', '烂', '失败', '讨厌'}

        words = jieba.cut(text)
        word_list = list(words)

        pos_count = sum(1 for w in word_list if w in positive_words)
        neg_count = sum(1 for w in word_list if w in negative_words)

        if pos_count > neg_count:
            return SentimentType.POSITIVE, 0.8
        elif neg_count > pos_count:
            return SentimentType.NEGATIVE, 0.8
        else:
            return SentimentType.NEUTRAL, 0.5

    def text_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        words1 = set(jieba.cut(text1))
        words2 = set(jieba.cut(text2))

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def automatic_categorization(self, text: str) -> str:
        """自动分类"""
        categories = {
            '技术': ['技术', '代码', '编程', 'AI'],
            '商业': ['创业', '融资', '商业'],
            '生活': ['生活', '健康', '美食'],
            '娱乐': ['明星', '电影', '游戏'],
        }

        max_score = 0
        best_category = '其他'

        for category, keywords in categories.items():
            score = sum(text.count(kw) for kw in keywords)
            if score > max_score:
                max_score = score
                best_category = category

        return best_category

    def analyze_title_quality(self, title: str) -> Dict:
        """分析标题质量"""
        length = len(title)
        scores = {
            'length_score': min(length / 25 * 100, 100),
            'number_bonus': 10 if any(c.isdigit() for c in title) else 0,
        }
        return {
            'total_score': min(sum(scores.values()) / len(scores), 100),
            'details': scores
        }

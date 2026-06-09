"""
SearchAgent - Arxiv文献检索Agent
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from tools.arxiv import ArxivClient, ArxivSearchError
from config.settings import ARXIV_MAX_RESULTS


class Paper(BaseModel):
    """论文数据结构"""
    title: str = Field(description="论文标题")
    authors: List[str] = Field(description="作者列表")
    abstract: str = Field(description="论文摘要")
    published: str = Field(description="发表时间")
    arxiv_url: str = Field(description="Arxiv链接")


class SearchResult(BaseModel):
    """检索结果"""
    topic: str = Field(description="搜索主题")
    total: int = Field(description="返回论文数量")
    papers: List[Paper] = Field(description="论文列表")
    cached: bool = Field(default=False, description="是否来自缓存")


class SearchAgent:
    """
    文献检索Agent

    输入: 研究主题
    输出: 论文列表(含title/authors/abstract/published/arxiv_url)
    """

    def __init__(self, max_results: int = ARXIV_MAX_RESULTS):
        self.arxiv_client = ArxivClient(max_results=max_results)
        self.max_results = max_results

    def search(self, topic: str, max_results: Optional[int] = None) -> SearchResult:
        """
        执行文献检索

        Args:
            topic: 研究主题，如 "LLM Agent Memory"
            max_results: 最大返回数量，默认20

        Returns:
            SearchResult: 检索结果

        Raises:
            SearchAgentError: 检索失败时抛出
        """
        if not topic or not topic.strip():
            raise SearchAgentError("搜索主题不能为空")

        topic = topic.strip()

        try:
            papers_data = self.arxiv_client.search(
                topic=topic,
                max_results=max_results or self.max_results
            )

            papers = []
            for p in papers_data:
                papers.append(Paper(**p))

            return SearchResult(
                topic=topic,
                total=len(papers),
                papers=papers,
                cached=False
            )

        except ArxivSearchError as e:
            raise SearchAgentError(f"检索失败: {str(e)}")
        except Exception as e:
            raise SearchAgentError(f"未知错误: {str(e)}")


class SearchAgentError(Exception):
    """SearchAgent异常"""
    pass


# 便捷函数
def search_papers(topic: str, max_results: int = 20) -> SearchResult:
    """
    快速检索函数

    Args:
        topic: 研究主题
        max_results: 最大返回数量

    Returns:
        SearchResult
    """
    agent = SearchAgent(max_results=max_results)
    return agent.search(topic)
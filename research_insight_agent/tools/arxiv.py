"""
Arxiv API 封装
使用 arxiv-hacker 库进行文献检索
"""
import arxiv_hacker
from typing import List, Optional
import cacheutil


class ArxivClient:
    """Arxiv API 客户端"""

    def __init__(self, max_results: int = 20):
        self.max_results = max_results
        self._cache = cacheutil.Cache()

    def search(self, topic: str, max_results: Optional[int] = None) -> List[dict]:
        """
        搜索Arxiv论文

        Args:
            topic: 研究主题
            max_results: 最大返回数量，默认20

        Returns:
            论文列表
        """
        cache_key = f"arxiv_{topic}_{max_results or self.max_results}"

        # 检查缓存
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            results = arxiv_hacker.search_arxiv(
                keyword=topic,
                max_results=max_results or self.max_results,
            )

            papers = []
            for result in results:
                #提取作者列表
                authors = []
                if hasattr(result, "authors") and result.authors:
                    for author in result.authors:
                        if hasattr(author, "name"):
                            authors.append(author.name)
                        elif isinstance(author, str):
                            authors.append(author)

                paper = {
                    "title": result.title if hasattr(result, "title") else "",
                    "authors": authors,
                    "abstract": result.summary if hasattr(result, "summary") else "",
                    "published": result.published if hasattr(result, "published") else "",
                    "arxiv_url": result.entry_id if hasattr(result, "entry_id") else "",
                }
                papers.append(paper)

            # 写入缓存 (24小时)
            self._cache.set(cache_key, papers, expire=86400)
            return papers

        except Exception as e:
            raise ArxivSearchError(f"Arxiv搜索失败: {str(e)}")


class ArxivSearchError(Exception):
    """Arxiv搜索异常"""
    pass
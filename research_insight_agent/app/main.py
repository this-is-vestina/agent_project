"""
Streamlit主界面 - SearchAgent演示
"""
import streamlit as st
from datetime import datetime

from agents.search_agent import SearchAgent, SearchAgentError, SearchResult


st.set_page_config(
    page_title="Research Insight Agent",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Research Insight Agent")
st.markdown("**P0阶段：SearchAgent - Arxiv文献检索**")

# 搜索表单
with st.form("search_form"):
    topic = st.text_input(
        "研究主题",
        placeholder="例如: LLM Agent Memory",
        help="输入您想调研的研究主题"
    )
    max_results = st.slider("返回数量", 5, 50, 20)
    submitted = st.form_submit_button("🔍 开始检索", type="primary")

# 显示结果
if submitted and topic:
    with st.spinner(f"正在检索「{topic}」..."):
        try:
            agent = SearchAgent(max_results=max_results)
            result = agent.search(topic)

            # 统计信息
            col1, col2, col3 = st.columns(3)
            col1.metric("检索主题", result.topic)
            col2.metric("论文数量", result.total)
            col3.metric("检索时间", datetime.now().strftime("%H:%M:%S"))

            st.divider()

            # 论文列表
            st.subheader(f"📚 找到 {result.total} 篇论文")

            for i, paper in enumerate(result.papers, 1):
                with st.expander(f"**{i}. {paper.title}**", expanded=i <= 3):
                    col1, col2 = st.columns([3, 1])
                    col1.markdown(f"**作者:** {', '.join(paper.authors[:5])}{'...' if len(paper.authors) > 5 else ''}")
                    col1.markdown(f"**发表:** {paper.published[:10] if paper.published else 'N/A'}")
                    col1.markdown(f"**链接:** [{paper.arxiv_url}]({paper.arxiv_url})")
                    col2.caption("点击上方链接查看原文")

                    st.markdown("**摘要:**")
                    st.text_area(
                        label="abstract",
                        value=paper.abstract[:800] + "..." if len(paper.abstract) > 800 else paper.abstract,
                        height=150,
                        label_visibility="collapsed",
                        disabled=True
                    )

        except SearchAgentError as e:
            st.error(f"❌ 检索失败: {str(e)}")
        except Exception as e:
            st.error(f"❌ 未知错误: {str(e)}")

elif submitted and not topic:
   st.warning("⚠️ 请输入研究主题")
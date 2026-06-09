# Research Insight Agent

科研领域智能分析Agent，基于LangGraph构建。

## 功能

-📚 Arxiv文献检索
- 📝论文智能分析
- 🔍 主题聚类
- 📈 热点趋势分析
- 💡 研究空白发现
- 📅 研究时间线
- 🛤️ 学习路线生成
- 📋 文献综述自动生成

## 快速开始

```bash
pip install -r requirements.txt
cp .env.example .env  # 配置API密钥
streamlit run app/main.py
```

## 项目结构

```
research_insight_agent/
├── app/
│   └── main.py          # Streamlit主界面
├── agents/
│   ├── search_agent.py  # Arxiv检索
│   ├── analysis_agent.py # 论文分析
│   ├── cluster_agent.py  # 主题聚类
│   ├── trend_agent.py    # 热点分析
│   ├── gap_agent.py      # 研究空白
│   ├── timeline_agent.py # 时间线
│   ├── roadmap_agent.py  # 学习路线
│   ├── survey_agent.py # 文献综述
│   └── workflow.py       # LangGraph工作流
├── tools/
│   ├── arxiv.py         # Arxiv API
│   └── llm.py            # LLM调用
├── config/
│   ├── settings.py       # 配置
│   └── prompts.py        # Prompt模板
└── data/                 # 数据存储
```
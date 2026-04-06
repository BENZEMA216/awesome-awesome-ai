from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
TEMPLATES_DIR = ROOT_DIR / "templates"
README_PATH = ROOT_DIR / "README.md"

CATEGORIES = {
    "prompts": "Prompt Collections",
    "cli-tools": "CLI Tools",
    "mcp-servers": "MCP Servers",
    "agents": "Agent Frameworks & Lists",
    "models": "Model Lists & Comparisons",
    "datasets": "Dataset Collections",
    "papers": "Paper Lists",
    "coding": "AI Coding Tools",
    "media": "Image / Audio / Video Generation",
    "productivity": "Productivity Tools",
    "other": "Other",
}

CATEGORIES_ZH = {
    "prompts": "Prompt 集合",
    "cli-tools": "CLI 工具",
    "mcp-servers": "MCP 服务器",
    "agents": "Agent 框架与列表",
    "models": "模型列表与对比",
    "datasets": "数据集合集",
    "papers": "论文列表",
    "coding": "AI 编程工具",
    "media": "图片 / 音频 / 视频生成",
    "productivity": "效率工具",
    "other": "其他",
}

MIN_STARS = 100
MAX_INACTIVE_DAYS = 180
MIN_README_LENGTH = 1000
MIN_LINK_DENSITY = 10

SEARCH_QUERIES = [
    "awesome ai",
    "awesome llm",
    "awesome agent",
    "awesome prompt",
    "awesome mcp",
    "awesome chatgpt",
    "awesome machine-learning",
    "awesome deep-learning",
    "awesome generative-ai",
    "awesome stable-diffusion",
]

SEARCH_RESULTS_PER_QUERY = 50

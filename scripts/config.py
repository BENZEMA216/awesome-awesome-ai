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

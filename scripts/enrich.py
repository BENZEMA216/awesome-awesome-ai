"""Enrich candidate repos with metadata and auto-tags."""
from datetime import date

from scripts.config import CATEGORIES, DATA_DIR
from scripts.github_client import GitHubClient


CATEGORY_KEYWORDS = {
    "prompts": ["prompt", "chatgpt-prompts", "gpt-prompts"],
    "cli-tools": ["cli", "terminal", "command-line"],
    "mcp-servers": ["mcp", "model-context-protocol"],
    "agents": ["agent", "autonomous", "crew", "swarm"],
    "models": ["model", "llm", "foundation-model"],
    "datasets": ["dataset", "data", "corpus", "benchmark"],
    "papers": ["paper", "research", "arxiv", "survey"],
    "coding": ["coding", "copilot", "code-generation", "devtools"],
    "media": ["image", "video", "audio", "diffusion", "generation", "art"],
    "productivity": ["productivity", "workflow", "automation", "assistant"],
}

TAG_KEYWORDS = [
    "chatgpt", "gpt", "openai", "claude", "anthropic", "llama", "mistral",
    "langchain", "llamaindex", "huggingface", "transformers", "diffusion",
    "stable-diffusion", "midjourney", "comfyui", "prompt-engineering",
    "rag", "fine-tuning", "embeddings", "vector-database", "ai-safety",
    "multimodal", "text-to-image", "text-to-speech", "speech-to-text",
    "nlp", "computer-vision", "reinforcement-learning",
]


def guess_category(full_name: str, description: str) -> str:
    """Guess primary category from repo name and description."""
    text = f"{full_name} {description}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return category
    return "other"


def auto_tag(full_name: str, description: str, readme_text: str) -> list[str]:
    """Generate tags from repo name, description, and README."""
    text = f"{full_name} {description} {readme_text[:2000]}".lower()
    tags = []
    for kw in TAG_KEYWORDS:
        if kw in text and kw not in tags:
            tags.append(kw)
    return tags[:15]


def enrich_repo(client: GitHubClient, full_name: str) -> dict:
    """Fetch metadata and auto-classify a single repo."""
    meta = client.get_repo_metadata(full_name)
    readme = client.get_readme_content(full_name)

    category = guess_category(full_name, meta.get("description", ""))
    tags = auto_tag(full_name, meta.get("description", ""), readme)

    return {
        "repo": meta["repo"],
        "name": meta["name"],
        "description": meta["description"],
        "url": meta["url"],
        "category": category,
        "tags": tags,
        "stars": meta["stars"],
        "forks": meta["forks"],
        "last_updated": meta["last_updated"],
        "last_commit": meta["last_commit"],
        "added_date": date.today().isoformat(),
        "status": "pending",
        "stars_growth_7d": 0,
    }


def enrich_candidates(candidate_names: list[str], client: GitHubClient = None) -> list[dict]:
    """Enrich a list of candidate repo names."""
    if client is None:
        client = GitHubClient()

    enriched = []
    for name in candidate_names:
        try:
            repo = enrich_repo(client, name)
            enriched.append(repo)
            print(f"  Enriched: {name} -> {repo['category']} ({len(repo['tags'])} tags)")
        except Exception as e:
            print(f"  ! Failed to enrich {name}: {e}")
    return enriched


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        results = enrich_candidates(sys.argv[1:])
        for r in results:
            print(f"{r['repo']}: {r['category']} | {r['tags']}")

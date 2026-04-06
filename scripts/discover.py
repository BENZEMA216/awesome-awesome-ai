"""Discover candidate awesome-list repos from multiple sources."""
import re
from datetime import date, timedelta

from scripts.config import (
    MIN_STARS,
    MAX_INACTIVE_DAYS,
    MIN_README_LENGTH,
    MIN_LINK_DENSITY,
    SEARCH_QUERIES,
    SEARCH_RESULTS_PER_QUERY,
    DATA_DIR,
)
from scripts.data_io import is_duplicate
from scripts.github_client import GitHubClient


def extract_github_links(readme_text: str) -> list[str]:
    """Extract GitHub repo full names (owner/repo) from markdown text."""
    pattern = r"https?://github\.com/([\w\-\.]+/[\w\-\.]+)"
    matches = re.findall(pattern, readme_text)
    seen = set()
    result = []
    for match in matches:
        clean = match.rstrip("/.")
        if "/" not in clean:
            continue
        parts = clean.split("/")
        full_name = f"{parts[0]}/{parts[1]}"
        if full_name not in seen:
            seen.add(full_name)
            result.append(full_name)
    return result


def passes_quality_gate(repo_meta: dict, readme_text: str) -> bool:
    """Check if a repo meets minimum quality thresholds."""
    if repo_meta.get("stars", 0) < MIN_STARS:
        return False

    last_commit = repo_meta.get("last_commit", "")
    if last_commit:
        try:
            commit_date = date.fromisoformat(last_commit[:10])
            if (date.today() - commit_date).days > MAX_INACTIVE_DAYS:
                return False
        except ValueError:
            pass

    if len(readme_text) < MIN_README_LENGTH:
        return False

    link_count = len(re.findall(r"\[.*?\]\(.*?\)", readme_text))
    if link_count < MIN_LINK_DENSITY:
        return False

    return True


def discover_from_search(client, queries: list[str], max_per_query: int = SEARCH_RESULTS_PER_QUERY) -> set[str]:
    """Search GitHub for candidate repos."""
    candidates = set()
    for query in queries:
        repos = client.search_repos(query, max_results=max_per_query)
        for repo in repos:
            candidates.add(repo.full_name)
    return candidates


def discover_from_awesome_list(client, awesome_repo: str = "sindresorhus/awesome") -> set[str]:
    """Extract AI-related links from sindresorhus/awesome."""
    readme = client.get_readme_content(awesome_repo)
    all_links = extract_github_links(readme)
    ai_keywords = {"ai", "llm", "agent", "prompt", "machine-learning", "deep-learning",
                   "gpt", "chatgpt", "generative", "diffusion", "nlp", "mcp"}
    candidates = set()
    for link in all_links:
        lower = link.lower()
        if any(kw in lower for kw in ai_keywords):
            candidates.add(link)
    return candidates


def discover_from_indexed(client, data_dir=DATA_DIR) -> set[str]:
    """Crawl READMEs of already-indexed repos for new links (depth=1)."""
    from scripts.data_io import get_all_repos
    candidates = set()
    for repo in get_all_repos(data_dir):
        if repo.get("status") != "approved":
            continue
        readme = client.get_readme_content(repo["repo"])
        links = extract_github_links(readme)
        candidates.update(links)
    return candidates


def run_discovery(client=None, data_dir=DATA_DIR) -> list[str]:
    """Run full discovery pipeline. Returns list of new candidate repo full names."""
    if client is None:
        client = GitHubClient()

    print("Searching GitHub...")
    candidates = discover_from_search(client, SEARCH_QUERIES)

    print("Scanning sindresorhus/awesome...")
    candidates |= discover_from_awesome_list(client)

    print("Scanning indexed repos...")
    candidates |= discover_from_indexed(client, data_dir)

    new_candidates = []
    for full_name in sorted(candidates):
        if is_duplicate(data_dir, full_name):
            continue
        try:
            meta = client.get_repo_metadata(full_name)
            readme = client.get_readme_content(full_name)
            if passes_quality_gate(meta, readme):
                new_candidates.append(full_name)
                print(f"  + {full_name} ({meta['stars']} stars)")
        except Exception as e:
            print(f"  ! {full_name}: {e}")

    print(f"Found {len(new_candidates)} new candidates")
    return new_candidates


if __name__ == "__main__":
    run_discovery()

"""Daily tracking: update metrics and compute trending."""
from scripts.config import DATA_DIR
from scripts.data_io import load_all, save_category
from scripts.github_client import GitHubClient


def compute_trending(repos: list[dict], limit: int = 10) -> list[dict]:
    """Compute 7-day star growth and return top repos."""
    for repo in repos:
        prev = repo.get("stars_prev_7d")
        current = repo.get("stars", 0)
        if prev is not None:
            repo["stars_growth_7d"] = current - prev
        else:
            repo["stars_growth_7d"] = 0
    return sorted(repos, key=lambda r: r["stars_growth_7d"], reverse=True)[:limit]


def track_all(client=None, data_dir=DATA_DIR) -> None:
    """Update metrics for all approved repos."""
    if client is None:
        client = GitHubClient()

    all_data = load_all(data_dir)
    total_updated = 0

    for category, repos in all_data.items():
        changed = False
        for repo in repos:
            if repo.get("status") != "approved":
                continue
            try:
                meta = client.get_repo_metadata(repo["repo"])
                repo["stars_prev_7d"] = repo.get("stars", 0)
                repo["stars"] = meta["stars"]
                repo["forks"] = meta["forks"]
                repo["last_commit"] = meta["last_commit"]
                repo["last_updated"] = meta["last_updated"]
                changed = True
                total_updated += 1
            except Exception as e:
                print(f"  ! Failed to update {repo['repo']}: {e}")

        if changed:
            save_category(data_dir, category, repos)

    print(f"Updated {total_updated} repos")


if __name__ == "__main__":
    track_all()

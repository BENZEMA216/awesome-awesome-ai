from pathlib import Path

import yaml


def load_category(data_dir: Path, category: str) -> list[dict]:
    """Load repos from a single category YAML file."""
    path = data_dir / f"{category}.yml"
    if not path.exists():
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, list) else []


def save_category(data_dir: Path, category: str, repos: list[dict]) -> None:
    """Save repos to a single category YAML file."""
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / f"{category}.yml"
    with open(path, "w") as f:
        yaml.dump(repos, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def load_all(data_dir: Path) -> dict[str, list[dict]]:
    """Load all category files. Returns {category: [repos]}."""
    result = {}
    for path in sorted(data_dir.glob("*.yml")):
        category = path.stem
        result[category] = load_category(data_dir, category)
    return result


def get_all_repos(data_dir: Path) -> list[dict]:
    """Load all repos from all categories as a flat list."""
    repos = []
    for category_repos in load_all(data_dir).values():
        repos.extend(category_repos)
    return repos


def is_duplicate(data_dir: Path, repo_full_name: str) -> bool:
    """Check if a repo is already in any data file."""
    for repo in get_all_repos(data_dir):
        if repo["repo"] == repo_full_name:
            return True
    return False

"""Generate README.md from YAML data files."""
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from scripts.config import CATEGORIES, CATEGORIES_ZH
from scripts.data_io import load_all


def build_template_context(data_dir: Path, github_repo: str) -> dict:
    """Build the template context from data files."""
    all_data = load_all(data_dir)

    repos_by_category = {}
    all_approved = []
    for category, repos in all_data.items():
        approved = [r for r in repos if r.get("status") == "approved"]
        approved.sort(key=lambda r: r.get("stars", 0), reverse=True)
        if approved:
            repos_by_category[category] = approved
        all_approved.extend(approved)

    for repo in all_approved:
        repo.setdefault("stars_growth_7d", 0)
    trending = sorted(all_approved, key=lambda r: r.get("stars_growth_7d", 0), reverse=True)[:10]

    return {
        "github_repo": github_repo,
        "last_updated": date.today().isoformat(),
        "categories": CATEGORIES,
        "categories_zh": CATEGORIES_ZH,
        "repos_by_category": repos_by_category,
        "trending": trending,
    }


def generate_readme(data_dir: Path, templates_dir: Path, output_path: Path, github_repo: str) -> None:
    """Generate README.md from data and template."""
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template("readme.md.j2")
    ctx = build_template_context(data_dir, github_repo)
    content = template.render(**ctx)
    output_path.write_text(content)
    print(f"Generated {output_path} with {sum(len(v) for v in ctx['repos_by_category'].values())} repos")


if __name__ == "__main__":
    from scripts.config import DATA_DIR, TEMPLATES_DIR, README_PATH
    generate_readme(DATA_DIR, TEMPLATES_DIR, README_PATH, "BENZEMA216/awesome-awesome-ai")

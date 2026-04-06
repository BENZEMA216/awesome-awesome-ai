"""Generate a review PR with pending candidates."""
import subprocess
import sys
from datetime import date

from scripts.config import DATA_DIR
from scripts.data_io import load_category, save_category


def add_pending_to_data(candidates: list[dict], data_dir=DATA_DIR) -> dict[str, int]:
    """Add pending candidates to their category data files. Returns counts per category."""
    counts = {}
    for repo in candidates:
        category = repo.get("category", "other")
        existing = load_category(data_dir, category)
        existing.append(repo)
        save_category(data_dir, category, existing)
        counts[category] = counts.get(category, 0) + 1
    return counts


def create_review_branch(candidates: list[dict], data_dir=DATA_DIR) -> str:
    """Create a new branch with pending candidates and return branch name."""
    branch_name = f"discover/{date.today().isoformat()}"

    subprocess.run(["git", "checkout", "-b", branch_name], check=True, cwd=data_dir.parent)

    counts = add_pending_to_data(candidates, data_dir)

    subprocess.run(["git", "add", "data/"], check=True, cwd=data_dir.parent)
    msg = f"feat: add {len(candidates)} candidates for review\n\n"
    for cat, count in sorted(counts.items()):
        msg += f"- {cat}: {count}\n"
    subprocess.run(["git", "commit", "-m", msg], check=True, cwd=data_dir.parent)

    return branch_name


def format_pr_body(candidates: list[dict]) -> str:
    """Format PR body listing all candidates for review."""
    lines = [
        "## New Candidates for Review",
        "",
        f"Found **{len(candidates)}** new repos. Review each and remove any you don't want.",
        "Merge this PR to approve the remaining repos.",
        "",
        "| Repo | Stars | Category | Tags |",
        "|------|-------|----------|------|",
    ]
    for repo in sorted(candidates, key=lambda r: r.get("stars", 0), reverse=True):
        tags = ", ".join(f"`{t}`" for t in repo.get("tags", [])[:5])
        lines.append(
            f"| [{repo['repo']}]({repo['url']}) | {repo['stars']:,} | {repo['category']} | {tags} |"
        )
    return "\n".join(lines)


def create_review_pr(candidates: list[dict], data_dir=DATA_DIR) -> None:
    """Full flow: branch, commit, push, create PR."""
    if not candidates:
        print("No candidates to review.")
        return

    branch = create_review_branch(candidates, data_dir)
    root = data_dir.parent

    subprocess.run(["git", "push", "-u", "origin", branch], check=True, cwd=root)

    body = format_pr_body(candidates)
    subprocess.run(
        ["gh", "pr", "create",
         "--title", f"Add {len(candidates)} new repos ({date.today().isoformat()})",
         "--body", body],
        check=True, cwd=root,
    )
    print(f"PR created on branch {branch}")

    subprocess.run(["git", "checkout", "main"], check=True, cwd=root)


if __name__ == "__main__":
    from scripts.discover import run_discovery
    from scripts.enrich import enrich_candidates

    candidates = run_discovery()
    enriched = enrich_candidates(candidates)
    create_review_pr(enriched)

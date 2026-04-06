import tempfile
from pathlib import Path

from scripts.config import CATEGORIES
from scripts.data_io import save_category
from scripts.generate import generate_readme, build_template_context


def _make_repo(repo="owner/name", category="prompts", stars=500, growth=10):
    return {
        "repo": repo,
        "name": repo.split("/")[1],
        "description": "A test repo for testing purposes",
        "url": f"https://github.com/{repo}",
        "category": category,
        "tags": ["test", "ai"],
        "stars": stars,
        "forks": 10,
        "last_updated": "2026-04-05",
        "last_commit": "2026-04-03",
        "added_date": "2026-04-06",
        "status": "approved",
        "stars_growth_7d": growth,
    }


def test_build_template_context(tmp_path):
    save_category(tmp_path, "prompts", [_make_repo("a/one", "prompts", 1000, 50)])
    save_category(tmp_path, "agents", [_make_repo("b/two", "agents", 500, 20)])

    ctx = build_template_context(tmp_path, "BENZEMA216/awesome-awesome-ai")
    assert "repos_by_category" in ctx
    assert len(ctx["repos_by_category"]["prompts"]) == 1
    assert len(ctx["trending"]) == 2
    assert ctx["trending"][0]["stars_growth_7d"] >= ctx["trending"][1]["stars_growth_7d"]


def test_generate_readme(tmp_path):
    save_category(tmp_path, "prompts", [_make_repo("a/one", "prompts", 1000, 50)])
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()

    # Copy the real template
    real_template = Path(__file__).parent.parent / "templates" / "readme.md.j2"
    (templates_dir / "readme.md.j2").write_text(real_template.read_text())

    output = tmp_path / "README.md"
    generate_readme(tmp_path, templates_dir, output, "BENZEMA216/awesome-awesome-ai")

    content = output.read_text()
    assert "Awesome Awesome AI" in content
    assert "a/one" in content or "one" in content
    assert "Prompt Collections" in content


def test_only_approved_repos(tmp_path):
    repos = [
        _make_repo("a/one", "prompts", 1000, 50),
        {**_make_repo("b/rejected", "prompts", 2000, 100), "status": "rejected"},
        {**_make_repo("c/pending", "prompts", 3000, 200), "status": "pending"},
    ]
    save_category(tmp_path, "prompts", repos)

    ctx = build_template_context(tmp_path, "test/repo")
    assert len(ctx["repos_by_category"]["prompts"]) == 1
    assert ctx["repos_by_category"]["prompts"][0]["repo"] == "a/one"

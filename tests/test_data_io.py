import tempfile
from pathlib import Path

import yaml

from scripts.data_io import load_category, save_category, load_all, get_all_repos, is_duplicate


def _make_repo(repo="owner/name", category="prompts", status="approved", stars=500):
    return {
        "repo": repo,
        "name": repo.split("/")[1],
        "description": "Test repo",
        "url": f"https://github.com/{repo}",
        "category": category,
        "tags": ["test"],
        "stars": stars,
        "forks": 10,
        "last_updated": "2026-04-05",
        "last_commit": "2026-04-03",
        "added_date": "2026-04-06",
        "status": status,
    }


def test_save_and_load_category(tmp_path):
    repos = [_make_repo("a/one"), _make_repo("b/two")]
    save_category(tmp_path, "prompts", repos)
    loaded = load_category(tmp_path, "prompts")
    assert len(loaded) == 2
    assert loaded[0]["repo"] == "a/one"


def test_load_empty_category(tmp_path):
    (tmp_path / "prompts.yml").write_text("# empty\n[]\n")
    loaded = load_category(tmp_path, "prompts")
    assert loaded == []


def test_load_all(tmp_path):
    save_category(tmp_path, "prompts", [_make_repo("a/one", category="prompts")])
    save_category(tmp_path, "agents", [_make_repo("b/two", category="agents")])
    all_data = load_all(tmp_path)
    assert "prompts" in all_data
    assert "agents" in all_data
    assert len(all_data["prompts"]) == 1


def test_get_all_repos(tmp_path):
    save_category(tmp_path, "prompts", [_make_repo("a/one", category="prompts")])
    save_category(tmp_path, "agents", [_make_repo("b/two", category="agents")])
    repos = get_all_repos(tmp_path)
    assert len(repos) == 2


def test_is_duplicate(tmp_path):
    save_category(tmp_path, "prompts", [_make_repo("a/one")])
    assert is_duplicate(tmp_path, "a/one") is True
    assert is_duplicate(tmp_path, "c/three") is False

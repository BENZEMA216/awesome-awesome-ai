import re
from unittest.mock import MagicMock, patch

from scripts.discover import (
    extract_github_links,
    passes_quality_gate,
    discover_from_search,
    discover_from_awesome_list,
)


def test_extract_github_links():
    readme = """
    Check out [awesome-ai](https://github.com/owner/awesome-ai) and
    also [another](https://github.com/org/another-repo). Not a github link:
    [docs](https://example.com/foo).
    """
    links = extract_github_links(readme)
    assert "owner/awesome-ai" in links
    assert "org/another-repo" in links
    assert len(links) == 2


def test_passes_quality_gate_good():
    repo_meta = {
        "stars": 500,
        "last_commit": "2026-03-01",
    }
    readme = "x" * 2000 + "\n" + "\n".join(f"[link{i}](https://example.com)" for i in range(20))
    assert passes_quality_gate(repo_meta, readme) is True


def test_passes_quality_gate_low_stars():
    repo_meta = {"stars": 50, "last_commit": "2026-03-01"}
    readme = "x" * 2000 + "\n" + "\n".join(f"[link{i}](https://example.com)" for i in range(20))
    assert passes_quality_gate(repo_meta, readme) is False


def test_passes_quality_gate_stale():
    repo_meta = {"stars": 500, "last_commit": "2024-01-01"}
    readme = "x" * 2000 + "\n" + "\n".join(f"[link{i}](https://example.com)" for i in range(20))
    assert passes_quality_gate(repo_meta, readme) is False


def test_passes_quality_gate_short_readme():
    repo_meta = {"stars": 500, "last_commit": "2026-03-01"}
    readme = "short"
    assert passes_quality_gate(repo_meta, readme) is False


def test_discover_from_search():
    mock_repo = MagicMock()
    mock_repo.full_name = "owner/awesome-ai"
    mock_repo.stargazers_count = 500

    mock_client = MagicMock()
    mock_client.search_repos.return_value = [mock_repo]

    results = discover_from_search(mock_client, ["awesome ai"], max_per_query=10)
    assert "owner/awesome-ai" in results

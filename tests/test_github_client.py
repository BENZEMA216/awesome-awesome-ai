import os
from unittest.mock import MagicMock, patch

from scripts.github_client import GitHubClient


def test_init_with_token():
    with patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}):
        client = GitHubClient()
        assert client.token == "test-token"


def test_init_without_token():
    with patch.dict(os.environ, {}, clear=True):
        client = GitHubClient()
        assert client.token is None


def test_get_repo_metadata():
    mock_repo = MagicMock()
    mock_repo.full_name = "owner/repo"
    mock_repo.name = "repo"
    mock_repo.description = "A test repo"
    mock_repo.html_url = "https://github.com/owner/repo"
    mock_repo.stargazers_count = 500
    mock_repo.forks_count = 50
    mock_repo.pushed_at.isoformat.return_value = "2026-04-03T00:00:00"
    mock_repo.updated_at.isoformat.return_value = "2026-04-05T00:00:00"

    mock_github = MagicMock()
    mock_github.get_repo.return_value = mock_repo

    client = GitHubClient()
    client.gh = mock_github

    meta = client.get_repo_metadata("owner/repo")
    assert meta["repo"] == "owner/repo"
    assert meta["stars"] == 500
    assert meta["forks"] == 50


def test_search_repos():
    mock_repo = MagicMock()
    mock_repo.full_name = "owner/awesome-ai"
    mock_repo.stargazers_count = 200

    mock_github = MagicMock()
    mock_github.search_repositories.return_value = [mock_repo]

    client = GitHubClient()
    client.gh = mock_github

    results = client.search_repos("awesome ai", max_results=10)
    assert len(results) == 1
    assert results[0].full_name == "owner/awesome-ai"

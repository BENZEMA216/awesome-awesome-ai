import os
import time

from github import Github, RateLimitExceededException


class GitHubClient:
    """GitHub API wrapper with rate limiting."""

    def __init__(self):
        self.token = os.environ.get("GITHUB_TOKEN")
        self.gh = Github(self.token) if self.token else Github()

    def _wait_for_rate_limit(self):
        """Sleep until rate limit resets if exhausted."""
        try:
            rate = self.gh.get_rate_limit()
            if int(rate.core.remaining) < 10:
                wait = (rate.core.reset - rate.core.reset.utcnow()).total_seconds() + 5
                if wait > 0:
                    print(f"Rate limit low, sleeping {wait:.0f}s...")
                    time.sleep(wait)
        except (TypeError, ValueError):
            pass

    def get_repo_metadata(self, full_name: str) -> dict:
        """Fetch metadata for a single repo."""
        self._wait_for_rate_limit()
        repo = self.gh.get_repo(full_name)
        return {
            "repo": repo.full_name,
            "name": repo.name,
            "description": (repo.description or "")[:200],
            "url": repo.html_url,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "last_commit": repo.pushed_at.isoformat()[:10],
            "last_updated": repo.updated_at.isoformat()[:10],
        }

    def search_repos(self, query: str, max_results: int = 50) -> list:
        """Search GitHub repos with rate limiting."""
        self._wait_for_rate_limit()
        try:
            results = self.gh.search_repositories(query=query, sort="stars", order="desc")
            return list(results[:max_results])
        except RateLimitExceededException:
            print(f"Search rate limited for query: {query}")
            time.sleep(60)
            return []

    def get_readme_content(self, full_name: str) -> str:
        """Fetch decoded README content for a repo."""
        self._wait_for_rate_limit()
        try:
            repo = self.gh.get_repo(full_name)
            readme = repo.get_readme()
            return readme.decoded_content.decode("utf-8")
        except Exception:
            return ""

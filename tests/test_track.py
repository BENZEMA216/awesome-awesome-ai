from scripts.track import compute_trending


def _make_repo(name, stars, prev_stars=None):
    r = {
        "repo": f"owner/{name}",
        "name": name,
        "stars": stars,
        "status": "approved",
        "tags": [],
    }
    if prev_stars is not None:
        r["stars_prev_7d"] = prev_stars
    return r


def test_compute_trending_with_history():
    repos = [
        _make_repo("fast", 1000, 800),   # +200
        _make_repo("slow", 500, 490),     # +10
        _make_repo("new", 300, None),      # no history, growth = 0
    ]
    result = compute_trending(repos)
    assert result[0]["repo"] == "owner/fast"
    assert result[0]["stars_growth_7d"] == 200


def test_compute_trending_limit():
    repos = [_make_repo(f"r{i}", 100 + i, 100) for i in range(20)]
    result = compute_trending(repos, limit=10)
    assert len(result) == 10

# Contributing to Awesome Awesome AI

## Suggesting a Repo

Open an issue with:
- **Repo URL**: GitHub link
- **Category**: One of: prompts, cli-tools, mcp-servers, agents, models, datasets, papers, coding, media, productivity, other
- **Tags**: Relevant tags (lowercase, hyphenated)
- **Why**: Brief explanation of why it belongs here

## Quality Criteria

Repos must meet these minimum thresholds:
- At least 100 GitHub stars
- Active (commit within the last 6 months)
- Must be a resource aggregation repo (curated list, not a single tool)
- README must contain substantial content with links to resources

## Updating Existing Entries

If a repo's category or tags are wrong, open a PR editing the relevant `data/*.yml` file.

## Running Locally

```bash
pip install -r requirements.txt
export GITHUB_TOKEN="your-token"
python -m scripts.generate  # regenerate README
python -m scripts.track     # update metrics
```

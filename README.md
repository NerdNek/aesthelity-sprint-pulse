# Aesthelity Sprint Pulse

[Open dashboard](https://nerdnek.github.io/aesthelity-sprint-pulse/)

GitHub Actions captures public Aesthelity-Team/Aesthelity issues, PRs, and checks
at **8 AM, noon, and 6 PM America/Los_Angeles**, including daylight saving changes.
GitHub may delay scheduled runs. Reload the page to load the latest publication.
The displayed snapshot timestamp is the evidence of freshness.

## Refresh now

Open **Actions → Refresh sprint dashboard → Run workflow → Run workflow**.
A successful run updates the snapshot files and deploys the website at the same URL.
Failed reads stop publication, leaving the last deployed snapshot available.
No personal access token, paid service, local server, or computer left running is needed.
Standard GitHub-hosted runners are used in this public repository.

## Source and interpretation

- Current GitHub sprint labels define scope.
- Closed issue counts, matched PR merges, reviews, and CI are separate signals.
- PRs match through closing references or exact story codes in titles.
- Project board fields, live demo acceptance, and deployment are not inferred.
- Issue assignees describe ownership; counts do not measure effort.
- Workflow-generated commits do not trigger a new workflow; the same run deploys Pages directly.

## Local update

With Python 3 and authenticated GitHub CLI installed:

```sh
python3 scripts/refresh_snapshot.py
```

The script fetches data read-only from the team repository. Only this dashboard
repository is modified by the automation.

## Visual layers

- Completion ring and labeled issue cells: one cell per issue; closure and open PRs have different symbols.
- Sprint comparison: closed/open-PR/remaining issue composition, directly labeled.
- Feature and assignment bars: shared count scale within each chart.
- Repository-wide top-down Git graph: actual commit parents, merge diamonds, current branch tips and open PR heads (including forks). Branch focus retains default-branch context.
- Graph is bounded to 140 captured commits and a fetch depth of 300 per branch, with visible boundary notes. Branch comparisons are within fetched history.
- Branch list provides a compact alternative to the horizontally scrollable graph.
- Sprint, search, state filter, branch focus, graph/list mode, and history extent are URL-backed; browser Back restores them.
- Green = closure or branch-tip focus; purple = open PR or merge shape (separate labeled views); rust = failing checks; neutral = remaining or unknown. Text and shape carry the meaning without color.

The snapshot generator fetches commit objects in a temporary bare repository. It never checks out or changes the team application. Public data only; no secret is included in the published files.

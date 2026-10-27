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

"""Validate the evidence contract before publishing, independent of rendering."""
import json
from pathlib import Path

snapshot = json.loads((Path(__file__).resolve().parents[1] / 'snapshot.json').read_text())
issues = snapshot['issues']
assert len({i['number'] for i in issues}) == len(issues), 'Duplicate issues inflate counts'
assert all(i['state'] in {'OPEN', 'CLOSED'} for i in issues)
graph = snapshot['graph']
commits = graph['commits']
rank = {c['sha']: n for n, c in enumerate(commits)}
assert len(rank) == len(commits), 'A commit must appear only once'
for commit in commits:
    assert len(commit['sha']) == 40
    for parent in commit['parents']:
        if parent in rank:
            assert rank[parent] > rank[commit['sha']], 'Parent edge must point down'
if not graph['partial']:
    assert all(b['sha'] in rank for b in graph['branches']), 'Missing branch tip'
assert any(b['name'] == graph['defaultBranch'] for b in graph['branches'])
assert all(b['ahead'] >= 0 and b['behind'] >= 0 for b in graph['branches'])
print(f'Validated {len(issues)} issues, {len(graph["branches"])} tips, {len(commits)} commits')

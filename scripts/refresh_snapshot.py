#!/usr/bin/env python3
"""Refresh the public GitHub snapshot. No personal token or third-party packages."""
import datetime
import json
import pathlib
import re
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = 'Aesthelity-Team/Aesthelity'

def github(*args):
    for attempt in range(3):
        result = subprocess.run(['gh', *args], text=True, capture_output=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
        if attempt == 2:
            raise RuntimeError('GitHub fetch failed: ' + result.stderr.strip())
        time.sleep(2 ** attempt)

# Finish every read before replacing any published data. A failed run retains
# the previous deployed snapshot rather than publishing incomplete results.
issues = github('issue', 'list', '--repo', REPO, '--state', 'all', '--limit', '1000',
    '--json', 'number,title,body,state,labels,assignees,url,createdAt,closedAt,updatedAt')
prs = github('pr', 'list', '--repo', REPO, '--state', 'all', '--limit', '1000',
    '--json', 'number,title,state,isDraft,url,createdAt,mergedAt,closedAt,updatedAt,author,closingIssuesReferences,reviewDecision,statusCheckRollup')
runs = github('api', f'repos/{REPO}/actions/runs?per_page=8')
if not issues or len(issues) >= 1000 or len(prs) >= 1000:
    raise RuntimeError('Snapshot is empty or may be truncated; refusing to publish.')

now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rows=[]
for i in issues:
 labels=[l['name'] for l in i['labels']]; sprint=next((l for l in labels if re.fullmatch(r'sprint-\d+',l)),None)
 if not sprint and 'later-queue' not in labels: continue
 code=re.match(r'([A-Z]+-\d+[a-z]?)',i['title']); code=code.group(1) if code else '#'+str(i['number'])
 links=[]
 for pr in prs:
  explicit=any(x['number']==i['number'] for x in pr['closingIssuesReferences'])
  title=bool(re.search(r'(?<![A-Z0-9-])'+re.escape(code)+r'(?![A-Z0-9])',pr['title'],re.I)) if not code.startswith('#') else False
  if explicit or title:
   checks=pr['statusCheckRollup']; conclusions=[c.get('conclusion') or c.get('state') or c.get('status') for c in checks]
   ci='failed' if any(c in ['FAILURE','ERROR','TIMED_OUT','CANCELLED','ACTION_REQUIRED'] for c in conclusions) else 'passed' if conclusions and all(c in ['SUCCESS','NEUTRAL','SKIPPED'] for c in conclusions) else 'pending' if conclusions else 'unknown'
   links.append(dict(number=pr['number'],title=pr['title'],state=pr['state'],url=pr['url'],review=pr['reviewDecision'],ci=ci,checks=[{'name':c.get('name') or c.get('context'),'result':c.get('conclusion') or c.get('state') or c.get('status')} for c in checks],basis='GitHub closing reference' if explicit else 'Story code in PR title',author=pr['author']['login']))
 points=re.search(r'Story points:\*?\*?\s*(\d+)',i['body'],re.I)
 rows.append(dict(number=i['number'],title=i['title'],code=code,sprint=sprint or 'later-queue',state=i['state'],url=i['url'],owners=[a['login'] for a in i['assignees']],points=int(points.group(1)) if points else None,proposed=bool(points and 'proposed' in i['body'][points.end():points.end()+35]),closedAt=i['closedAt'],updatedAt=i['updatedAt'],prs=links,module=code.split('-')[0]))
data=dict(capturedAt=now,repo='Aesthelity-Team/Aesthelity',issues=sorted(rows,key=lambda x:x['number']),runs=[dict(name=r['name'],branch=r['head_branch'],status=r['status'],conclusion=r['conclusion'],url=r['html_url'],createdAt=r['created_at']) for r in runs.get('workflow_runs',[])])

encoded = json.dumps(data, indent=2)
for name, content in [('snapshot.json', encoded + '\n'),
                       ('data.js', 'window.SPRINT_SNAPSHOT = ' + encoded + ';\n')]:
    destination = ROOT / name
    temporary = destination.with_suffix(destination.suffix + '.tmp')
    temporary.write_text(content)
    temporary.replace(destination)
print(f'Captured {len(rows)} labeled issues and inspected {len(prs)} PRs at {now}')

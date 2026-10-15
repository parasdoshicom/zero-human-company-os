#!/usr/bin/env python3
"""Bounded text checks; not a complete security audit or remote URL checker."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
# Scan authored text, excluding generated/private outputs and Git internals.
patterns = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
            r'\bgh[pousr]_[A-Za-z0-9]{30,}\b', r'\bsk-[A-Za-z0-9_-]{24,}\b',
            r'/Users/[A-Za-z][^\s)\"]*', r'\bAKIA[A-Z0-9]{16}\b']
for path in ROOT.rglob('*'):
    if not path.is_file() or any(p in {'.git','__pycache__','demo-output','private','presentation'} for p in path.relative_to(ROOT).parts):
        continue
    if path.suffix not in {'.md','.py','.json','.html','.yml','.yaml','.txt'}:
        continue
    text = path.read_text()
    for pattern in patterns:
        if re.search(pattern, text): errors.append(f'{path.relative_to(ROOT)}: possible secret or private path; inspect locally')
    if path.suffix == '.md':
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in link or link.startswith(('#','mailto:')): continue
            target = link.split('#')[0]
            if target and not (path.parent / target).exists():
                errors.append(f'{path.relative_to(ROOT)}: broken local link {target}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('PASS: authored text local links and selected secret/private-path patterns')
print('Scope excludes presentation binaries and generated outputs; manual review still required.')

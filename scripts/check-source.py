#!/usr/bin/env python3
"""Basic citation, include, semantic-label and cross-reference checks."""
from pathlib import Path
import re
import sys

INCLUDE = re.compile(r'\{\{<\s*include\s+([^\s>]+)\s*>\}\}')
LABEL = re.compile(r'\{#([\w-]+)\}')
REF = re.compile(r'(?<![\w/@])@((?:sec|eq|fig|tbl|thm|prp|lem|cor|def|asm|rem|exm)-[\w-]+)')
CITE = re.compile(r'(?<![\w/@])@([A-Za-z][\w:-]*)')
BIB = re.compile(r'@(?:article|book|inproceedings|misc|techreport|phdthesis|mastersthesis|inbook|unpublished|online)\s*\{\s*([^,\s]+)', re.I)

def check(root):
    errors, seen, text_parts = [], {}, []
    main = root / 'index.qmd'
    if not main.exists():
        return ['index.qmd missing']
    def visit(path, stack):
        if path in stack:
            errors.append(f'cyclic include: {path}')
            return
        if not path.exists():
            errors.append(f'missing include: {path.relative_to(root)}')
            return
        source = path.read_text(encoding='utf-8')
        for lineno, line in enumerate(source.splitlines(), 1):
            for label in LABEL.findall(line):
                if label in seen:
                    errors.append(f'duplicate label {label}: {path}:{lineno}, {seen[label]}')
                seen[label] = f'{path.relative_to(root)}:{lineno}'
        parts, pos = [], 0
        for match in INCLUDE.finditer(source):
            parts.append(source[pos:match.start()])
            pos = match.end()
            child = (root / match.group(1)).resolve()
            if not child.is_relative_to(root.resolve()):
                errors.append(f'include outside root: {child}')
                continue
            visit(child, stack + (path,))
        parts.append(source[pos:])
        text_parts.extend(parts)
    visit(main, tuple())
    combined = '\n'.join(text_parts)
    for ref in sorted(set(REF.findall(combined))):
        if ref not in seen:
            errors.append(f'unresolved cross-reference @{ref}')
    bibpath = root / 'references.bib'
    bib = bibpath.read_text(encoding='utf-8') if bibpath.exists() else ''
    keys = set(BIB.findall(bib))
    for cite in sorted(set(CITE.findall(combined))):
        if cite.startswith(('sec-', 'eq-', 'fig-', 'tbl-', 'thm-', 'prp-', 'lem-', 'cor-', 'def-', 'asm-', 'rem-', 'exm-')):
            continue
        if cite not in keys:
            errors.append(f'missing bibliography key @{cite}')
    return errors

if __name__ == '__main__':
    errors = check(Path(__file__).resolve().parent.parent)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        raise SystemExit(1)
    print('Source includes, labels and citations OK')

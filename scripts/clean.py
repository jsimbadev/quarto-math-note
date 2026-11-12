#!/usr/bin/env python3
from pathlib import Path
import shutil
root = Path(__file__).resolve().parent.parent
for name in ('_output', '.quarto'):
    path = root / name
    if path.exists():
        shutil.rmtree(path)
for name in ('index.tex', 'index.aux', 'index.log'):
    path = root / name
    if path.exists():
        path.unlink()
print('Removed generated outputs')

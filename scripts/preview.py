#!/usr/bin/env python3
"""Touch the main Quarto entrypoint when included source files change."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import threading
INPUTS = ('sections', 'appendices', 'figures', 'filters', 'styles', 'tex',
          '_quarto.yml', 'macros.tex', 'references.bib', 'styles.css')
def snapshot(root):
    observed = {}
    for name in INPUTS:
        path = root / name
        for f in (path.rglob('*') if path.is_dir() else (path,)):
            try:
                if f.is_file():
                    observed[str(f)] = hashlib.sha256(f.read_bytes()).digest()
            except FileNotFoundError:
                pass
    return observed
def watch(root, stopped):
    previous = snapshot(root)
    while not stopped.wait(0.5):
        current = snapshot(root)
        if current != previous:
            (root / 'index.qmd').touch()
            previous = current
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quarto', default='quarto')
    args, other = parser.parse_known_args()
    root = Path(__file__).resolve().parent.parent
    stop = threading.Event()
    watcher = threading.Thread(target=watch, args=(root, stop), daemon=True)
    watcher.start()
    try:
        return subprocess.call([args.quarto, 'preview', 'index.qmd', '--to', 'html', *other], cwd=root)
    except KeyboardInterrupt:
        return 130
    finally:
        stop.set()
        watcher.join()
if __name__ == '__main__':
    raise SystemExit(main())

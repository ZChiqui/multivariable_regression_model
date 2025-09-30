import json
import sys
from pathlib import Path

# Ensure unicode prints without crashing on Windows terminals
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if not path or not path.exists():
    print("Usage: python tools/inspect_nb.py <notebook.ipynb>")
    sys.exit(1)

nb = json.loads(path.read_text(encoding='utf-8'))

cells = nb.get('cells', [])
for i, cell in enumerate(cells):
    ctype = cell.get('cell_type')
    print(f"--- Cell {i} [{ctype}] ---")
    if ctype == 'markdown':
        src = ''.join(cell.get('source', []))
        snippet = src.strip().replace('\n', ' ')[:300]
        print(snippet)
    elif ctype == 'code':
        src_lines = cell.get('source', [])
        # Show only comment lines and the first non-comment line
        shown = []
        non_comment_line = None
        for line in src_lines:
            if line.lstrip().startswith('#'):
                shown.append(line.rstrip('\n'))
            elif non_comment_line is None and line.strip():
                non_comment_line = line.rstrip('\n')
        # Print up to 8 lines to keep it compact
        for line in shown[:8]:
            print(line)
        if non_comment_line:
            print(f"[first code]: {non_comment_line}")
    print()

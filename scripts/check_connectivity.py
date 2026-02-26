import sys
import re

with open('make_map.py', 'r') as f:
    text = f.read()

m = re.search(r'grid_lines = \[(.*?)\]', text, flags=re.DOTALL)
lines_str = m.group(1)
lines = [l.strip().strip('"').strip("'") for l in lines_str.split(',\n')]
grid = [l.split() for l in lines]

H = len(grid)
W = max(len(row) for row in grid)

states = set()
for r in grid:
    for c in r:
        if c != '..':
            states.add(c)

def get_neighbors(r, c, state):
    ns = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # ORTHOGONAL ONLY
        nr, nc = r + dr, c + dc
        if 0 <= nr < H and 0 <= nc < len(grid[nr]) and grid[nr][nc] == state:
            ns.append((nr, nc))
    return ns

errors = False
for state in states:
    # Find all cells for this state
    cells = []
    for r in range(H):
        for c in range(len(grid[r])):
            if grid[r][c] == state:
                cells.append((r, c))
    
    if not cells: continue
    
    # BFS to check contiguity
    start = cells[0]
    visited = set([start])
    queue = [start]
    
    while queue:
        curr = queue.pop(0)
        for n in get_neighbors(curr[0], curr[1], state):
            if n not in visited:
                visited.add(n)
                queue.append(n)
                
    if len(visited) != len(cells):
        errors = True
        print(f"ERROR: State {state} is NOT orthogonally continuous!")
        print(f"  Found {len(cells)} total cells, but only {len(visited)} are connected to the first found cell.")

if not errors:
    print("SUCCESS: All states are orthogonally continuous.")
else:
    sys.exit(1)

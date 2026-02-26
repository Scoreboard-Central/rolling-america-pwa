import re
with open('generate_map.py', 'r') as f: code = f.read()
grid_str = re.search(r'grid_str = """(.*?)"""', code, flags=re.DOTALL).group(1).strip()
grid = [l.split() for l in grid_str.split('\n')]
H, W = len(grid), len(grid[0])

def get_neighbors(r, c, state):
    ns = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # ORTHOGONAL ONLY
        nr, nc = r + dr, c + dc
        if 0 <= nr < H and 0 <= nc < len(grid[nr]) and grid[nr][nc] == state:
            ns.append((nr, nc))
    return ns

errors = False
for state in set(c for r in grid for c in r if c != '..'):
    cells = [(r, c) for r in range(H) for c in range(len(grid[r])) if grid[r][c] == state]
    if not cells: continue
    
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
        
        unvisited = set(cells) - visited
        print(f"  Example unvisited cell: {list(unvisited)[0]}")
        print(f"  Example visited cell: {list(visited)[0]}")

if not errors:
    print("SUCCESS: All states are orthogonally continuous.")

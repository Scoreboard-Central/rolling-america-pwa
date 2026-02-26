import re
with open('make_map.py', 'r') as f: code = f.read()
grid_lines_str = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL).group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]

H = len(grid)
W = max(len(row) for row in grid)
for r in range(H):
    grid[r].extend(['..'] * (W - len(grid[r])))

states = set(c for r in grid for c in r if c != '..')

def get_neighbors(r, c, state):
    ns = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < H and 0 <= nc < len(grid[nr]) and grid[nr][nc] == state:
            ns.append((nr, nc))
    return ns

def get_components(state):
    cells = [(r, c) for r in range(H) for c in range(W) if grid[r][c] == state]
    if not cells: return []
    
    unvisited = set(cells)
    components = []
    while unvisited:
        start = unvisited.pop()
        comp = set([start])
        queue = [start]
        while queue:
            curr = queue.pop(0)
            for n in get_neighbors(curr[0], curr[1], state):
                if n in unvisited:
                    unvisited.remove(n)
                    comp.add(n)
                    queue.append(n)
        components.append(comp)
    return components

discon = []
for s in states:
    comps = get_components(s)
    if len(comps) > 1:
        discon.append(s)

print("Disconnected states:", discon)

for s in discon:
    print(f"\nState {s}:")
    comps = get_components(s)
    for i, c in enumerate(comps):
        print(f"  Component {i}: {sorted(list(c))}")
        
    # Find bounding box of this state +/- 2
    min_r = max(0, min(r for r, c in get_components(s)[0]) - 2)
    max_r = min(H, max(r for comp in comps for r, c in comp) + 3)
    min_c = max(0, min(c for comp in comps for r, c in comp) - 2)
    max_c = min(W, max(c for comp in comps for r, c in comp) + 3)
    
    for r in range(min_r, max_r):
        row_str = ""
        for c in range(min_c, max_c):
            if grid[r][c] == s:
                row_str += f"[{grid[r][c]}] "
            else:
                row_str += f" {grid[r][c]}  "
        print(f"R{r:02d}: {row_str}")


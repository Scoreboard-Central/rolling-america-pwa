import re

with open('make_map.py', 'r') as f: code = f.read()
grid_lines_str = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL).group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]
H, W = len(grid), len(grid[0])

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

discon = ['NY', 'NC', 'MA', 'MO', 'TN']
for s in discon:
    print(f"\nState {s}:")
    comps = get_components(s)
    
    # Just print the center coordinates of each component to see how far they are
    for i, c in enumerate(comps):
        avg_r = sum(r for r, c in c) // len(c)
        avg_c = sum(col for r, col in c) // len(c)
        print(f"  Component {i}: center ({avg_r}, {avg_c}), size {len(c)}")
        
        # print the bounding box of the whole state
    min_r = max(0, min(r for r, c in get_components(s)[0]) - 2)
    max_r = min(H, max(r for comp in comps for r, c in comp) + 3)
    min_c = max(0, min(c for comp in comps for r, c in comp) - 2)
    max_c = min(W, max(c for comp in comps for r, c in comp) + 3)
    
    print(f"  Bounding box: row {min_r}-{max_r}, col {min_c}-{max_c}")

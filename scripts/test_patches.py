import sys
import re

rules = {}
with open('state_color_rules.txt', 'r') as f:
    lines = f.readlines()
    
    current_state = None
    for line in lines:
        if line.startswith('State: '):
            current_state = line.split()[1]
            rules[current_state] = {'neighbors': [], 'edges': []}
        elif line.strip().startswith('Neighbor States:'):
            n_str = line.split(':', 1)[1].strip()
            if n_str:
                rules[current_state]['neighbors'] = [n.strip() for n in n_str.split(',')]
            else:
                rules[current_state]['neighbors'] = []

image_neighbors = {s: set(data['neighbors']) for s, data in rules.items()}
for s, ns in list(image_neighbors.items()):
    for n in ns:
        if s not in ['AK', 'HI'] and n not in ['AK', 'HI']:
            if n in image_neighbors:
                image_neighbors[n].add(s)

with open('make_map.py', 'r') as f: code = f.read()
m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
lines = [l.strip().strip('"').strip("'") for l in m.group(1).split(',\n')]
grid = [l.split() for l in lines]
H, W = len(grid), max(len(r) for r in grid)
for i in range(H): grid[i].extend(['..']*(W-len(grid[i])))

# Apply patches
# 1. Break IL-MI
grid[4][19] = 'IN'
# 2. Break MD-WV
grid[8][25] = 'PA'
# 3. Break MT-WA
grid[2][10] = 'ID'
# 4. Break UT-NM
grid[9][12] = 'AZ'

def check_grid(grid):
    states = set(c for r in grid for c in r if c != '..')
    
    neighbors = {s: set() for s in states}
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c == '..': continue
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < H and 0 <= nx < W:
                    nc = grid[ny][nx]
                    if nc != '..' and nc != c:
                        neighbors[c].add(nc)
                        
    errors = []
    
    # check disjoint components
    for s in states:
        cells = [(y, x) for y in range(H) for x in range(W) if grid[y][x] == s]
        if not cells: continue
        start = cells[0]
        q = [start]
        visited = {start}
        while q:
            cy, cx = q.pop(0)
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = cy+dy, cx+dx
                if 0 <= ny < H and 0 <= nx < W and grid[ny][nx] == s and (ny, nx) not in visited:
                    visited.add((ny, nx))
                    q.append((ny, nx))
        if len(visited) != len(cells):
            errors.append(f"ERROR {s} is DISCONNECTED.")

    for s in states:
        if s in ['AK', 'HI']: continue
        expected = image_neighbors.get(s, set())
        actual = neighbors[s]
        
        if expected != actual:
            added = actual - expected
            missing = expected - actual
            errors.append(f"ERROR {s}: Extra neighbors: {added}, Missing neighbors: {missing}")

    return errors

errors = check_grid(grid)
if errors:
    for e in errors: print(e)
else:
    print("SUCCESS: Patched grid matches user topological constraints PERFECTLY!")
    
    # save result to a file so we can run our standard pipeline
    with open('patched_base.txt', 'w') as f:
        f.write("\n".join(" ".join(r) for r in grid))

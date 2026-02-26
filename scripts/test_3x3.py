import sys
import re

rules = {}
with open('state_color_rules.txt', 'r') as f:
    lines = f.readlines()
    current_state = None
    for line in lines:
        if line.startswith('State: '):
            current_state = line.split()[1]
            rules[current_state] = {'neighbors': []}
        elif line.strip().startswith('Neighbor States:'):
            n_str = line.split(':', 1)[1].strip()
            if n_str:
                rules[current_state]['neighbors'] = [n.strip() for n in n_str.split(',')]

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
grid[4][19] = 'IN'  # Break IL-MI
grid[8][25] = 'PA'  # Break MD-WV
grid[2][10] = 'ID'  # Break MT-WA
grid[9][12] = 'AZ'  # Break UT-NM

# 1x grid checks done. Now Expand 3x3 and bridge
new_H, new_W = H * 3, W * 3
new_grid = [['..'] * new_W for _ in range(new_H)]

for r in range(H):
    for c in range(W):
        val = grid[r][c]
        if val == '..': continue
        for dr in range(3):
            for dc in range(3):
                new_grid[3*r + dr][3*c + dc] = val

for r in range(H - 1):
    for c in range(W - 1):
        val1 = grid[r][c]
        val2 = grid[r+1][c+1]
        val_tr = grid[r][c+1]
        val_bl = grid[r+1][c]
            
        if val1 == val2 and val1 != '..':
            if val_tr != val1 and val_bl != val1:
                new_grid[3*r+2][3*c+3] = val1
                new_grid[3*r+3][3*c+2] = val1
                
        if val_tr == val_bl and val_tr != '..':
            if val1 != val_tr and val2 != val_tr:
                new_grid[3*r+2][3*c+2] = val_tr
                new_grid[3*r+3][3*c+3] = val_tr

def check_grid(grid, H, W):
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
            errors.append(f"ERROR {s}: Extra: {added}, Missing: {missing}")

    return errors

errs = check_grid(new_grid, new_H, new_W)
if errs:
    for e in errs: print(e)
else:
    print("SUCCESS on 3x3 GRID! All constraints perfectly met.")
    with open('final_grid.py', 'w') as f:
        f.write('grid_lines = [\n')
        for r in grid:
            f.write(f'    "{" ".join(r)}",\n')
        f.write(']\n')


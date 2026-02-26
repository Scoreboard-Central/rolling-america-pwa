import sys
import re

with open('state_color_rules.txt', 'r') as f:
    lines = f.readlines()
    rules = {}
    for line in lines:
        if line.startswith('State: '):
            current_state = line.split()[1]
            rules[current_state] = []
        elif line.strip().startswith('Neighbor States:'):
            n_str = line.split(':', 1)[1].strip()
            if n_str:
                rules[current_state] = [n.strip() for n in n_str.split(',')]

image_neighbors = {s: set(rules[s]) for s in rules}
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

grid[4][19] = 'IN'  # Break IL-MI
grid[8][25] = 'PA'  # Break MD-WV
grid[2][10] = 'ID'  # Break MT-WA

# Fix NY-MI
grid[3][22] = '..'  # Was NY
grid[4][23] = '..'  # Was NY

# Fix NJ-NY-CT-DE logic
grid[6][25] = 'NJ'
grid[6][26] = 'NJ'
grid[6][27] = 'NJ'
grid[6][28] = 'NJ'
grid[6][29] = '..' # Clear old DE

# Fix RI-NH logic
grid[4][31] = '..'
grid[5][30] = 'RI'

# MD extra NC logic
grid[9][27] = '..' # Clear MD

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

states = set(c for r in new_grid for c in r if c != '..')
neighbors = {s: set() for s in states}
for y in range(new_H):
    for x in range(new_W):
        c = new_grid[y][x]
        if c == '..': continue
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < new_H and 0 <= nx < new_W:
                nc = new_grid[ny][nx]
                if nc != '..' and nc != c:
                    neighbors[c].add(nc)
errs = []
for s in states:
    expected = image_neighbors.get(s, set())
    actual = neighbors[s]
    if expected != actual:
        added = actual - expected
        missing = expected - actual
        errs.append(f"ERROR {s}: Extra: {added}, Missing: {missing}")

if errs:
    for e in errs: print(e)
else:
    print("SUCCESS on 3x3 GRID!")
    with open('final_grid.py', 'w') as f:
        f.write('grid_lines = [\n')
        for r in grid:
            f.write(f'    "{" ".join(r)}",\n')
        f.write(']\n')

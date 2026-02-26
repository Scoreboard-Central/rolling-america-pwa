import sys
import re

with open('make_map.py', 'r') as f: code = f.read()
grid_lines_str = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL).group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]

H, W = len(grid), max(len(r) for r in grid)

colors = {
    'AK': 'orange', 'HI': 'orange', 'WA': 'orange', 'OR': 'orange', 'ID': 'orange', 'UT': 'orange', 'AZ': 'orange', 'NV': 'orange', 'CA': 'orange',
    'MT': 'blue', 'ND': 'blue', 'SD': 'blue', 'MN': 'blue', 'IA': 'blue', 'WI': 'blue', 'IL': 'blue', 'IN': 'blue', 'MI': 'blue',
    'WY': 'green', 'NE': 'green', 'KS': 'green', 'CO': 'green', 'NM': 'green', 'OK': 'green', 'TX': 'green',
    'MO': 'yellow', 'AR': 'yellow', 'LA': 'yellow', 'AL': 'yellow', 'TN': 'yellow', 'MS': 'yellow', 'FL': 'yellow', 'KY': 'yellow',
    'DE': 'red', 'MD': 'red', 'PA': 'red', 'OH': 'red', 'WV': 'red', 'VA': 'red', 'NC': 'red', 'SC': 'red', 'GA': 'red',
    'ME': 'purple', 'NH': 'purple', 'VT': 'purple', 'NY': 'purple', 'MA': 'purple', 'RI': 'purple', 'CT': 'purple', 'NJ': 'purple',
}

states = set(c for r in grid for c in r if c != '..')

image_neighbors = {
    'WA': {'OR', 'ID', 'MT'}, 'OR': {'WA', 'ID', 'CA', 'NV'}, 'CA': {'OR', 'NV', 'AZ'},
    'NV': {'OR', 'ID', 'UT', 'CA', 'AZ'}, 'ID': {'WA', 'MT', 'OR', 'WY', 'NV', 'UT'},
    'UT': {'ID', 'WY', 'CO', 'NV', 'AZ', 'NM'}, 'AZ': {'NV', 'UT', 'CA', 'NM'},
    'MT': {'WA', 'ID', 'WY', 'ND', 'SD'}, 'WY': {'MT', 'ID', 'SD', 'NE', 'UT', 'CO'},
    'CO': {'WY', 'NE', 'KS', 'OK', 'UT', 'NM'}, 'NM': {'CO', 'OK', 'TX', 'UT', 'AZ'},
    'ND': {'MT', 'SD', 'MN'}, 'SD': {'ND', 'MT', 'WY', 'MN', 'IA', 'NE'},
    'NE': {'SD', 'WY', 'CO', 'IA', 'MO', 'KS'}, 'KS': {'NE', 'CO', 'OK', 'MO'},
    'OK': {'KS', 'CO', 'NM', 'MO', 'AR', 'TX'}, 'TX': {'OK', 'NM', 'AR', 'LA'},
    'MN': {'ND', 'SD', 'IA', 'WI'}, 'IA': {'MN', 'SD', 'NE', 'WI', 'IL', 'MO'},
    'MO': {'IA', 'NE', 'KS', 'OK', 'AR', 'IL', 'KY', 'TN'}, 'AR': {'MO', 'OK', 'TX', 'TN', 'MS', 'LA'},
    'LA': {'AR', 'TX', 'MS'}, 'WI': {'MN', 'IA', 'IL', 'MI'},
    'IL': {'WI', 'IA', 'MO', 'MI', 'IN', 'KY'}, 'MI': {'WI', 'IL', 'IN', 'OH'},
    'IN': {'MI', 'IL', 'OH', 'KY'}, 'OH': {'MI', 'IN', 'PA', 'WV', 'KY'},
    'KY': {'IN', 'OH', 'WV', 'VA', 'IL', 'MO', 'TN'}, 'TN': {'KY', 'VA', 'NC', 'MO', 'AR', 'MS', 'AL', 'GA'},
    'MS': {'TN', 'AR', 'LA', 'AL'}, 'AL': {'TN', 'MS', 'GA', 'FL'}, 'FL': {'AL', 'GA'},
    'PA': {'NY', 'NJ', 'OH', 'WV', 'MD', 'DE'}, 'WV': {'OH', 'PA', 'MD', 'VA', 'KY'},
    'VA': {'MD', 'WV', 'KY', 'TN', 'NC'}, 'NC': {'VA', 'TN', 'GA', 'SC'}, 'SC': {'NC', 'GA'},
    'GA': {'NC', 'SC', 'TN', 'AL', 'FL'}, 'NY': {'VT', 'MA', 'CT', 'NJ', 'PA'},
    'NJ': {'NY', 'PA', 'DE'}, 'DE': {'NJ', 'PA', 'MD'}, 'MD': {'PA', 'DE', 'WV', 'VA'},
    'CT': {'MA', 'RI', 'NY'}, 'RI': {'MA', 'CT'}, 'MA': {'NH', 'VT', 'NY', 'CT', 'RI'},
    'VT': {'NH', 'MA', 'NY'}, 'NH': {'ME', 'VT', 'MA'}, 'ME': {'NH'},
}

# Add symmetric links
for s, neighs in list(image_neighbors.items()):
    for n in neighs:
        if s not in ['AK', 'HI'] and n not in ['AK', 'HI']:
            image_neighbors[n].add(s)

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
    if s in ['AK', 'HI']: continue
    expected = image_neighbors.get(s, set())
    actual = neighbors[s]
    def color_counts(n_set):
        cts = {}
        for n in n_set:
            c = colors[n]
            cts[c] = cts.get(c, 0) + 1
        return cts
    exp_c = color_counts(expected)
    act_c = color_counts(actual)
    if exp_c != act_c:
        errors.append(f"ERROR {s}: Expected {exp_c}, but got {act_c}. Expected {expected}, got {actual}")

def is_connected(s):
    cells = [(x, y) for y in range(H) for x in range(W) if grid[y][x] == s]
    if not cells: return True
    start = cells[0]
    visited = set([start])
    stack = [start]
    while stack:
        cx, cy = stack.pop()
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = cy+dy, cx+dx
            if (nx, ny) in cells and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append((nx, ny))
    return len(visited) == len(cells)

for s in states:
    if not is_connected(s):
        errors.append(f"ERROR: State {s} is not orthogonally connected.")

if not errors:
    print("SUCCESS: Target grid perfectly satisfies all state rules and continuity!")
else:
    for err in errors:
        print(err)

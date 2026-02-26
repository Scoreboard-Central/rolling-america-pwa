import re

with open('make_map.py', 'r') as f: code = f.read()

m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
grid_lines_str = m.group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]

H, W = len(grid), max(len(r) for r in grid)
for i in range(H):
    grid[i].extend(['..'] * (W - len(grid[i])))

colors = {
    'AK': 'orange', 'HI': 'orange', 'WA': 'orange', 'OR': 'orange', 'ID': 'orange', 'UT': 'orange', 'AZ': 'orange', 'NV': 'orange', 'CA': 'orange',
    'MT': 'blue', 'ND': 'blue', 'SD': 'blue', 'MN': 'blue', 'IA': 'blue', 'WI': 'blue', 'IL': 'blue', 'IN': 'blue', 'MI': 'blue',
    'WY': 'green', 'NE': 'green', 'KS': 'green', 'CO': 'green', 'NM': 'green', 'OK': 'green', 'TX': 'green',
    'MO': 'yellow', 'AR': 'yellow', 'LA': 'yellow', 'AL': 'yellow', 'TN': 'yellow', 'MS': 'yellow', 'FL': 'yellow', 'KY': 'yellow',
    'DE': 'red', 'MD': 'red', 'PA': 'red', 'OH': 'red', 'WV': 'red', 'VA': 'red', 'NC': 'red', 'SC': 'red', 'GA': 'red',
    'ME': 'purple', 'NH': 'purple', 'VT': 'purple', 'NY': 'purple', 'MA': 'purple', 'RI': 'purple', 'CT': 'purple', 'NJ': 'purple',
}

states = set(c for r in grid for c in r if c != '..')

neighbors = {s: set() for s in states}
for y in range(H):
    for x in range(W):
        c = grid[y][x]
        if c == '..': continue
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < H and 0 <= nx < W:
                nc = grid[ny][nx]
                if nc != '..' and nc != c:
                    neighbors[c].add(nc)

# Output rules
with open('state_color_rules.txt', 'w') as f:
    f.write("Rolling America - State Neighbor Color Rules\n")
    f.write("============================================\n\n")
    for state in sorted(list(states)):
        if state in ['AK', 'HI']: continue
        my_color = colors[state]
        f.write(f"State: {state} ({my_color})\n")
        
        neigh_colors = {}
        for n in neighbors[state]:
            c = colors[n]
            neigh_colors[c] = neigh_colors.get(c, 0) + 1
            
        f.write(f"  Total Neighbors: {len(neighbors[state])}\n")
        f.write(f"  Neighbor States: {', '.join(sorted(list(neighbors[state])))}\n")
        f.write(f"  Neighbor Colors:\n")
        for color in ['orange', 'blue', 'green', 'yellow', 'red', 'purple']:
            if color in neigh_colors:
                f.write(f"    - {color}: {neigh_colors[color]}\n")
        f.write("\n")

print("Generated state_color_rules.txt")

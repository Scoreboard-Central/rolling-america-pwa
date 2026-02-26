import sys

with open('grid.txt', 'r') as f:
    grid_str = f.read()

colors = {
    'AK': 'ra-orange', 'HI': 'ra-orange', 'WA': 'ra-orange', 'OR': 'ra-orange', 'ID': 'ra-orange', 'UT': 'ra-orange', 'AZ': 'ra-orange', 'NV': 'ra-orange', 'CA': 'ra-orange',
    'MT': 'ra-blue', 'ND': 'ra-blue', 'SD': 'ra-blue', 'MN': 'ra-blue', 'IA': 'ra-blue', 'WI': 'ra-blue', 'IL': 'ra-blue', 'IN': 'ra-blue', 'MI': 'ra-blue',
    'WY': 'ra-green', 'NE': 'ra-green', 'KS': 'ra-green', 'CO': 'ra-green', 'NM': 'ra-green', 'OK': 'ra-green', 'TX': 'ra-green',
    'MO': 'ra-yellow', 'AR': 'ra-yellow', 'LA': 'ra-yellow', 'AL': 'ra-yellow', 'TN': 'ra-yellow', 'MS': 'ra-yellow', 'FL': 'ra-yellow', 'KY': 'ra-yellow',
    'DE': 'ra-red', 'MD': 'ra-red', 'PA': 'ra-red', 'OH': 'ra-red', 'WV': 'ra-red', 'VA': 'ra-red', 'NC': 'ra-red', 'SC': 'ra-red', 'GA': 'ra-red',
    'ME': 'ra-purple', 'NH': 'ra-purple', 'VT': 'ra-purple', 'NY': 'ra-purple', 'MA': 'ra-purple', 'RI': 'ra-purple', 'CT': 'ra-purple', 'NJ': 'ra-purple',
}

lines = [l.strip().split() for l in grid_str.strip().split('\n') if l.strip()]
W = max(len(row) for row in lines)
H = len(lines)

grid = []
for row in lines:
    grid.append(row + ['..'] * (W - len(row)))

neighbors = {}
states = set(c for r in grid for c in r if c != '..')
for s in states:
    neighbors[s] = set()

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
                    
def check():
    errors = []
    
    # Check GA constraints
    ga_neighbors = neighbors.get('GA', set())
    ga_yellows = [n for n in ga_neighbors if colors[n] == 'ra-yellow']
    ga_reds = [n for n in ga_neighbors if colors[n] == 'ra-red']
    
    if set(ga_yellows) != {'TN', 'MS', 'FL'}:
        errors.append(f"GA yellow neighbors wrong: {ga_yellows}")
    if set(ga_reds) != {'SC', 'NC'}:
        errors.append(f"GA red neighbors wrong: {ga_reds}")

    # Check state shapes (connected components)
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
            errors.append(f"State {s} is not connected.")

    if not errors:
        print("All checks passed!")
    else:
        for err in errors:
            print("ERROR:", err)

if __name__ == '__main__':
    check()

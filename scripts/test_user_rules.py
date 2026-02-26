import sys

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

def check_grid(grid_str):
    lines = [l.strip().split() for l in grid_str.strip().split('\n') if l.strip()]
    W = max(len(l) for l in lines)
    H = len(lines)
    grid = [r + ['..']*(W-len(r)) for r in lines]
    
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
            errors.append(f"ERROR {s} is DISCONNECTED. Found {len(cells)} cells but only {len(visited)} connected.")

    for s in states:
        if s in ['AK', 'HI']: continue
        expected = image_neighbors.get(s, set())
        actual = neighbors[s]
        
        if expected != actual:
            added = actual - expected
            missing = expected - actual
            errors.append(f"ERROR {s}: Extra neighbors: {added}, Missing neighbors: {missing}")

    return errors

grid = [
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. .. .. WA ID MT MT ND MN WI MI .. .. .. .. .. .. VT NH NH ME ME ..",
    ".. .. .. OR WA ID MT MT ND MN WI MI .. .. .. .. .. .. VT MA MA .. .. ..",
    ".. .. .. OR ID ID WY WY SD SD IA IL IN OH PA PA NY NY NY MA CT RI .. ..",
    ".. CA CA NV ID WY WY NE IA IA IL IN OH PA PA NJ NY CT CT CT .. .. .. ..",
    ".. CA CA NV NV UT CO NE KS MO IL KY WV MD DE DE .. .. .. .. .. .. .. ..",
    ".. HI HI .. AZ UT CO KS MO MO KY WV VA VA .. .. .. .. .. .. .. .. .. ..",
    ".. .. .. .. AZ NM OK OK AR TN TN NC NC .. .. .. .. .. .. .. .. .. .. ..",
    ".. .. .. .. .. NM TX AR AR MS AL GA SC SC .. .. .. .. .. .. .. .. .. ..",
    ".. .. .. .. .. TX TX LA MS AL GA GA .. .. .. .. .. .. .. .. .. .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. FL FL .. .. .. .. .. .. .. .. .. .. .."
]

errors = check_grid("\n".join(grid))
if errors:
    for e in errors: print(e)
else:
    print("SUCCESS: Grid matches all user topology rules perfectly!")

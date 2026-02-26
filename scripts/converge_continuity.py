import re
import heapq

with open('make_map.py', 'r') as f: code = f.read()
m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
grid_lines_str = m.group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]
H, W = len(grid), len(grid[0])

try:
    from build_strict_grid import image_neighbors as valid_neighbors
except:
    valid_neighbors = {}

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

def find_path(state, comp0, comp1):
    pq = []
    visited = {}
    valid_ns = valid_neighbors.get(state, set())
    
    for r, c in comp0:
        heapq.heappush(pq, (0, r, c))
        visited[(r, c)] = (0, None)
        
    target_cell = None
    while pq:
        cost, r, c = heapq.heappop(pq)
        
        if (r, c) in comp1:
            target_cell = (r, c)
            break
            
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < H and 0 <= nc < W:
                cell_state = grid[nr][nc]
                if cell_state == '..': step_cost = 1000
                elif cell_state == state: step_cost = 0
                elif cell_state in valid_ns: step_cost = 1
                else: step_cost = 500
                    
                new_cost = cost + step_cost
                if (nr, nc) not in visited or new_cost < visited[(nr, nc)][0]:
                    visited[(nr, nc)] = (new_cost, (r, c))
                    heapq.heappush(pq, (new_cost, nr, nc))
                    
    path = []
    if target_cell:
        curr = target_cell
        while visited[curr][1] is not None:
            curr = visited[curr][1]
            if curr not in comp0: path.append(curr)
    return path

states = set(c for r in grid for c in r if c != '..')

iterations = 0
while True:
    iterations += 1
    if iterations > 10:
        print("Max iterations reached!")
        break
        
    discon = []
    for s in states:
        comps = get_components(s)
        if len(comps) > 1:
            discon.append(s)
            
    if not discon:
        print("SUCCESS! Grid is 100% mathematically contiguous.")
        break
        
    print(f"Iteration {iterations}: Disconnected states: {discon}")
    for s in discon:
        comps = get_components(s)
        if len(comps) > 1:
            path = find_path(s, comps[0], comps[1])
            for r, c in path:
                grid[r][c] = s
            print(f"  Bridged {s} with {len(path)} cells.")

joined = ",\n    ".join('"' + " ".join(row) + '"' for row in grid)
new_code = code[:m.start(1)] + "\n    " + joined + "\n" + code[m.end(1):]
with open('make_map.py', 'w') as f: f.write(new_code)

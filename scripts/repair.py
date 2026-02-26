import re
import heapq

# 1. Start with the perfectly valid 1x grid
grid_lines = [
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. AK AK AK .. .. WA WA WA MT MT MT ND ND MN MN WI WI MI MI MI .. .. .. VT VT NH NH ME ME ..",
    ".. .. AK AK AK .. .. WA WA WA ID MT MT SD SD MN MN WI WI MI MI MI NY NY NY NY VT VT NH NH MA MA",
    ".. .. AK AK AK .. .. OR OR OR ID ID WY SD SD SD IA WI IL IL MI MI MI NY NY NY MA CT MA MA MA RI",
    ".. .. .. .. .. .. .. OR OR OR NV ID WY WY WY NE IA IA IL IL IN IN OH OH PA PA NJ NY CT CT CT RI",
    ".. .. .. .. .. .. .. CA CA NV NV UT WY WY CO NE NE MO IL IN OH OH PA PA PA PA DE DE DE DE .. ..",
    ".. .. .. .. .. .. .. CA CA NV NV UT UT CO CO CO KS KS MO IL KY OH OH WV PA PA MD MD DE DE .. ..",
    ".. .. HI HI HI .. .. CA CA AZ NV UT UT CO CO CO KS KS KS MO MO KY KY KY WV WV MD MD MD .. .. ..",
    ".. .. HI HI HI .. .. CA CA AZ AZ AZ NM NM NM OK OK OK MO MO KY KY VA VA VA VA MD MD .. .. .. ..",
    ".. .. .. .. .. .. .. CA CA AZ AZ AZ AZ NM NM TX TX OK OK AR TN MO TN TN TN NC VA NC NC NC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX AR AR MS MS AL GA GA GA SC SC SC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX LA LA MS MS AL AL GA GA GA GA SC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. LA LA LA LA LA MS MS AL AL AL FL FL FL .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL FL .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .."
]

max_w = max(len(l.split()) for l in grid_lines)
grid = []
for l in grid_lines:
    words = l.split()
    words.extend(['..'] * (max_w - len(words)))
    grid.append(words)

grid[6][20] = 'IN'
grid[6][19] = 'IL'

# 2. 3x3 expansion to safely add bridges without destroying any borders
H, W = len(grid), len(grid[0])
new_H, new_W = H * 3, W * 3
new_grid = [['..'] * new_W for _ in range(new_H)]

for r in range(H):
    for c in range(len(grid[r])):
        val = grid[r][c]
        if val == '..': continue
        for dr in range(3):
            for dc in range(3):
                new_grid[3*r + dr][3*c + dc] = val

# Safe Bridge logic for direct adjacent diagonals
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

# 3. Dijkstra Pathfinder for disconnected states
def get_neighbors(n_grid, r, c, state):
    ns = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(n_grid) and 0 <= nc < len(n_grid[0]) and n_grid[nr][nc] == state:
            ns.append((nr, nc))
    return ns

def get_components(n_grid, state):
    cells = [(r, c) for r in range(len(n_grid)) for c in range(len(n_grid[0])) if n_grid[r][c] == state]
    if not cells: return []
    unvisited = set(cells)
    components = []
    while unvisited:
        start = unvisited.pop()
        comp = set([start])
        queue = [start]
        while queue:
            curr = queue.pop(0)
            for n in get_neighbors(n_grid, curr[0], curr[1], state):
                if n in unvisited:
                    unvisited.remove(n)
                    comp.add(n)
                    queue.append(n)
        components.append(comp)
    return components

discon = ['NY', 'NC', 'MA', 'MO', 'TN']
for s in discon:
    comps = get_components(new_grid, s)
    if len(comps) > 1:
        # A simple BFS bridge through closest blocks
        pq = []
        visited = {}
        for r, c in comps[0]:
            heapq.heappush(pq, (0, r, c))
            visited[(r, c)] = (0, None)
            
        target_cell = None
        while pq:
            cost, r, c = heapq.heappop(pq)
            if (r, c) in comps[1]:
                target_cell = (r, c)
                break
                
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < new_H and 0 <= nc < new_W:
                    cell_state = new_grid[nr][nc]
                    step_cost = 1 if cell_state != s else 0
                    if cell_state == '..': step_cost += 1000  # Avoid void
                        
                    new_cost = cost + step_cost
                    if (nr, nc) not in visited or new_cost < visited[(nr, nc)][0]:
                        visited[(nr, nc)] = (new_cost, (r, c))
                        heapq.heappush(pq, (new_cost, nr, nc))
                        
        if target_cell:
            curr = target_cell
            while visited[curr][1] is not None:
                curr = visited[curr][1]
                if curr not in comps[0]:
                    new_grid[curr[0]][curr[1]] = s

grid_str = "\n".join(" ".join(row) for row in new_grid)

# Inject to generate_map.py
with open('generate_map.py', 'r') as f:
    gen_code = f.read()

# Make sure generate map parses the multi line correct
new_gen_code = re.sub(r'grid_str = """[\s\S]*?"""', f'grid_str = """\n{grid_str}\n"""', gen_code)
# make SIZE smaller so it fits
new_gen_code = new_gen_code.replace("SIZE = 34", "SIZE = 12")
with open('generate_map.py', 'w') as f:
    f.write(new_gen_code)

print("Repair complete! Ready to generate.")

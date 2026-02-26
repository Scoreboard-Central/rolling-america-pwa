with open("grid.txt") as f: lines = [l.strip().split() for l in f if l.strip()]
H, W = len(lines), len(lines[0])
def get_neighbors(r, c, state):
    ns = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # ORTHOGONAL ONLY
        nr, nc = r + dr, c + dc
        if 0 <= nr < H and 0 <= nc < len(lines[nr]) and lines[nr][nc] == state:
            ns.append((nr, nc))
    return ns

errors = False
for state in set(c for r in lines for c in r if c != '..'):
    cells = [(r, c) for r in range(H) for c in range(len(lines[r])) if lines[r][c] == state]
    if not cells: continue
    
    start = cells[0]
    visited = set([start])
    queue = [start]
    
    while queue:
        curr = queue.pop(0)
        for n in get_neighbors(curr[0], curr[1], state):
            if n not in visited:
                visited.add(n)
                queue.append(n)
                
    if len(visited) != len(cells):
        errors = True
        print(f"ERROR: State {state} is NOT orthogonally continuous!")

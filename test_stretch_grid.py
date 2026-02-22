import test_shape

grid_str = """
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. AK AK .. WA ID ID MT ND MN MN WI VT VT NH ME .. .. ..
.. AK AK .. OR ID UT SD SD SD IA WI NY MA MA .. .. .. ..
.. .. .. .. OR NV UT WY NE NE IL WI NY CT RI .. .. .. ..
.. .. .. .. CA NV AZ WY NE NE IN MI NJ CT CT OH PA DE ..
.. .. HI HI CA CA AZ CO CO KS IN MI NJ CT CT WV PA MD ..
.. .. .. .. CA CA AZ NM OK KS LA TN MS KY VA VA VA NC ..
.. .. .. .. CA CA AZ TX OK AR MO TN AL AL SC SC SC GA ..
.. .. .. .. .. .. .. TX TX AR AR AR AR AR SC GA GA GA ..
.. .. .. .. .. .. .. .. TX TX AR FL AR AR .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. AR FL FL .. .. .. .. .. ..
"""

target_adj = test_shape.target_adjacencies

def analyze(grid_str):
    lines = [l.strip().split() for l in grid_str.strip().split('\n')]
    grid = lines
    
    H = len(grid)
    W = max(len(r) for r in grid)
    for row in grid:
        row.extend(['..'] * (W - len(row)))
        
    adj = {s: set() for s in target_adj}
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c != '..':
                for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < H and 0 <= nx < W:
                        nc = grid[ny][nx]
                        if nc != '..' and nc != c:
                            adj[c].add(nc)
                            
    mismatches = 0
    for s, count in target_adj.items():
        if len(adj[s]) != count:
            print(f"{s} mismatches! Got {len(adj[s])} {list(adj[s])}, Want {count}.")
            mismatches += 1
    
    vis = set()
    states = set(c for r in grid for c in r if c != '..')
    for y in range(H):
        for x in range(W):
            if grid[y][x] != '..':
                vis.add(grid[y][x])
                
    empty_vis = set()
    def bfs(sy, sx):
        q = [(sy, sx)]
        empty_vis.add((sy, sx))
        while q:
            cy, cx = q.pop(0)
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = cy+dy, cx+dx
                if 0 <= ny < H and 0 <= nx < W:
                    if (ny, nx) not in empty_vis and grid[ny][nx] == '..':
                        empty_vis.add((ny, nx))
                        q.append((ny, nx))
                        
    holes = 0
    for y in range(H):
        for x in range(W):
            if grid[y][x] == '..' and (y, x) not in empty_vis:
                if y == 0 or y == H-1 or x == 0 or x == W-1:
                    bfs(y, x)
                else:
                    bfs(y, x)
                    holes += 1

    print(f"Holes: {holes}")
    if mismatches == 0 and holes == 0:
        print("PERFECT MATCH on layout!")
        return 0
    return mismatches

analyze(grid_str)

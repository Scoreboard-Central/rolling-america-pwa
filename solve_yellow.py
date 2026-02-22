import random

targets = {
    'MO': 3, 'AR': 4, 'LA': 2, 'AL': 4, 'TN': 5, 'MS': 3, 'FL': 1, 'KY': 2
}

# The space we have is roughly a 5x4 grid
# Florida is locked at the bottom right.
def analyze(grid):
    H = len(grid)
    W = len(grid[0])
    adj = {}
    for y in range(H):
        for x in range(W):
            s1 = grid[y][x]
            if s1 == '.': continue
            if s1 not in adj: adj[s1] = set()
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < W and 0 <= ny < H:
                    s2 = grid[ny][nx]
                    if s2 != '.' and s2 != s1:
                        adj[s1].add(s2)
    mismatches = 0
    for s, t in targets.items():
        got = len(adj.get(s, []))
        mismatches += abs(got - t)
        
    # Check contiguity
    for st in targets:
        cells = [(x,y) for y in range(H) for x in range(W) if grid[y][x] == st]
        if not cells: return 1000
        st_Q = [cells[0]]
        st_visited = {cells[0]}
        while st_Q:
            cx, cy = st_Q.pop(0)
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = cx+dx, cy+dy
                if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == st:
                    if (nx, ny) not in st_visited:
                        st_visited.add((nx, ny))
                        st_Q.append((nx, ny))
        if len(st_visited) != len(cells):
            mismatches += 5
            
    # Check for holes (isolated dots surrounded by non-dots)
    holes = 0
    for y in range(H):
        for x in range(W):
            if grid[y][x] == '.':
                surrounding = 0
                for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] != '.':
                        surrounding += 1
                if surrounding >= 3:
                    holes += 1
    mismatches += holes * 10
            
    return mismatches

def solve():
    states = list(targets.keys())
    grid_size = (5, 5)
    best_grid = [['.' for _ in range(grid_size[0])] for _ in range(grid_size[1])]
    
    # Fill random
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            best_grid[y][x] = random.choice(states)
            
    # Lock FL in bottom right
    # Row 3,4 x=2,3
    best_grid[3][2] = 'FL'
    best_grid[4][2] = 'FL'
    best_grid[4][3] = 'FL'
            
    best_score = analyze(best_grid)
    print("Initial:", best_score)
    
    for _ in range(300000):
        if best_score == 0: break
        
        new_grid = [row[:] for row in best_grid]
        
        # enforce shape
        for px, py in [(2,3), (2,4), (3,4)]:
            new_grid[py][px] = 'FL'
        
        # Don't let FL spread anywhere else
        for y in range(grid_size[1]):
            for x in range(grid_size[0]):
                if new_grid[y][x] == 'FL' and (x,y) not in [(2,3), (2,4), (3,4)]:
                    new_grid[y][x] = random.choice([s for s in states if s != 'FL'])
        
        if random.random() < 0.5:
            # Change
            x, y = random.randint(0, grid_size[0]-1), random.randint(0, grid_size[1]-1)
            if (x,y) not in [(2,3), (2,4), (3,4)]:
                new_grid[y][x] = random.choice(states + ['.'])
        else:
            # Swap
            x1, y1 = random.randint(0, grid_size[0]-1), random.randint(0, grid_size[1]-1)
            x2, y2 = random.randint(0, grid_size[0]-1), random.randint(0, grid_size[1]-1)
            if (x1,y1) not in [(2,3), (2,4), (3,4)] and (x2,y2) not in [(2,3), (2,4), (3,4)]:
                new_grid[y1][x1], new_grid[y2][x2] = new_grid[y2][x2], new_grid[y1][x1]
            
        score = analyze(new_grid)
        if score < best_score or (score == best_score and random.random() < 0.05):
            best_score = score
            best_grid = new_grid
            
    print("Final score:", best_score)
    for row in best_grid:
        print(" ".join(f"{c:2}" for c in row))

solve()

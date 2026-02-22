import random
import time

def evaluate(grid, targets):
    adj = {}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            s1 = grid[y][x]
            if s1 == '.': continue
            if s1 not in adj: adj[s1] = set()
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                    s2 = grid[ny][nx]
                    if s2 != '.' and s2 != s1:
                        adj[s1].add(s2)
    score = 0
    for s, t in targets.items():
        score += abs(len(adj.get(s, [])) - t)
    return score, adj

def solve(targets, grid_size=(5, 6), max_iters=50000):
    states = list(targets.keys())
    
    # We maintain a grid of strings, initially all '.'
    grid = [['.' for _ in range(grid_size[0])] for _ in range(grid_size[1])]
    
    # Place each state at least once
    available_cells = [(x,y) for y in range(grid_size[1]) for x in range(grid_size[0])]
    random.shuffle(available_cells)
    
    for i, s in enumerate(states):
        x, y = available_cells[i]
        grid[y][x] = s
        
    for i in range(len(states), len(available_cells)):
        x, y = available_cells[i]
        grid[y][x] = random.choice(states + ['.', '.'])
        
    best_score, _ = evaluate(grid, targets)
    best_grid = [row[:] for row in grid]
    
    for _ in range(max_iters):
        if best_score == 0:
            return best_grid
            
        # Copy best
        new_grid = [row[:] for row in best_grid]
        
        # Mutate
        x, y = random.randint(0, grid_size[0]-1), random.randint(0, grid_size[1]-1)
        
        # We can change it to any state or '.'
        # But ensure every state exists at least once!
        counts = {s: sum(r.count(s) for r in new_grid) for s in states}
        
        curr_val = new_grid[y][x]
        if curr_val in counts and counts[curr_val] <= 1:
            # Cannot mutate the last instance of a state
            pass
        else:
            new_grid[y][x] = random.choice(states + ['.', '.', '.'])
        
        # also try swapping
        x2, y2 = random.randint(0, grid_size[0]-1), random.randint(0, grid_size[1]-1)
        new_grid[y][x2], new_grid[y2][x] = new_grid[y2][x], new_grid[y][x2]
        
        score, _ = evaluate(new_grid, targets)
        if score <= best_score:
            best_score = score
            best_grid = new_grid
            
    return best_grid

targets = {'MO': 3, 'AR': 4, 'LA': 2, 'AL': 4, 'TN': 5, 'MS': 3, 'FL': 1, 'KY': 2}
best = solve(targets, (5, 6), 50000)
for r in best:
    print(" ".join(f"{c:2}" for c in r))
print("Score:", evaluate(best, targets))

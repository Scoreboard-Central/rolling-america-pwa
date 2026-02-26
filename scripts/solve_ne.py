import random
import copy

# Extract the region to solve
# R03-R08, col 23-31
# States involved: PA, NY, NJ, DE, CT, RI, MA, VT, NH, MD
targets = {
    'PA': {'NY', 'NJ', 'DE', 'MD', 'OH', 'WV', 'VA'}, # Note: OH, WV, VA are fixed on the left/bottom
    'NY': {'PA', 'NJ', 'CT', 'MA', 'VT'},
    'NJ': {'PA', 'NY', 'CT', 'DE'},
    'DE': {'PA', 'NJ', 'MD'},
    'CT': {'NY', 'NJ', 'MA', 'RI'},
    'RI': {'CT', 'MA'},
    'MA': {'NY', 'CT', 'RI', 'VT', 'NH'},
    'VT': {'NY', 'MA', 'NH'},
    'NH': {'VT', 'MA', 'ME'},
    'MD': {'PA', 'DE', 'WV', 'VA'}
}

fixed = {
    (3, 21): 'MI', (4, 21): 'MI', (4, 22): 'MI',
    (5, 23): 'PA', (5, 24): 'PA', (6, 23): 'PA', (6, 24): 'PA',
    (7, 23): 'WV', (7, 24): 'PA', (7, 25): 'PA',
    (8, 23): 'WV', (8, 24): 'WV', (8, 25): 'PA',
    (2, 29): 'ME', (2, 30): 'ME'
}

W = 8
H = 6
# Local offsets for the 6x8 grid starting at row 3, col 24
startY = 3
startX = 24

def evaluate(grid):
    score = 0
    adj = {s: set() for s in targets.keys()}
    
    for y in range(H):
        for x in range(W):
            s1 = grid[y][x]
            if s1 == '..': continue
            
            # Check neighbors
            for dy, dx in [(0,1), (1,0), (0,-1), (-1,0)]:
                ny, nx = y+dy, x+dx
                s2 = '..'
                if 0 <= ny < H and 0 <= nx < W:
                    s2 = grid[ny][nx]
                else:
                    absY, absX = startY + ny, startX + nx
                    if (absY, absX) in fixed:
                        s2 = fixed[(absY, absX)]
                        
                if s2 != '..' and s2 != s1:
                    if s1 in targets: adj[s1].add(s2)
                    if s2 in targets: adj[s2].add(s1)
                    
    # Must have exact matches for targets
    for s, expected in targets.items():
        if s == 'MD': continue # we just deal with NY, NJ, DE, CT, RI, MA, VT, NH
        if s not in adj:
            score += 10 # Missing state entirely
            continue
            
        actual = adj[s]
        score += len(expected - actual) * 10
        score += len(actual - expected) * 10
        
    return score

# Initial guess
grid = [
    ['NY', 'NY', 'VT', 'VT', 'NH', 'NH', '..', '..'], # R03
    ['NY', 'NY', 'VT', 'MA', 'MA', 'MA', 'MA', 'RI'], # R04
    ['NY', 'NY', 'NY', 'CT', 'CT', 'CT', 'RI', '..'], # R05
    ['NJ', 'DE', 'DE', 'DE', 'DE', '..', '..', '..'], # R06
    ['PA', 'DE', 'DE', 'DE', '..', '..', '..', '..'], # R07
    ['MD', 'MD', 'MD', '..', '..', '..', '..', '..'], # R08
]

states = ['NY', 'VT', 'NH', 'MA', 'RI', 'CT', 'NJ', 'DE', 'MD']

best_score = evaluate(grid)
best_grid = copy.deepcopy(grid)

iters = 100000
for i in range(iters):
    if best_score == 0: break
    
    new_grid = copy.deepcopy(best_grid)
    
    x1, y1 = random.randint(0, W-1), random.randint(0, H-1)
    
    if random.random() < 0.5:
        x2, y2 = random.randint(0, W-1), random.randint(0, H-1)
        new_grid[y1][x1], new_grid[y2][x2] = new_grid[y2][x2], new_grid[y1][x1]
    else:
        new_grid[y1][x1] = random.choice(states + ['..', '..'])
        
    # Validation: all states must be connected in new_grid!
    # simple connectedness test inside score helps
    
    score = evaluate(new_grid)
    
    # Add strong penalty for disconnected shapes
    for s in states:
        cells = [(y,x) for y in range(H) for x in range(W) if new_grid[y][x] == s]
        if not cells: 
            score += 1000
            continue
            
        visited = set()
        q = [cells[0]]
        visited.add(cells[0])
        while q:
            cy, cx = q.pop(0)
            for dy, dx in [(0,1), (1,0), (0,-1), (-1,0)]:
                ny, nx = cy+dy, cx+dx
                if 0 <= ny < H and 0 <= nx < W and new_grid[ny][nx] == s and (ny,nx) not in visited:
                    visited.add((ny,nx))
                    q.append((ny,nx))
        if len(visited) != len(cells):
            score += 500 # disconnected

    # Add shapes metric: a 1-length state looks bad.
    for s in states:
        cells = sum(row.count(s) for row in new_grid)
        if cells < 2: score += 5
        if cells > 6: score += 2
            
    if score <= best_score or random.random() < 0.001:
        best_score = score
        best_grid = new_grid

print(f"Best score: {best_score}")
for r in best_grid:
    print(" ".join(f"{c:2}" for c in r))


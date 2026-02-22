import random

grid_str = """
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
AK AK .. .. WA ID ID MT ND MN MN WI VT VT NH ME .. .. .. .. ..
AK AK .. .. OR ID UT SD SD SD IA WI NY MA MA .. .. .. .. .. ..
.. .. .. .. OR NV UT .. .. .. IL WI NY CT RI .. .. .. .. .. ..
HI HI .. .. CA NV AZ WY NE NE IN MI NJ CT .. OH PA DE .. .. ..
HI HI .. .. CA CA AZ CO CO KS .. .. .. .. .. WV PA MD .. .. ..
.. .. .. .. .. .. .. NM OK KS LA LA LA .. .. VA VA NC .. .. ..
.. .. .. .. .. .. .. TX OK OK MS .. AR AR MO SC SC GA .. .. ..
.. .. .. .. .. .. .. TX TX TX MS AL AR TN MO .. GA GA .. .. ..
.. .. .. .. .. .. .. .. .. .. TN AL TN TN KY .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. FL .. KY KY .. .. .. .. .. ..
"""

colors = {
    'AK': 'orange', 'HI': 'orange', 'WA': 'orange', 'OR': 'orange', 'ID': 'orange', 'UT': 'orange', 'AZ': 'orange', 'NV': 'orange', 'CA': 'orange',
    'MT': 'blue', 'ND': 'blue', 'SD': 'blue', 'MN': 'blue', 'IA': 'blue', 'WI': 'blue', 'IL': 'blue', 'IN': 'blue', 'MI': 'blue',
    'WY': 'green', 'NE': 'green', 'KS': 'green', 'CO': 'green', 'NM': 'green', 'OK': 'green', 'TX': 'green',
    'MO': 'yellow', 'AR': 'yellow', 'LA': 'yellow', 'AL': 'yellow', 'TN': 'yellow', 'MS': 'yellow', 'FL': 'yellow', 'KY': 'yellow',
    'ME': 'purple', 'NH': 'purple', 'VT': 'purple', 'NY': 'purple', 'MA': 'purple', 'RI': 'purple', 'CT': 'purple', 'NJ': 'purple',
    'DE': 'red', 'MD': 'red', 'PA': 'red', 'OH': 'red', 'WV': 'red', 'VA': 'red', 'NC': 'red', 'SC': 'red', 'GA': 'red'
}
targets = {
    'AK': 0, 'HI': 0, 'WA': 2, 'OR': 4, 'ID': 4, 'UT': 3, 'AZ': 3, 'NV': 5, 'CA': 3,
    'MT': 1, 'ND': 3, 'SD': 4, 'MN': 4, 'IA': 4, 'WI': 4, 'IL': 3, 'IN': 2, 'MI': 2,
    'WY': 2, 'NE': 3, 'KS': 3, 'CO': 5, 'NM': 3, 'OK': 4, 'TX': 2,
    'MO': 3, 'AR': 4, 'LA': 2, 'AL': 4, 'TN': 5, 'MS': 3, 'FL': 1, 'KY': 2,
    'ME': 1, 'NH': 3, 'VT': 3, 'NY': 4, 'MA': 5, 'RI': 2, 'CT': 4, 'NJ': 2,
    'DE': 2, 'MD': 3, 'PA': 5, 'OH': 2, 'WV': 3, 'VA': 4, 'NC': 3, 'SC': 2, 'GA': 2
}

def analyze(grid):
    adj = {}
    H = len(grid)
    W = len(grid[0])
    for y in range(H):
        for x in range(W):
            s1 = grid[y][x]
            if s1 == '..': continue
            if s1 not in adj: adj[s1] = set()
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < W and 0 <= ny < H:
                    s2 = grid[ny][nx]
                    if s2 != '..' and s2 != s1:
                        adj[s1].add(s2)
    mismatches = 0
    for s in targets:
        if s not in adj:
            mismatches += 10
            continue
        c = colors[s]
        same_col = [n for n in adj[s] if colors.get(n) == c]
        if s == 'MT': continue
        if len(same_col) != targets[s]:
            mismatches += abs(len(same_col) - targets[s])
    
    # Check for interior holes (dots entirely surrounded by non-dots, or just count dots not on the boundary)
    holes = 0
    for y in range(H):
        for x in range(W):
            if grid[y][x] == '..':
                # Just checking if there are ANY non-boundary '..' inside the main bounding box
                # that would look like a gap. Let's just count all dots between leftmost and rightmost state in that row
                row = grid[y]
                states_in_row = [i for i, v in enumerate(row) if v != '..']
                if states_in_row:
                    first = states_in_row[0]
                    last = states_in_row[-1]
                    if first < x < last:
                        holes += 1
                        
    return mismatches * 1000 + holes

def solve():
    lines = [l.strip().split() for l in grid_str.strip().split('\n') if l.strip()]
    H = len(lines)
    W = max(len(row) for row in lines)
    best_grid = [row + ['..'] * (W - len(row)) for row in lines]
    
    best_score = analyze(best_grid)
    print("Initial score:", best_score)
    
    if best_score == 0:
        return best_grid
        
    for _ in range(50000):
        new_grid = [row[:] for row in best_grid]
        
        # Mutate: pick a random hole or state
        y = random.randint(0, H-1)
        x = random.randint(0, W-1)
        
        # find neighbors
        neighbors = []
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < W and 0 <= ny < H:
                if new_grid[ny][nx] != '..':
                    neighbors.append(new_grid[ny][nx])
        
        if neighbors:
            new_grid[y][x] = random.choice(neighbors + ['..'])
        else:
            continue
            
        score = analyze(new_grid)
        if score < best_score or (score == best_score and random.random() < 0.1):
            best_score = score
            best_grid = new_grid
            
        if best_score == 0:
            break
            
    print("Final score:", best_score)
    for row in best_grid:
        print(" ".join(f"{c:2}" for c in row))
    return best_grid

solve()

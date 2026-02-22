grid_str = """
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..
.. AK AK .. WA ID ID MT ND MN MN WI NY VT VT NH ME ME ..
.. AK AK .. OR ID UT SD SD SD IA WI NY VT VT NH NH .. ..
.. .. .. .. OR NV UT WY NE NE IL WI NY MA MA MA MA .. ..
.. .. .. .. CA NV AZ WY NE NE IN MI NY CT CT CT RI .. ..
.. HI HI .. CA CA AZ CO CO KS IN MI NJ CT OH PA DE .. ..
.. .. .. .. CA CA AZ NM OK KS LA TN MS KY WV PA MD .. ..
.. .. .. .. CA CA AZ TX OK AR MO TN AL AL VA VA NC .. ..
.. .. .. .. .. .. .. TX TX AR AR AR AR AR SC SC GA GA ..
.. .. .. .. .. .. .. TX TX AR FL AR AR .. .. .. GA ..
.. .. .. .. .. .. .. .. .. .. AR FL FL .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
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

def analyze(grid_str):
    lines = [l.strip().split() for l in grid_str.strip().split('\n') if l.strip()]
    H = len(lines)
    W = max(len(r) for r in lines)
    grid = [row + ['..'] * (W - len(row)) for row in lines]

    adj = {}
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
    for s in sorted(adj.keys()):
        if s not in colors: continue
        if s == 'MT': continue
        c = colors[s]
        same_col = [n for n in adj[s] if colors.get(n) == c]
        if len(same_col) != targets.get(s, 0):
            mismatches += 1
            print(f"{s} mismatches! Got {len(same_col)} {same_col}, Want {targets.get(s, 0)}.")
    if mismatches == 0:
        print("PERFECT MATCH")

analyze(grid_str)

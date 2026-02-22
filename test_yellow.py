import sys

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
    'MO': 'yellow', 'AR': 'yellow', 'LA': 'yellow', 'AL': 'yellow', 'TN': 'yellow', 'MS': 'yellow', 'FL': 'yellow', 'KY': 'yellow',
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
    for s in sorted(adj.keys()):
        if s not in colors: continue
        c = colors[s]
        same_col = [n for n in adj[s] if colors.get(n) == c]
        print(f"{s} touches ({len(same_col)}): {same_col}")

analyze(grid_str)

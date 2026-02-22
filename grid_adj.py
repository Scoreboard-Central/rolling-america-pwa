grid_str = """
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. AK AK .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME
.. .. AK AK .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. VT NH ME
.. .. .. .. WA WA ID MT MT ND ND MN .. .. .. .. .. .. NY NY MA MA
.. .. .. .. OR OR ID MT MT SD SD MN WI WI MI MI .. .. PA PA CT RI
.. .. .. .. CA NV UT WY WY NE NE IA IL IL IN OH OH .. WV MD NJ ..
.. .. .. .. CA AZ UT CO CO KS KS MO IL IL IN OH OH VA VA DE .. ..
.. HI HI .. .. .. .. NM NM OK OK AR KY KY KY KY NC NC NC .. .. ..
.. .. .. .. .. .. .. .. TX TX TX LA TN TN TN TN SC SC .. .. .. ..
.. .. .. .. .. .. .. .. TX TX TX LA MS AL GA GA GA .. .. .. .. ..
.. .. .. .. .. .. .. .. .. TX TX .. MS AL FL FL .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. FL .. .. .. .. .. .. ..
"""
lines = [l.strip().split() for l in grid_str.strip().split('\n') if l.strip()]
H = len(lines)
W = max(len(row) for row in lines)
grid = []
for row in lines:
    grid.append(row + ['..'] * (W - len(row)))

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
    print(f"{s}: {', '.join(sorted(adj[s]))}")

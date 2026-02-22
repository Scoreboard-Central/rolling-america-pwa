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

colors = {
    'AK': 'orange', 'HI': 'orange', 'WA': 'orange', 'OR': 'orange', 'ID': 'orange', 'UT': 'orange', 'AZ': 'orange', 'NV': 'orange', 'CA': 'orange',
    'MT': 'blue', 'ND': 'blue', 'SD': 'blue', 'MN': 'blue', 'IA': 'blue', 'WI': 'blue', 'IL': 'blue', 'IN': 'blue', 'MI': 'blue',
    'WY': 'green', 'NE': 'green', 'KS': 'green', 'CO': 'green', 'NM': 'green', 'OK': 'green', 'TX': 'green', # Assumed NM instead of Arizona
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

print(f"{'State':<5} | {'Got':<5} | {'Target':<6} | {'Status'}")
print("-" * 35)
for s in sorted(adj.keys()):
    if s not in colors:
        print(f"Unknown state {s}")
        continue
    c = colors[s]
    same_color_neighbors = [n for n in adj[s] if colors.get(n) == c]
    count = len(same_color_neighbors)
    target = targets[s]
    status = "OK" if count == target else "MISMATCH"
    print(f"{s:<5} | {count:<5} | {target:<6} | {status} (Neighbors: {','.join(same_color_neighbors)})")


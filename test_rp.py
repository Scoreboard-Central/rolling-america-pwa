def analyze_sub(grid, targets):
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
    mismatches = 0
    for s, tgt in targets.items():
        got = len(adj.get(s, []))
        if got != tgt:
            print(f"  {s} got {got}, want {tgt}. Neighbors: {adj.get(s,[])}")
            mismatches += 1
    if mismatches == 0:
        print("PERFECT")
    return mismatches

purple_targets = {'ME': 1, 'NH': 3, 'VT': 3, 'NY': 4, 'MA': 5, 'RI': 2, 'CT': 4, 'NJ': 2}
purple_grid = [
    ["ME", ".",  ".",  "."],
    ["NH", "MA", "MA", "MA"],
    ["VT", "NY", "CT", "RI"],
    ["NJ", "NY", "CT", "RI"],
    ["NJ", ".",  ".",  "."]
]

print("Purple:")
analyze_sub(purple_grid, purple_targets)

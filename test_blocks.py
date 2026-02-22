import sys

def analyze_sub(grid, targets, color_name):
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
        if s == 'MT': continue  # known mathematical adjustment
        if got != tgt:
            print(f"{color_name} {s} got {got}, want {tgt}. Neighbors: {adj.get(s,[])}")
            mismatches += 1
    if mismatches == 0:
        print(f"{color_name} is PERFECT!")
    return mismatches

green_t = {'WY': 2, 'NE': 3, 'KS': 3, 'CO': 5, 'NM': 3, 'OK': 4, 'TX': 2}
green_g = [
    ["WY", "NE", "NE"],
    ["CO", "CO", "KS"],
    ["NM", "OK", "KS"],
    ["TX", "OK", "OK"],
    ["TX", "TX", "TX"]
]

purple_t = {'ME': 1, 'NH': 3, 'VT': 3, 'NY': 4, 'MA': 5, 'RI': 2, 'CT': 4, 'NJ': 2}
purple_g = [
    ["VT", "VT", "NH", "ME"],
    ["NY", "MA", "MA", "."],
    ["NY", "CT", "RI", "."],
    ["NJ", "CT", ".",  "."]
]

analyze_sub(green_g, green_t, "Green")
analyze_sub(purple_g, purple_t, "Purple")

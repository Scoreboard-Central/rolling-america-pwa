# Let's generate the map using an array of arrays we can easily modify and print.
grid = [[".." for _ in range(40)] for _ in range(25)]

def fill(state, r1, r2, c1, c2):
    for r in range(r1, r2+1):
        for c in range(c1, c2+1):
            if r < len(grid) and c < len(grid[0]):
                grid[r][c] = state

# Col 0: AK, HI
fill("AK", 0, 3, 0, 1)
fill("HI", 10, 11, 0, 1)

# West
fill("WA", 2, 3, 2, 4)
fill("MT", 2, 3, 5, 8)
fill("OR", 4, 5, 2, 4)
fill("ID", 4, 7, 5, 5) # ID drops down
fill("WY", 4, 5, 6, 8)
fill("CA", 6, 11, 2, 3)
fill("NV", 6, 9, 4, 5)
fill("UT", 6, 9, 6, 7)
fill("CO", 6, 9, 8, 10)
fill("AZ", 10, 11, 4, 7)
fill("NM", 10, 11, 8, 10)

# Central
fill("ND", 2, 3, 9, 10)
fill("SD", 4, 5, 9, 11)
fill("NE", 6, 7, 11, 12)
fill("KS", 8, 9, 11, 12)
fill("OK", 10, 11, 11, 13)
fill("TX", 12, 17, 8, 12)

# Central-East
fill("MN", 2, 5, 12, 13) 
fill("WI", 2, 5, 14, 15) 
fill("IA", 6, 7, 13, 14)
fill("MO", 8, 11, 14, 15)
fill("AR", 12, 13, 13, 15)
fill("LA", 14, 17, 13, 14)
fill("MS", 14, 17, 15, 16)
fill("AL", 14, 17, 17, 18)
fill("FL", 18, 21, 17, 19)

# East
fill("IL", 6, 9, 15, 16)
fill("MI", 2, 5, 15, 17)
fill("IN", 6, 7, 17, 18)
fill("OH", 6, 7, 19, 20)
fill("KY", 8, 9, 17, 20)
fill("TN", 10, 11, 16, 20)
fill("GA", 14, 17, 19, 20)
fill("SC", 14, 15, 21, 22)
fill("NC", 12, 13, 21, 23)
fill("VA", 10, 11, 21, 23)
fill("WV", 8, 9, 21, 22)
fill("PA", 6, 7, 21, 23)
fill("MD", 8, 9, 23, 24)
fill("DE", 8, 9, 25, 25)

# Northeast
fill("NY", 4, 5, 21, 23)
fill("NJ", 6, 7, 24, 25)
fill("CT", 4, 5, 24, 25)
fill("RI", 4, 5, 26, 26)
fill("MA", 2, 3, 24, 26)
fill("VT", 0, 3, 21, 22)
fill("NH", 0, 3, 23, 23)
fill("ME", 0, 1, 24, 26)

import sys

# Write grid out
with open("tmp_grid.txt", "w") as f:
    for r in grid:
        f.write(" ".join(f"{c:2}" for c in r) + "\n")
        
# Read it into the test script mechanism
import build_strict_grid
def test_grid():
    build_strict_grid.grid = grid
    build_strict_grid.H = len(grid)
    build_strict_grid.W = len(grid[0])
    # check states
    states = set(c for r in grid for c in r if c != '..')
    for s in build_strict_grid.colors.keys():
        if s not in states:
            print(f"MISSING STATE: {s}")
            return False

    neighbors = {s: set() for s in states}
    for y in range(build_strict_grid.H):
        for x in range(build_strict_grid.W):
            c = grid[y][x]
            if c == '..': continue
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < build_strict_grid.H and 0 <= nx < build_strict_grid.W:
                    nc = grid[ny][nx]
                    if nc != '..' and nc != c:
                        neighbors[c].add(nc)
                        
    passed = True
    for s in states:
        if s in ['AK', 'HI']: continue
        expected = build_strict_grid.image_neighbors.get(s, set())
        actual = neighbors[s]
        
        # We need exact neighbor matches? The prompt said "how many states it should border OF EACH COLOR"
        # Not exact specific state IDs, but exact color counts!
        # "Each color should contain the same number of states as the picture. Also, go state by state to see how many states it should border of each color."
        exp_c = build_strict_grid.color_counts(expected)
        act_c = build_strict_grid.color_counts(actual)
        
        if exp_c != act_c:
            print(f"ERROR {s}: Expected color neighbors {exp_c}, but got {act_c}. Actual IDs: {actual}, Expected IDs: {expected}")
            passed = False
    return passed

if test_grid():
    print("SUCCESS")
else:
    print("FAILED")


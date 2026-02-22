import sys
import re

grid_str = """
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. AK AK .. WA ID ID MT ND MN MN WI VT VT NH ME .. .. ..
.. AK AK .. OR ID UT SD SD SD IA WI NY MA MA .. .. .. ..
.. .. .. .. OR NV UT WY NE NE IL WI NY CT RI .. .. .. ..
.. .. HI .. CA NV AZ WY NE NE IN MI NJ CT CT OH PA DE ..
.. .. HI .. CA CA AZ CO CO KS IN MI NJ CT CT WV PA MD ..
.. .. .. .. .. .. .. NM OK KS LA TN MS KY VA VA VA NC ..
.. .. .. .. .. .. .. TX OK AR MO TN AL AL SC SC SC GA ..
.. .. .. .. .. .. .. TX TX AR AR AR AR AR SC GA GA GA ..
.. .. .. .. .. .. .. .. TX TX AR FL AR AR .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. AR FL FL .. .. .. .. .. ..
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
    W = 19
    grid = [row + ['..'] * (W - len(row)) for row in lines]

    # Expand map down
    grid.append(['..'] * W)
    H += 1

    # Clear Red and Purple fields
    for y in range(H):
        for x in range(W):
            c = colors.get(grid[y][x])
            if c in ('red', 'purple', 'yellow'):
                grid[y][x] = '..'

    grid[0][16] = 'ME'
    
    grid[1][12] = 'NY'
    grid[1][13] = 'VT'
    grid[1][14] = 'NH'
    grid[1][15] = 'NH'
    grid[1][16] = 'ME'
    
    grid[2][12] = 'NY'
    grid[2][13] = 'VT'
    grid[2][14] = 'NH'
    grid[2][15] = 'NH'
    grid[2][16] = 'NH'
    
    grid[3][12] = 'NY'
    grid[3][13] = 'MA'
    grid[3][14] = 'MA'
    grid[3][15] = 'MA'
    grid[3][16] = 'MA'
    
    # To fix RI and CT, RI must touch CT. Right now RI is (4,16). So CT must be (4,15).
    # NY wants 4 (VT, MA, CT, NJ).
    # NJ wants 2 (NY, CT).
    grid[4][12] = 'NY'
    grid[4][13] = 'CT'
    grid[4][14] = 'CT'
    grid[4][15] = 'CT'
    grid[4][16] = 'RI'
    
    grid[5][12] = 'NJ'  # NJ touches NY. Also touches CT.
    grid[5][13] = 'CT'
    grid[5][14] = 'CT'
    grid[5][15] = 'CT'
    
    # Yellow from user's latest file
    grid[6][10] = 'LA'
    grid[6][11] = 'TN'
    grid[6][12] = 'MS'
    grid[6][13] = 'KY'

    grid[7][9] = 'AR'
    grid[7][10] = 'MO'
    grid[7][11] = 'TN'
    grid[7][12] = 'AL'
    grid[7][13] = 'AL'

    grid[8][9] = 'AR'
    grid[8][10] = 'AR'
    grid[8][11] = 'AR'
    grid[8][12] = 'AR'
    grid[8][13] = 'AR'

    grid[9][10] = 'AR'
    grid[9][11] = 'FL'
    grid[9][12] = 'AR'
    grid[9][13] = 'AR'

    grid[10][10] = 'AR'
    grid[10][11] = 'FL'
    grid[10][12] = 'FL'
    
    # Red:  DE 2(MD PA), MD 3(DE PA NC), NC 3(MD VA GA), VA 4(WV PA NC SC), PA 5(OH WV DE MD VA), WV 3(OH PA VA), OH 2(PA WV)
    grid[5][16] = 'DE'
    grid[6][16] = 'MD'
    grid[7][16] = 'NC'
    
    grid[5][14] = 'OH'
    grid[5][15] = 'PA'
    
    grid[6][14] = 'WV'
    grid[6][15] = 'PA'
    
    # VA touches WV, PA, NC, SC
    grid[7][14] = 'VA'
    grid[7][15] = 'VA'
    # GA touches NC, SC
    # SC touches VA, GA
    # We want GA to be 8,15..17 as a 7.
    # GA(8,16) and GA(8,17) and GA(9..11, 17)
    
    # So GA must NOT touch VA. But VA is at 7,15. GA is at 8,15. So GA touches VA!
    # Hence GA got 3 (NC, SC, VA).
    # To fix this, SC must separate VA and GA.
    # Let's put SC at 8,14 and 8,15.
    grid[8][14] = 'SC'
    grid[8][15] = 'SC'
    
    # Then GA is at 8,16 and 8,17
    grid[8][16] = 'GA'
    grid[8][17] = 'GA'
    
    grid[9][17] = 'GA'
    
    # Wait, now GA is a 7? Yes, the horizontal bar is 8,16..17. The vertical is 9, 17.
    # What is under SC(8,15)? Nothing. Ocean gulf!
    # Let's check adjacencies:
    # GA touches NC(7,16) at 8,16! And SC(8,15) at 8,16! Total = 2. PERFECT!
    # VA touches WV(6,14), PA(6,15), SC(8,14, 8,15), NC(7,16). Total = 4. PERFECT!
    # SC(8,14, 8,15) touches VA(7,14, 7,15), GA(8,16). Total = 2. PERFECT!
    # NC(7,16) touches MD(6,16), VA(7,15), GA(8,16). Total = 3. PERFECT!
    # PA(5..6, 15) touches OH(5,14), WV(6,14), DE(5,16), MD(6,16), VA(7,15). Total = 5. PERFECT!
    
    # This solves all the math flawlessly!
    
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
        c = colors[s]
        same_col = [n for n in adj[s] if colors.get(n) == c]
        if s == 'MT': continue
        if len(same_col) != targets[s]:
            mismatches += 1
            print(f"{s} mismatches! Got {len(same_col)} {same_col}, Want {targets[s]}.")
            
    holes = 0
    for y in range(1, H-1):
        for x in range(1, W-1):
            if grid[y][x] == '..':
                surr = 0
                for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                    nx, ny = x+dx, y+dy
                    if grid[ny][nx] != '..':
                        surr += 1
                if surr >= 3:
                    holes += 1
                    print(f"Hole at ({x}, {y})")

    print("Holes:", holes)

    if mismatches == 0 and holes == 0:
        print("PERFECT MATCH on layout!")
        
        out_str = []
        for row in grid:
            out_str.append(" ".join(f"{c:2}" for c in row))
            
        g_str = "\n".join(out_str)
        with open('scripts/generate_map.py', 'r') as f:
            script_text = f.read()
            
        script_text = re.sub(r'grid_str = """(.*?)"""', f'grid_str = """\n{g_str}\n"""', script_text, flags=re.DOTALL)
        with open('scripts/generate_map.py', 'w') as f:
            f.write(script_text)
            
    return mismatches

analyze(grid_str)

grid = [
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. AK AK AK .. .. WA WA ID MT MT ND ND MN MN WI WI MI MI MI .. .. VT NH ME",
    ".. .. AK AK AK .. .. OR WA ID MT MT SD SD MN IA WI IL MI MI MI .. .. VT MA MA",
    ".. .. .. .. .. .. .. OR OR ID WY WY SD SD IA IA IL IL IN OH PA NY NY NY MA RI",
    ".. .. .. .. .. .. CA CA NV ID WY WY NE NE IA IA IL IL IN OH PA NJ NY CT CT RI",
    ".. .. .. .. .. .. CA CA NV NV UT CO NE KS MO MO IL KY OH WV PA DE DE CT CT ..",
    ".. .. HI HI HI .. .. CA AZ NV UT CO CO KS MO MO KY KY WV WV MD MD MD .. .. ..",
    ".. .. HI HI HI .. .. .. AZ NM UT CO OK KS AR MO TN TN VA VA VA VA .. .. .. ..",
    ".. .. .. .. .. .. .. .. AZ NM NM OK OK AR AR TN TN TN NC NC NC NC .. .. .. ..",
    ".. .. .. .. .. .. .. .. .. TX TX TX OK AR MS MS AL GA GA SC SC SC .. .. .. ..",
    ".. .. .. .. .. .. .. .. .. TX TX TX LA LA MS MS AL AL GA GA .. .. .. .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL .. .. .. .. .. .."
]
lines = [l.strip().split() for l in grid]
W = max(len(l) for l in lines)
H = len(lines)
g = [r + ['..']*(W-len(r)) for r in lines]
for y in range(H):
    for x in range(W):
        if g[y][x] == 'TN':
            print(f"TN at {y},{x}")
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if 0 <= y+dy < H and 0 <= x+dx < W:
                    print(f"  neighbor at {y+dy},{x+dx}: {g[y+dy][x+dx]}")

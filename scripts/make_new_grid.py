
grid = [
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. .. .. WA ID MT MT ND MN WI MI .. .. .. .. .. .. VT NH NH ME ME ..",
    ".. .. .. OR WA ID MT MT ND MN WI MI .. .. .. .. .. .. VT MA MA .. .. ..",
    ".. .. .. OR ID ID WY WY SD SD IA IL IN OH PA PA NY NY NY MA CT RI .. ..",
    ".. CA CA NV ID WY WY NE IA IA IL IN OH PA PA NJ NY CT CT CT .. .. .. ..",
    ".. CA CA NV NV UT CO NE KS MO IL KY WV MD DE DE .. .. .. .. .. .. .. ..",
    ".. HI HI .. AZ UT CO KS MO MO KY WV VA VA .. .. .. .. .. .. .. .. .. ..",
    ".. .. .. .. AZ NM OK OK AR TN TN NC NC .. .. .. .. .. .. .. .. .. .. ..",
    ".. .. .. .. .. NM TX AR AR MS AL GA SC SC .. .. .. .. .. .. .. .. .. ..",
    ".. .. .. .. .. TX TX LA MS AL GA GA .. .. .. .. .. .. .. .. .. .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. FL FL .. .. .. .. .. .. .. .. .. .. .."
]

def print_grid(g):
    for r in g:
        print(" ".join(f"{c:2}" for c in r.split()))

print_grid(grid)

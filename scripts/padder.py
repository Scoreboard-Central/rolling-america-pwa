grid_raw = [
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

import sys
lines = []
for r in grid_raw:
    parts = r.strip().split()
    lines.append(parts)

max_len = max(len(p) for p in lines)
for i, l in enumerate(lines):
    if len(l) < max_len:
        print(f"Row {i} has length {len(l)} instead of {max_len}")
        lines[i] = l + ['..'] * (max_len - len(l))

for r in lines:
    print(" ".join(f"{c:2}" for c in r))

grid_lines = [
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. AK AK AK .. .. WA WA WA MT MT MT ND ND MN MN WI WI MI MI MI .. .. .. VT VT NH NH ME ME ..",
    ".. .. AK AK AK .. .. WA WA WA ID MT MT SD SD MN MN WI WI MI MI MI NY NY NY NY VT VT NH NH MA MA",
    ".. .. AK AK AK .. .. OR OR OR ID ID WY SD SD SD IA WI IL IL MI MI NY NY NY NY CT MA MA MA MA RI",
    ".. .. .. .. .. .. .. OR OR OR NV ID WY WY WY NE IA IA IL IL IN OH OH PA PA NY NJ CT CT CT RI RI",
    ".. .. .. .. .. .. .. CA CA NV NV UT WY WY CO NE NE MO IL IN OH OH PA PA PA PA NJ DE DE DE .. ..",
    ".. .. .. .. .. .. .. CA CA NV NV UT UT CO CO CO KS KS MO IL KY OH OH WV PA PA MD MD DE DE .. ..",
    ".. .. HI HI HI .. .. CA CA AZ NV UT UT CO CO CO KS KS KS MO MO KY KY KY WV WV MD MD MD .. .. ..",
    ".. .. HI HI HI .. .. CA CA AZ AZ AZ NM NM UT OK OK OK MO MO KY KY VA VA VA VA MD MD .. .. .. ..",
    ".. .. .. .. .. .. .. CA CA AZ AZ AZ AZ NM NM TX TX OK OK AR MO TN TN TN TN VA NC NC NC NC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX AR AR MS MS AL AL GA GA SC SC SC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX LA LA MS MS AL AL GA GA GA GA SC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. LA LA LA LA LA MS MS AL AL AL FL FL FL .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL FL .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .."
]

# TN: needs NC, VA, GA (red), MO, AR, MS, AL, KY (yellow).
# To make TN touch NC, TN must be next to NC or above/below NC.
# To make TN touch GA, TN must be next to GA or above/below GA.
# Let's adjust Row 10 and 11:
grid_lines[9] = ".. .. HI HI HI .. .. CA CA AZ AZ AZ NM NM UT OK OK MO AR MO KY KY VA VA VA VA MD MD .. .. .. .."
grid_lines[10] = ".. .. .. .. .. .. .. CA CA AZ AZ AZ AZ NM NM TX TX OK OK AR AR TN TN TN TN VA NC NC NC NC .. .."
grid_lines[11] = ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX AR AR MS MS AL AL GA GA SC SC SC .. .."

# Wait, we need:
# OK touches KS (row 8 has KS KS KS at 21,22,23 ? No, let's look:
# Row 8:  `CA CA AZ NV UT UT CO CO CO KS KS KS MO MO KY KY KY WV WV MD MD MD` -> CA(7,8) AZ(9) NV(10) UT(11,12) CO(13,14,15) KS(16,17,18) MO(19,20)
# Row 9:  `CA CA AZ AZ AZ NM NM UT OK OK MO AR MO KY KY VA VA VA VA MD MD`     -> CA(7,8) AZ(9,10,11) NM(12,13) UT(14) OK(15,16) MO(17) AR(18) MO(19)
# OK is 15,16. KS is 16,17,18. OK touches KS!
# AR touches MO. AR is 18 in row 9. AR is 20,21 in row 10. AR is 20,21 in row 11.
# MO is 19,20 in row 8. 17, 19 in row 9.
# NY touches PA, NJ, VT, MA, CT.
# NJ touches PA, DE, MD.
# IN touches KY, OH, MI, IL.
# Let's write a targeted script to build specific adjacency rows.

max_w = max(len(l.split()) for l in grid_lines)
fixed_lines = []
for l in grid_lines:
    words = l.split()
    words.extend(['..'] * (max_w - len(words)))
    fixed_lines.append(" ".join(words))

import re
with open('make_map.py', 'r') as f:
    code = f.read()

joined = ",\n    ".join(f'"{fl}"' for fl in fixed_lines)
new_code = re.sub(r'grid_lines = \[(.*?)\]', f'grid_lines = [\n    {joined}\n]', code, flags=re.DOTALL)
with open('make_map.py', 'w') as f:
    f.write(new_code)

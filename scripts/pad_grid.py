
grid = [
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. AK AK AK .. .. WA WA WA MT MT MT ND ND MN MN WI WI MI MI MI .. .. .. VT VT NH NH ME ME .. ..",
    ".. .. AK AK AK .. .. WA WA WA ID MT MT SD SD MN MN WI WI MI MI MI NY NY NY NY VT VT NH NH NH NH ..",
    ".. .. AK AK AK .. .. OR OR OR ID ID WY SD SD SD IA WI IL IL MI MI MI NY NY NY VT MA MA MA MA RI ..",
    ".. .. .. .. .. .. .. OR OR OR NV ID WY WY WY NE IA IA IL IL IN IN OH PA PA NY NY NY CT CT CT RI ..",
    ".. .. .. .. .. .. .. CA CA NV NV UT WY WY CO NE NE MO MO IL IN OH OH PA PA NJ DE DE DE DE .. .. ..",
    ".. .. .. .. .. .. .. CA CA NV NV UT UT CO CO CO KS KS MO IL KY OH OH WV PA PA PA DE DE DE .. .. ..",
    ".. .. HI HI HI .. .. CA CA AZ NV UT UT CO CO CO KS KS MO MO KY KY KY WV WV WV MD MD MD .. .. .. ..",
    ".. .. HI HI HI .. .. CA CA AZ AZ AZ NM NM NM OK OK OK MO MO KY KY VA VA VA VA VA MD .. .. .. .. ..",
    ".. .. .. .. .. .. .. CA CA AZ AZ AZ AZ NM NM TX TX OK OK MO TN TN TN TN TN NC NC NC NC NC .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX AR AR AR MS MS AL GA GA GA SC SC SC .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX LA LA MS MS AL AL GA GA GA GA SC .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. LA LA LA LA LA MS MS AL AL AL FL FL FL .. .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL FL .. .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .. .."
]
lines = [l.split() for l in grid]

# Apply patches from earlier
lines[4][19] = 'IN'  # IL-MI
lines[8][25] = 'PA'  # MD-WV
lines[2][10] = 'ID'  # MT-WA
lines[9][12] = 'AZ'  # UT-NM

# Add back UT and NM connection! (User made asymmetric edit, we want symmetric connection)
# Actually, the user rules dict added it back automatically since we enforced symmetry!
# But wait, my patch broke UT and NM connection!
# Does the USER want UT and NM connected?
# Yes, user rules say NM: AZ, CO, OK, TX, UT. So they DO touch!
# So I should NOT apply the UT-NM patch!
lines[9][12] = 'NM' # Revert my patch

# To fix accidental NY-MI and NY-DE touches, let's look at the grid.
# NY is at Row 3 (23-26), Row 4 (23-25), Row 5 (23-25)
# DE is at Row 6 (26-29), Row 7 (27-29)
# MI is at Row 2 (19-21), Row 3 (20-22), Row 4 (20-22)
# NY(Row 3, 23) is next to MI(Row 3, 22). Wait, Row 3 has MI MI MI NY NY NY NY.
# Does NY touch MI orthogonally? Yes, Row 3: MI(21), NY(22).
# Wait, Does NY touch MI in the rules?
# NY: CT, PA, MA, NJ, VT.
# IT NEVER TOUCHES MI in the rules!!
# Oh!! Row 3 has `MI MI MI NY NY NY NY`?! So they touch orthogonally!
# Why didn't `test_patches.py` complain about `NY` touching `MI` orthogonally?!

import sys
for r in lines:
    print(" ".join(f"{c:2}" for c in r))


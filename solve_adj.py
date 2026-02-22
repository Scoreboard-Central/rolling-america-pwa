grid_str = """
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
AK AK .. WA ID MT ND MN MN WI MI ME ME ME ME .. .. .. .. .. .. ..
AK AK .. WA OR SD SD SD IA WI MI VT VT NH MA MA .. .. .. .. .. ..
HI HI .. OR OR NV UT CO NE IA IA IL IN NY NY NY NH MA MA .. .. ..
CA CA .. NV NV UT WY KS MO AR KY IN IN NJ CT RI PA PA PA DE .. ..
.. .. .. AZ AZ NM OK TX LA AL TN OH WV PA MD MD NC NC .. .. .. ..
. . . . . . . . . . . . . GA SC VA VA NC .. .. .. . . . . . . . .
"""

def make_orange():
    return """
WA ID ID
WA OR OR
OR OR NV
CA NV NV
CA AZ UT
CA AZ UT
"""
# targets: WA 2, OR 4, ID 4, UT 3, AZ 3, NV 5, CA 3
# WA: ID, OR (2)
# OR: WA, ID, NV, CA (4)
# ID: WA, OR, NV (3) - wait, ID target is 4.
# Let's write a python builder.

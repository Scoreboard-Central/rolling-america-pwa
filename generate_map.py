import json

grid_str = """
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. AK AK .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME
.. .. AK AK .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. VNH VNH ME
.. .. .. .. WA WA IDNV MT MT ND ND MNIA MNIA .. .. .. .. NY NY VNH VNH MA MA
.. .. .. .. OR OR IDNV WY WY SD SD MNIA MNIA WI WI MI MI PA PA NY NY MA MA
.. .. .. .. CA UTAZ CONE CONE MNIA MNIA IL IL IN OH OH WV MD NJ RCT RCT
.. .. .. .. CA UTAZ CONE CONE KS KS MOAR IL IL IN OH OH VA VA DE RCT RCT
.. HI HI .. .. .. NM NM OK OK MOAR KYTN KYTN KYTN NC NC NC .. .. ..
.. .. .. .. .. .. .. TX TX TX LA KYTN KYTN KYTN SC SC .. .. .. ..
.. .. .. .. .. .. .. TX TX TX LA MSAL MSAL GAFL GAFL GAFL .. .. .. ..
.. .. .. .. .. .. .. .. TX TX .. MSAL MSAL GAFL GAFL GAFL .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. GAFL .. .. .. .. .. ..
"""

colors = {
    'AK': 'ra-orange', 'HI': 'ra-orange', 'WA': 'ra-orange', 'OR': 'ra-orange', 'CA': 'ra-orange', 'IDNV': 'ra-orange', 'UTAZ': 'ra-orange',
    'MT': 'ra-blue', 'WY': 'ra-blue', 'ND': 'ra-blue', 'SD': 'ra-blue', 'CONE': 'ra-blue', 'MNIA': 'ra-blue',
    'NM': 'ra-green', 'KS': 'ra-green', 'OK': 'ra-green', 'TX': 'ra-green', 'MOAR': 'ra-green', 'LA': 'ra-green',
    'WI': 'ra-yellow', 'MI': 'ra-yellow', 'IL': 'ra-yellow', 'IN': 'ra-yellow', 'OH': 'ra-yellow', 'KYTN': 'ra-yellow', 'MSAL': 'ra-yellow',
    'PA': 'ra-red', 'WV': 'ra-red', 'VA': 'ra-red', 'NC': 'ra-red', 'SC': 'ra-red', 'GAFL': 'ra-red',
    'NJ': 'ra-purple', 'NY': 'ra-purple', 'MA': 'ra-purple', 'VNH': 'ra-purple', 'RCT': 'ra-purple', 'ME': 'ra-purple', 'MD': 'ra-purple', 'DE': 'ra-purple'
}
# wait, the subagent said NC/SC is ONE box. So NC SC should be NCSC.
# Let's rewrite the grid_str:

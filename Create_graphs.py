'''

This Code is Written By: Mehdi Touyserkani - Feb 2024.
BESTPRO SOFTWARE ENGINEERING GROUP

'''

import networkx as nx
import random
from Parameters import Params

#________Create Some Graphs according to base paper__________

def create_erods_renyi_graph(V):
    GG = nx.erdos_renyi_graph(V,random.uniform(Params.d[0] , Params.d[1])) # Density Between 0.04 and 0.5 according to the based paper section 3
    return GG

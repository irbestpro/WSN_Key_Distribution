'''

This Code is Written By: Mehdi Touyserkani - Feb 2024.
BESTPRO SOFTWARE ENGINEERING GROUP

Base Paper: https://arxiv.org/pdf/1901.07314.pdf

'''

class Params:
    ci = [5,6,7,8] # maximum capacity of each node Memory
    tk = [3,4,5] # number of Keys assigned to each node
    K  = [10,20,30,60] # Number of All keys
    V  = [10,30,50,60] # Number of Vectextes
    d  = [0.04,0.5] # Graph Distribution Probability
    p  = 0.3 # Probability of Number of time each key used
    alpha = 1 # To avoid Zero Result
    q = 1 # K Common Shared Keys
    mk = 1 # amount of memory required to save k
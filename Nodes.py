'''

This Code is Written By: Mehdi Touyserkani - Feb 2024.
BESTPRO SOFTWARE ENGINEERING GROUP

Base Paper: https://arxiv.org/pdf/1901.07314.pdf

'''

from Parameters import Params
import numpy as np

class Nodes :
       
    def __init__(self,id):
        self.id = id
        self.keys = []
        self.Keynames = []
    
    def Add_Key(self,key):
        self.keys.append(key)
        
    def Add_Name(self,name):
        self.Keynames.append(name)
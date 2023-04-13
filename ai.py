import sys, os
import random
import time 

class AI():

    def choose_move(self, list):
        if len(list) > 0 :
            return random.sample(list, 1)[0]
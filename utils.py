import settings
import random 

def height_prct(percentage):
    return (settings.WINDOW_HEIGHT / 100 ) * percentage 

def width_prct(percentage):
    return (settings.WINDOW_WIDTH / 100 ) * percentage 

def choose_goal():
    return random.sample(['win', 'lose', 'draw'], 1)

def whos_turn(parity):
    if parity == 0:
        return "your"
    else:
        return "the ai's"
    
def change_parity(parity):
    if parity == 0:
        return 1
    if parity == 1:
        return 0

import sys, os
import tkinter as tk
from tkinter import *
import utils 
import time 
from ai import AI
import settings 

class Engine:

    board_state = [0,0,0,0,0,0,0,0,0] 

    all = []

    round_trigger = 0

    turn_trigger = 0

    game_trigger = 0

    parity = 0

    turn = 0

    player_score_label_object = None

    ai_score_label_object = None 

    player_score = 0

    ai_score = 0 

    player_goal_label_object = None

    ai_goal_label_object = None 

    player_goal = ''

    ai_goal = ''

    turn_label_object = None

    message_label_object = None 

    next_round_button_object = None 

    agent = AI()

    #FORMAT = cell -> (row, column, forwards diag, back diag)
    neighbor_dictionary = {
            1 : ((1, 4, 7), (1, 2, 3), None, (1, 5, 9)),
            2 : ((2, 5, 8), (1, 2, 3), None, None),
            3 : ((3, 6, 9), (1, 2, 3), (3, 5, 7), None),
            4 : ((1, 4, 7), (4, 5, 6), None, None),
            5 : ((2, 5, 8), (4, 5, 6), (3, 5, 7), (1, 5, 9)),
            6 : ((3, 6, 9), (4, 5, 6), None, None),
            7 : ((1, 4, 7), (7, 8, 9), (3, 5, 7), None),
            8 : ((2, 5, 8), (7, 8, 9), None, None),
            9 : ((3, 6, 9), (7, 8, 9), None, (1, 5, 9))
            }

    def __init__(self, position) -> None:
        self.position = position
        Engine.all.append(self)
        self.game_square_button_object = None 
        self.game_frame_object = None
        self.is_blank = True
        self.owned_by_player = False
        self.owned_by_ai = False

    @staticmethod
    def get_cell_by_position(position):
        for c in Engine.all:
            if c.position == position:
                return c

    @staticmethod
    def create_player_goal_label(location):
        Engine.player_goal = utils.choose_goal()
        # Engine.player_goal = ['win']
        lbl = Label(
            location, 
            text =f'     Your goal this round is to {Engine.player_goal[0]}.',
            bg = 'black',
            fg ='white',
            font = ('', 35)
        )
        Engine.player_goal_label_object = lbl 

    @staticmethod
    def create_ai_goal_label(location):
        Engine.ai_goal = utils.choose_goal()
        lbl = Label(
            location, 
            # text =f'     The ai\'s goal last round was to {Engine.ai_goal[0]}.',
            bg = 'black',
            fg ='white',
            font = ('', 35)
        )
        Engine.ai_goal_label_object = lbl 

    @staticmethod
    def create_turn_label(location):
        lbl = Label(
            location, 
            text = f'It is currently {utils.whos_turn(Engine.parity)} turn.',
            bg = 'black',
            fg = 'white',
            font = ("", 35)
        )

        Engine.turn_label_object = lbl

    @staticmethod
    def create_message_label(location):
        lbl = Label(
            location, 
            bg = 'black',
            fg = 'white',
            font = ("", 35)
        )

        Engine.message_label_object = lbl

    @staticmethod
    def create_player_score_label(location):
        lbl = Label(
            location, 
            text =f'You have\n{Engine.player_score}\npoints',
            bg = 'black',
            fg ='white',
            font = ('', 35)
        )
        Engine.player_score_label_object = lbl 

    @staticmethod
    def create_ai_score_label(location):
        Engine.ai_goal = utils.choose_goal()
        lbl = Label(
            location, 
            text =f'The ai has\n{Engine.ai_score}\npoints',
            bg = 'black',
            fg ='white',
            font = ('', 35)
        )
        Engine.ai_score_label_object = lbl 

    @staticmethod
    def create_next_round_button_object(location):
        btn = Button(
            location, 
            bg = 'White',
            fg = 'black',
            text = 'Begin Next\nRound',
            font = ("", 30)
        )
        Engine.next_round_button_object = btn
        Engine.next_round_button_object.bind('<Button-1>', Engine.next_round)

    @staticmethod
    def next_round(event):
        Engine.round_trigger = 2
        Engine.player_goal = utils.choose_goal()
        Engine.ai_goal = utils.choose_goal()
        Engine.update_messages()
        for c in Engine.all:
            c.activate_cell()
            c.game_square_button_object.configure(text = '', bg = 'white')
            c.owned_by_player = False
            c.owned_by_ai = False
        if Engine.parity == 1:
                Engine.click_cell_by_index(Engine.agent.choose_move(Engine.get_open_cells_indicies()))
        
    @staticmethod
    def end_round(code):
        if code == 0:
            Engine.ai_goal_label_object.configure(text =f'     The ai\'s goal last round was to {Engine.ai_goal[0]}.')
            Engine.message_label_object.configure(text = 'The round is a draw')
            for c in Engine.all:
                c.deactivate_cell()
            if Engine.ai_goal[0] == 'draw':
                Engine.ai_score += 1
                Engine.ai_score_label_object.configure(text = f'The ai has\n{Engine.ai_score}\npoints')
            if Engine.player_goal[0] == 'draw':
                Engine.player_score += 1
                Engine.player_score_label_object.configure(text = f'You have\n{Engine.player_score}\npoints')
            Engine.round_trigger = 1

        if code == 1:
            Engine.ai_goal_label_object.configure(text =f'     The ai\'s goal last round was to {Engine.ai_goal[0]}.')
            Engine.message_label_object.configure(text = 'You win this round')
            for c in Engine.all:
                c.deactivate_cell()
            if Engine.ai_goal[0] == 'lose':
                Engine.ai_score += 1
                Engine.ai_score_label_object.configure(text = f'The ai has\n{Engine.ai_score}\npoints')
            if Engine.player_goal[0] == 'win':
                Engine.player_score += 1
                Engine.player_score_label_object.configure(text = f'You have\n{Engine.player_score}\npoints')
            Engine.round_trigger = 1

        if code == 2:
            Engine.ai_goal_label_object.configure(text =f'     The ai\'s goal last round was to {Engine.ai_goal[0]}.')
            Engine.message_label_object.configure(text = 'The ai wins this round')
            for c in Engine.all:
                c.deactivate_cell()
            if Engine.ai_goal[0] == 'win':
                Engine.ai_score += 1
                Engine.ai_score_label_object.configure(text = f'The ai has\n{Engine.ai_score}\npoints')
            if Engine.player_goal[0] == 'lose':
                Engine.player_score += 1
                Engine.player_score_label_object.configure(text = f'You have\n{Engine.player_score}\npoints')
            Engine.round_trigger = 1
        Engine.evaluate_score()

    @staticmethod
    def get_open_cells_indicies():
        list = []
        for c in Engine.all:
            if c.is_blank:
                list.append(c.position)
        return list
    
    @staticmethod
    def click_cell_by_index(value):
        for c in Engine.all:
            if c.position == value:
                c.left_click_actions(None)

    def check_win_lose_draw(self):
        neighbors = Engine.neighbor_dictionary[self.position]
        win = 0 
        ultra_win = -1
        for tuple in neighbors:
            check = True
            if tuple:
                for x in tuple:
                    candidate = Engine.get_cell_by_position(x)
                    if not candidate.owned_by_player:
                        check = False
                if check:
                    win = 1 
                    for x in tuple:
                        candidate = Engine.get_cell_by_position(x)
                        candidate.game_square_button_object.configure(bg = 'green')
                    ultra_win = 1 
        for tuple in neighbors:
            check = True
            if tuple:
                for x in tuple:
                    candidate = Engine.get_cell_by_position(x)
                    if not candidate.owned_by_ai:
                        check = False
                if check:
                    win = 2 
                    for x in tuple:
                        candidate = Engine.get_cell_by_position(x)
                        candidate.game_square_button_object.configure(bg = 'green')
                    ultra_win = 2
        if win == 0:
            draw = True
            for c in Engine.all:
                if c.is_blank:
                    draw = False
            if draw:
                ultra_win = 0
        return ultra_win

    def deactivate_cell(self):
        self.is_blank =False
        self.game_square_button_object.unbind('<Button-1>')

    def activate_cell(self):
        self.game_square_button_object.bind('<Button-1>', self.left_click_actions)
        self.is_blank = True 

    def left_click_actions(self, event):
        self.deactivate_cell()
        if Engine.parity == 0:
            self.game_square_button_object.configure(text = 'X')
            self.owned_by_player = True
            Engine.parity = utils.change_parity(Engine.parity)
            Engine.turn_label_object.configure(text = f'It is currently {utils.whos_turn(Engine.parity)} turn.')
            Engine.end_round(self.check_win_lose_draw())
            if len(Engine.get_open_cells_indicies()) > 0 :
                Engine.click_cell_by_index(Engine.agent.choose_move(Engine.get_open_cells_indicies()))
        elif Engine.parity == 1:
            self.game_square_button_object.configure(text = 'O')
            self.owned_by_ai = True
            Engine.parity = utils.change_parity(Engine.parity)
            Engine.turn_label_object.configure(text = f'It is currently {utils.whos_turn(Engine.parity)} turn.')
            Engine.end_round(self.check_win_lose_draw())

    @staticmethod
    def update_messages():
        Engine.message_label_object.configure(text = '')
        Engine.ai_goal_label_object.configure(text = '')
        Engine.player_goal_label_object.configure(text =f'     Your goal this round is to {Engine.player_goal[0]}.')
    
    def create_game_spot_object(self, location):
        btn = Button(
            location, 
            bg = 'White',
            fg = 'black',
            text = '',
            font = ("", 60)
        )
        self.game_square_button_object = btn
        self.game_square_button_object.bind('<Button-1>', self.left_click_actions)

    def create_game_spot_frame(self, location):
        frame = Frame(location,
                      bg = 'blue',
                      width = utils.width_prct(20),
                      height = utils.height_prct(20)
                      )
        self.game_frame_object = frame

    @staticmethod
    def evaluate_score():
        if Engine.player_score >= settings.SCORE_LIMIT and Engine.ai_score >= settings.SCORE_LIMIT:
            if Engine.player_score > Engine.ai_score:
                Engine.game_trigger = 1
            if Engine.player_score < Engine.ai_score:
                Engine.game_trigger = 2
        else:
            if Engine.player_score >= settings.SCORE_LIMIT:
                Engine.game_trigger = 1
            if Engine.ai_score >=settings.SCORE_LIMIT:
                Engine.game_trigger = 2
            
    @staticmethod
    def reset_all():
        
        Engine.all = []

        Engine.round_trigger = 0

        Engine.turn_trigger = 0

        Engine.game_trigger = 0

        Engine.parity = 0

        Engine.turn = 0

        Engine.player_score_label_object = None

        Engine.ai_score_label_object = None 

        Engine.player_score = 0

        Engine.ai_score = 0 

        Engine.player_goal_label_object = None

        Engine.ai_goal_label_object = None 

        Engine.player_goal = ''

        Engine.ai_goal = ''

        Engine.turn_label_object = None

        Engine.message_label_object = None 

        Engine.next_round_button_object = None 

        Engine.agent = AI()
        

#############################################3
#############BUGS TO FIX!!!!!!!!!!
##############################################
 #    
##   
#   make ai turn feel better- sleep 
## handle winning/losing the game 
#       reset after winning/losing game suuuper broken 
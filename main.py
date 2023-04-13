import sys, os
import tkinter as tk 
from tkinter import *
import settings 
import utils
import time 
from engine import Engine

trigger = 0

class IITTT(tk.Tk):

    def __init__(self):

        super().__init__()

        #settings
        self.configure(bg='black')
        self.geometry(f'{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}')
        self.title('SMBC Tic-Tac-Toe')
        self.resizable(FALSE, FALSE)

        self.end_frame = None
        self.meme_trigger = 7
        self.meme_frame = None
        self.counter = 0

        self.load_start_screen(None)

    def load_start_screen(self, event):

        if self.end_frame:
            self.end_frame.place_forget()


        self.start_frame = Frame(
            self, 
            bg ='black',
            width=utils.width_prct(100),
            height=utils.height_prct(100)
        )

        self.start_frame.place(x=0, y=0)

        self.start_label = Label(
            self.start_frame,
            bg = 'black', 
            fg = 'white',
            text = settings.WELCOME_MESSAGE,
            font = ('', 25)
        )

        self.start_label.grid(row=0, column=0, padx = utils.width_prct(4), pady = utils.height_prct(10))


        self.start_button = Button(
            self.start_frame,
            width = 12,
            height = 6,
            text = "Start Game",
            font = ('', 15),
        )

        self.start_button.grid(row =1, column =0)

        self.meme_button = Button(
            self.start_frame,
            width = 12,
            height = 6,
            text = "Delete\nHard Drive",
            font = ('', 15),
        )

        self.meme_button.grid(row =2, column =0, pady = 20)

        self.start_button.bind('<Button-1>', self.begin_game)
        self.meme_button.bind('<Button-1>', self.trigger_meme)

        self.after(10, self.begin_meme)
    
    def begin_game(self, event):

        self.start_frame.place_forget()

        self.top_frame = Frame(
            self, 
            bg='black',
            width = utils.width_prct(100),
            height = utils.height_prct(20)
        )

        self.top_frame.place(x=0, y=0)

        self.bot_frame = Frame(
            self, 
            bg='black',
            width = utils.width_prct(100),
            height = utils.height_prct(20)
        )

        self.bot_frame.place(x=0, y=utils.height_prct(80))


        self.left_frame = Frame(
            self, 
            bg = 'black',
            width = utils.width_prct(20),
            height = utils.height_prct(60)
        )

        self.left_frame.place(x =0, y = utils.height_prct(20))


        self.right_frame = Frame(
            self, 
            bg = 'black',
            width = utils.width_prct(20),
            height = utils.height_prct(60)
        )

        self.right_frame.place(x = utils.width_prct(80), y = utils.height_prct(20))

        self.center_frame = Frame(
            self, 
            bg = 'black',
            width = utils.width_prct(60),
            height = utils.height_prct(60)
        )

        self.center_frame.place(x=utils.width_prct(20), y=utils.height_prct(20))

        Engine.create_player_goal_label(self.top_frame)
        Engine.player_goal_label_object.grid(row=0, column=0, pady = 5)
        Engine.create_turn_label(self.top_frame)
        Engine.turn_label_object.grid(row =1, column = 0, pady = 5)
        Engine.create_ai_score_label(self.right_frame)
        Engine.ai_score_label_object.place(x=0, y=0)
        Engine.create_player_score_label(self.left_frame)
        Engine.player_score_label_object.place(x=0, y=0)
        Engine.create_ai_goal_label(self.bot_frame)
        Engine.ai_goal_label_object.grid(row=0, column=0, pady = 7)
        Engine.create_message_label(self.bot_frame)
        Engine.message_label_object.grid(row =1, column = 0, pady = 5)
        
        counter = 0
        for x in range(3):
            for y in range(3):
                counter+= 1
                e = Engine(counter)
                e.create_game_spot_frame(self.center_frame)
                e.create_game_spot_object(e.game_frame_object)
                e.game_frame_object.pack_propagate(0)
                e.game_square_button_object.pack(expand = True, fill = 'both') 
                e.game_frame_object.place(x= x * utils.width_prct(20), y= y * utils.height_prct(20) )

                



        self.after(50, self.listen)
        self.after(50, self.escuchar)
        



    def listen(self):
        trigger = Engine.round_trigger
        if trigger == 1:
            if not Engine.next_round_button_object:
                Engine.create_next_round_button_object(self.bot_frame)
            if not Engine.next_round_button_object.winfo_ismapped():
                Engine.next_round_button_object.grid(row = 0, column= 1)
                

        if trigger == 2:
            if Engine.next_round_button_object:
                Engine.next_round_button_object.grid_forget()
            Engine.round_trigger = 0


        self.after(50, self.listen)

    def escuchar(self):
        trigger = Engine.game_trigger
        if not trigger == 0:
            self.top_frame.place_forget()
            self.left_frame.place_forget()
            self.right_frame.place_forget()
            self.right_frame.place_forget()
            self.bot_frame.place_forget()
            self.center_frame.place_forget()

            self.end_frame = Frame(
            self, 
            bg ='black',
            width=utils.width_prct(100),
            height=utils.height_prct(100)
            )

            self.end_frame.place(x=0, y=0)

            if trigger == 1:
                self.end_label = Label(
                    self.end_frame,
                    bg = 'black', 
                    fg = 'white',
                    text = settings.GOODBYE_MESSAGE_VICTORY,
                    font = ('', 25)
                )
            if trigger == 2:
                self.end_label = Label(
                    self.end_frame,
                    bg = 'black', 
                    fg = 'white',
                    text = settings.GOODBYE_MESSAGE_DEFEAT,
                    font = ('', 25)
                )

            self.end_label.grid(row=0, column=0, padx = utils.width_prct(4), pady = utils.height_prct(10))


            self.new_game_button = Button(
                self.end_frame,
                width = 12,
                height = 6,
                text = "Restart Game",
                font = ('', 15),
            )

            self.new_game_button.grid(row =1, column =0)

            self.exit_button = Button(
                self.end_frame,
                width = 12,
                height = 6,
                text = "Close Game",
                font = ('', 15),
            )

            self.exit_button.grid(row =2, column =0, pady = 20)

            self.new_game_button.bind('<Button-1>', self.new_game)
            self.exit_button.bind('<Button-1>', sys.exit)

            Engine.game_trigger = 0
            

        self.after(50, self.escuchar)

    def new_game(self, event):
        Engine.reset_all()
        self.load_start_screen(None)


    def trigger_meme(self, event):
        self.meme_trigger = 1



    def begin_meme(self):
        if self.meme_trigger == 1:
            self.start_frame.place_forget()

            if not self.meme_frame:
                self.meme_frame = Frame(
                    self, 
                    bg='black',
                    width = utils.width_prct(100),
                    height = utils.height_prct(100)
                )
                self.meme_frame.place(x=0, y=0)

                self.meme_label = Label(
                            self.end_frame,
                            bg = 'black', 
                            fg = 'white',
                            text = 'ERROR',
                            font = ('', 25)
                        )

                self.meme_label.grid(row=0, column=0)

            self.after(6669, self.animate_meme)
            

        self.after(10, self.begin_meme)


    def animate_meme(self):
        if self.counter < 2000:
            if self.counter % 3 == 0:
                self.meme_label.configure(text = settings.MEME_MESSAGE_ONE)
            if self.counter % 3 == 1:
                self.meme_label.configure(text = settings.MEME_MESSAGE_TWO)
            if self.counter % 3 == 2:
                self.meme_label.configure(text = settings.MEME_MESSAGE_THREE)
        if self.counter > 2000:
            self.meme_label.configure(text = 'ERROR')
        if self.counter > 2001:
            self.meme_label.configure(text = settings.JUNK)
        self.counter += 1
        if self.counter > 2010:
            time.sleep(4.5)
            sys.exit()
        self.after(9666, self.animate_meme)

        

    # screen fills with random junk characters and the window closes.  


if __name__ == '__main__':

    root = IITTT()

    root.mainloop()

            
        



























#
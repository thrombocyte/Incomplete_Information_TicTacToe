import sys, os
import tkinter as tk 
from tkinter import *
import settings 
import utils
from engine import Engine

trigger = 0

class IITTT(tk.Tk):

    def __init__(self):

        super().__init__()

        #settings
        self.configure(bg='black')
        self.geometry(f'{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}')
        self.title('Mine Sweeper')
        self.resizable(FALSE, FALSE)


    
    #def begin_game():
        self.top_frame = Frame(
            self, 
            bg='black',
            width = utils.width_prct(100),
            height = utils.height_prct(25)
        )

        self.top_frame.place(x=0, y=0)


        self.left_frame = Frame(
            self, 
            bg = 'black',
            width = utils.width_prct(40),
            height = utils.height_prct(50)
        )

        self.left_frame.place(x =0, y = 180)


        self.center_frame = Frame(
            self, 
            bg = 'black',
            width = utils.width_prct(60),
            height = utils.height_prct(75)
        )

        self.center_frame.place(x=utils.width_prct(25), y=utils.height_prct(25))


        for x in range(settings.GRID_SIZE):
            for y in range(settings.GRID_SIZE):
                c = Cell(x, y)
                c.create_button_object(self.center_frame)
                c.cell_button_object.grid(column = x, row = y)


        Cell.create_cell_count_label(self.left_frame)
        Cell.cell_count_label_object.place(x=0, y =0 )
        Cell.create_message_label(self.top_frame)
        Cell.cell_message_label_object.place(x=utils.width_prct(10), y=utils.height_prct(5))

        Cell.randomize_mines()

        self.left_frame.after(1, self.listen)

    def listen(self):
        trigger = Cell.trigger
        if trigger == 1:
            if not Cell.reset_button:
                Cell.create_reset_button(self.left_frame)
            Cell.reset_button.place(x= 0, y =0)
            Cell.reset_button.bind('<Button-1>',  Cell.reset)
            if not Cell.exit_button:
                Cell.create_exit_button(self.left_frame)
            Cell.exit_button.place(x= 0, y =50)
            Cell.exit_button.bind('<Button-1>', sys.exit)
            
        if trigger == 2:
            Cell.reset_button.place_forget()
            Cell.exit_button.place_forget()
            Cell.create_message_label(self.top_frame)
            Cell.create_cell_count_label(self.left_frame)
            Cell.cell_count_label_object.place(x=0, y =0 )
            Cell.cell_message_label_object.place(x=utils.width_prct(10), y=utils.height_prct(5))
            Cell.trigger = 0

        self.left_frame.after(5, self.listen)



if __name__ == '__main__':

    root = SweepyBoi()

    root.mainloop()

            
        



























#
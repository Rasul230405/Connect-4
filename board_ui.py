# this file is to create GUI for circle-4 board
# BoardUI

from tkinter import *
from tkinter import ttk

from gameLogic import GameLogic
from board import Board

class BoardUI:

    def __init__(self,  width: int, height: int, bg_colour: str, p_colour: str, ai_colour: str):
        self.game_logic = GameLogic()

        # variable initialisations
        self.n_rows = Board.row
        self.n_cols = Board.column

        self._player_colour = p_colour
        self._ai_colour = ai_colour
        self._bg_colour = bg_colour
        
        self.width = width
        self.height = height

        self._player_turn = True # to control the turns, because tkinter is event based
        self._endgame = False
    
        self._root = Tk()
        self._canvas = Canvas(self._root, width=width, height=height, background=self._bg_colour);

    
        # create the board
        self.__create_boardui();

    
    def display_board(self):       
        self._root.mainloop()

    def __open_endgame_window(self, mssg: str):
        win = Toplevel(self._root)
        win.geometry(str(int(self.height/2)) + "x" + str(int(self.width/2)))
        win.title("Game Over")
        l = Label(win, text=mssg, bg='#fff', fg='#f00', width = win.winfo_width() - 40, height = int(win.winfo_height() / 4))
        l.place(relx=0.1, rely=0.5)
        
        
    def __player_move(self, event, column, row):
        # if clicked to any circle in 'column', colour the circle in the lowest row possible (meaning if it is not coloured already)
        # change _player_move to false to block user from making a move before AI makes a move
        # then call the function to make the AI move (inside ai_move function set
        # _player_turn to True)

        if self._player_turn and not self._endgame:

            move_row = self.game_logic.make_move(column, 'player')

            # if row is full, dont do anything
            if move_row == -1:
                return

            circle = self._canvas.find_withtag(str(column)+"_"+str(move_row))
            self._canvas.itemconfigure(circle, fill=self._player_colour)
            
            self._player_turn = False
            
            if self.game_logic.is_endgame(move_row, column):
                self._endgame = True
                #self._root.after(1, self.__open_endgame_window, 'YOU WON!')
                self.__open_endgame_window('YOU WON!')
                return

            if not self._endgame: 
                #self._root.after(1, self.__ai_move)
                self.__ai_move()

    def __ai_move(self):
        [row, col] = self.game_logic.ai_move()
        
        circle = self._canvas.find_withtag(str(col)+"_"+str(row))
        self._canvas.itemconfigure(circle, fill=self._ai_colour)

        if self.game_logic.is_endgame(row, col):
            print("AI wins")
            self._endgame = True
            #self._root.after(1, self.__open_endgame_window, 'YOU LOST:( Hades will come and take you to the Underworld!')
            self.__open_endgame_window('YOU LOST:( Hades will come and take you to the Underworld!')
            return

        self._player_turn = True
        

    def __create_boardui(self):
        # add padding
        self._canvas.grid(row=0, column=0, padx=20, pady=20)

        # 6x7 board
        w = self.width / self.n_cols
        h = self.height / self.n_rows
        
        for i in range(0, 7): # columns
            for j in range(0, 6): # rows
                
                # tag format: (1_2, col_1)
                tags = (str(i) + "_" + str(j), "col_" + str(i));
                
                self.__create_circle(i*w +(w / 2), j*h + h / 2,  w / 2, self._bg_colour, self._canvas, tags=tags)

                # bind an event. <Button-1> means mouse left-click
                # bind the circles in the same column with same tag
                self._canvas.tag_bind(tags[1], "<Button-1>", lambda e, c=i, r=j: self.__player_move(e, c, r))

    

    @staticmethod
    def __create_circle( x, y, r, fill_colour, canvas, tags):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvas.create_oval(x0, y0, x1, y1, fill=fill_colour, tags=tags)
           

board_ui = BoardUI(700, 600, 'gray75', 'green', 'red');
board_ui.display_board()


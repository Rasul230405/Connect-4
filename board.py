# This file contains Board class implementation

"""
Board is (m)x(n) 1D numpy array where player pieces represented by Board.player and AI pieces
by Board.ai, empty cells by Board.empty. These static variables are just numbers. Following is the sketch of empty 6x7 board:
                           0 1 2 3 4 5 6
                           _____________
                        0 |0 0 0 0 0 0 0
                        1 |0 0 0 0 0 0 0 
                        2 |0 0 0 0 0 0 0 
                        3 |0 0 0 0 0 0 0 
                        4 |0 0 0 0 0 0 0 
                        5 |0 0 0 0 O 0 0

Size of a board is not limited to the 6x7. it can be specified when creating a board, and cannot be and shouldnt be changed after that.

display() function prints the board to the terminal in a nicely formatted way
"""

import numpy as np

class Board:

    player = 1
    ai = 2
    full = 3
    empty = 0
    red = 'r'
    blue = 'b'
    
    def __init__(self, p_colour: str, row: int=6, column: int=7):
        self.column = column
        self.row = row

        self._p_colour = p_colour
        self._ai_colour = Board.red if p_colour == Board.blue else Board.blue
        self._board = Board.__create_board(self.row, self.column)


    def set(self, row: int, col: int, char: int) -> None:
        # puts the piece in a specified coordinate
        if char == Board.ai:
            self._board[row][col] = Board.ai
        elif char == Board.player:
            self._board[row][col] = Board.player
        else:
            raise ValueError("Board::put(): char should be either Board.ai or Board.player")

    def remove(self, row:int, col: int) -> None:
        # removes the the piece from board in a specified coordinate
        # just replaces the 'character' in [row][col] with Board.empty
        self._board[row][col] = Board.empty

    def get(self, row: int, col: int) -> int:
        # returns the 'character' in board[row][col]
        # 'character' is either Board.ai or Board.player
        return self._board[row][col]

    def is_full(self) -> bool:
        return np.all(self._board != 0)

        
    def display(self) -> None:
        # at top print column numbers
        for i in range(0, self.column):
            if i == 0:
                print(f"  {i}", end="")
                continue
            
            print(f" {i}", end="")
            
        print()

        for i in range(0, self.row):
            # print row number
            print(f"{i} ", end="")

            # print characters: Board.ai = blue O, Board.player = red O, Board.empty = .
            for j in range(0, self.column):
                if self._board[i][j] == Board.player:
                    print(Board.__colour_char("O", self._p_colour), end=" ")
                elif self._board[i][j] == Board.ai:
                    print(Board.__colour_char("O", self._ai_colour), end=" ")
                else:
                    print(". ", end="")

            print()

        print("\n")

    @staticmethod
    def __create_board(row, col):# returns numpy array
        arr = np.zeros((row, col), dtype=np.int8)
        return arr

    @staticmethod
    def __colour_char(char: str, colour: str):
        out = "\033["
        if colour == Board.red:
            out += "31m"
        elif colour == Board.blue:
            out += "34m"
        else:
            raise ValueError(f"board.py::Board::{colour} colour is not supported")

        out += char
        out += "\033[0m"
        return out

    

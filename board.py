import numpy as np

class Board:

    column = 7
    row = 6
    player = 1
    ai = 2
    
    def __init__(self):
        self.board = Board.__create_board(Board.row, Board.column)

    def update(self, row, col, turn):
        if turn == 'player':
            self.board[row][col] = 1
        elif turn == 'ai':
            self.board[row][col] = 0
        else:
            raise ValueError

    def print(self):
        for i in range(0, Board.row):
            for j in range(0, Board.column):
                print(f"{self.board[i][j]} ", end="")

            print()

        print("\n")

    @staticmethod
    def __create_board(row, col):

        arr = np.zeros((row, col), dtype=np.int8)
        return arr


    

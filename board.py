import numpy as np

class Board:

    player = 1
    ai = 2
    empty = 0
    
    def __init__(self, row: int=6, column: int=7):
        self.column = 7
        self.row = 6
        self.board = Board.__create_board(self.row, self.column)

    def update(self, row: int, col: int, turn: str):
        if turn == 'player':
            self.board[row][col] = 1
        elif turn == 'ai':
            self.board[row][col] = 0
        else:
            raise ValueError

    def print(self):
        for i in range(0, self.row):
            for j in range(0, self.column):
                if self.board[i][j] == Board.player:
                    print("\033[31mO\033[0m ", end="")
                elif self.board[i][j] == Board.ai:
                    print("\033[34mO\033[0m ", end="")
                else:
                    print(". ", end="")

            print()

        print("\n")

    @staticmethod
    def __create_board(row, col):

        arr = np.zeros((row, col), dtype=np.int8)
        return arr


    

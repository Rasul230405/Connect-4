import numpy as np

class Board:

    player = 1
    ai = 2
    full = 3
    empty = 0
    
    
    def __init__(self, row: int=6, column: int=7):
        self.column = column
        self.row = row
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
        # removes the the piece from board
        # just replaces the 'character' in [row][col] with Board.empty
        self._board[row][col] = Board.empty

    def get(self, row: int, col: int) -> int:
        # returns the 'character' in board[row][col]
        # 'character' is either Board.ai or Board.player
        return self._board[row][col]

    def is_full(self) -> bool:
        if not np.any(self._board):
            return True
        return False

    def print(self) -> None:
        for i in range(0, self.row):
            for j in range(0, self.column):
                if self._board[i][j] == Board.player:
                    print("\033[31mO\033[0m ", end="")
                elif self._board[i][j] == Board.ai:
                    print("\033[34mO\033[0m ", end="")
                else:
                    print(". ", end="")

            print()

        print("\n")

    @staticmethod
    def __create_board(row, col):# returns numpy array
        arr = np.zeros((row, col), dtype=np.int8)
        return arr


    

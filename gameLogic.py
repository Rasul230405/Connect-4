
from board import Board
from ai import AI

class ConnectFour:

    def __init__(self):
        self.board: Board = Board()
        self._AI: AI = AI()

    def ai_move(self) -> tuple(int, int):
        col = self._AI.move(self.board)
        row = self.gravity(col)
        
        while row == -1:
             col = self._AI.move(self.board)
             row = self.gravity(col)
        
        return self.update_board(row, col, 'ai')

    def player_move(self, col: int) -> tuple(int, int):
        if col < 0 or col >= Board.column:
            raise ValueError("out of range column\n")
        
        row = self.gravity(col)

        if row <= -1:
            raise ValueError("columns is full\n")

        else:
            return self.update_board(row, col, 'player')

    def gravity(self, col: int) -> int:
        # given a column returns the 'lowest' row which is not occupied
        # if column is full returns -1
        r = -1
        for i in range(Board.row-1, -1, -1):
            if self.board.board[i][col] == 0:
                r = i
                break

        return r


    def update_board(self, row: int, col: int, player: str) -> tuple(int, int):
        # updates the logical board, and returns the updated coordinates
       
        if player == 'player':
            self.board.board[row][col] = Board.player

        elif player == 'ai':
            self.board.board[row][col] = Board.ai
        else:
            raise ValueError
        
        return (row, col)

    def is_endgame(self, lm_row: int, lm_col: int) -> bool:
        # lm_row -> row number of last move
        # lm_col -> column number of last move
        # check for 5 directions: W, E, S, SW, SE
        # no need to check N direction, because rows are filled from South towards the North

       
        flag: bool = True
        ch: int = self.board.board[lm_row][lm_col]

        # S - vertical
        if lm_row <= 2:
            flag = True
            for i in range(lm_row + 1, Board.row):
                if self.board.board[i][lm_col] != ch:
                    flag = False
                    break

            if flag == True:
                return True

        # SW - diagonal
        if lm_row <= 2 and lm_col >= 3:
            flag = True
            for i in range(lm_row + 1, Board.row):
                if self.board.board[i][lm_col - (i - lm_row)] != ch:
                    flag = False
                    break

            if flag == True:
                return True

        # SE - diagonal
        if lm_row <= 2 and lm_col <= 3:
            flag = True
            for i in range(lm_row + 1, Board.row):
                if self.board.board[i][lm_col + (i - lm_row)] != ch:
                    flag = False
                    break

            if flag == True:
                return True


        # W
        if lm_col >= 3:
            flag = True
            for i in range(lm_col - 1, -1, -1):
                if self.board.board[lm_row][i] != ch:
                    flag = False
                    break

            if flag == True:
                return True

        # E
        if lm_col <=3:
            flag = True
            for i in range(lm_col + 1, Board.column):
               if self.board.board[lm_row][i] != ch:
                   flag = False
                   break

            if flag == True:
                return True


            
        return False

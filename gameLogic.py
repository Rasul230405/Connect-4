
from board import Board
from ai import AI
import numpy as np


class ConnectFour:

    neg_inf = -100
    pos_inf = 100
    
    def __init__(self, max_depth):
        self.board: Board = Board()
        self.max_depth = max_depth

    def ai_move(self) -> tuple(int, int):
       [row, col] = self.__think(self.board)
       return self.update_board(row, col, 'ai')

    def player_move(self, col: int) -> tuple(int, int):
        if col < 0 or col >= Board.column:
            raise ValueError("out of range column\n")
        
        row = ConnectFour.gravity(self.board, col)

        if row <= -1:
            raise ValueError("columns is full\n")

        else:
            return self.update_board(row, col, 'player')

    @staticmethod
    def gravity(board: Board, col: int) -> int:
        # given a column returns the 'lowest' row which is not occupied
        # if column is full returns -1
        r = -1
        for i in range(Board.row-1, -1, -1):
            if board.board[i][col] == 0:
                r = i
                break

        return r


    def update_board(self, row: int, col: int, player: str) -> tuple(int, int):
        # updates the logical board.board, and returns the updated coordinates
       
        if player == 'player':
            self.board.board[row][col] = Board.player

        elif player == 'ai':
            self.board.board[row][col] = Board.ai
        else:
            raise ValueError
        
        return (row, col)

    @staticmethod
    def is_endgame(board: Board, lm_row: int, lm_col: int) -> bool:
        # lm_row -> row number of last move
        # lm_col -> column number of last move
        # check for 7 directions:  NW, NE, W, E, S, SW, SE
        # no need to check N direction, because rows are filled from South towards the North

       
        flag: bool = True
        ch: int = board.board[lm_row][lm_col]

        # NW
        if lm_row <= 2 and lm_col >= 3:
            flag = True
            for i in range(lm_row + 1, lm_row + 4):
                if board.board[i][lm_col - (i - lm_row)] != ch:
                    flag = False
                    break

            if flag == True:
                return True

        # NE
        if lm_row <= 2 and lm_col <= 3:
            flag = True
            for i in range(lm_row + 1, lm_row + 4):
                if board.board[i][lm_col + (i - lm_row)] != ch:
                    flag = False
                    break

            if flag == True:
                return True

        # S - vertical
        if lm_row <= 2:
            flag = True
            for i in range(lm_row + 1, lm_row + 4):
                if board.board[i][lm_col] != ch:
                    flag = False
                    break

            if flag == True:
                return True

        # SW - diagonal
        if lm_row <= 2 and lm_col >= 3:
            flag = True
            for i in range(lm_row + 1, lm_row + 4):
                if board.board[i][lm_col - (i - lm_row)] != ch:
                    flag = False
                    break

            if flag == True:
                return True

        # SE - diagonal
        if lm_row <= 2 and lm_col <= 3:
            flag = True
            for i in range(lm_row + 1, lm_row + 4):
                if board.board[i][lm_col + (i - lm_row)] != ch:
                    flag = False
                    break

            if flag == True:
                return True


        # W
        if lm_col >= 3:
            flag = True
            for i in range(lm_col - 1, lm_col - 4, -1):
                if board.board[lm_row][i] != ch:
                    flag = False
                    break

            if flag == True:
                return True

        # E
        if lm_col <=3:
            flag = True
            for i in range(lm_col + 1, lm_col + 4):
               if board.board[lm_row][i] != ch:
                   flag = False
                   break

            if flag == True:
                return True


        return False

    
    def __generate_legal_moves(self, board: Board):
        # there is max number of columns moves at each turn
        all_moves = np.zeros((Board.column, 2), dtype=np.int8)

        for c in range(0, Board.column):
            row = ConnectFour.gravity(board, c)
            all_moves[c][0] = row
            all_moves[c][1] = c

        return all_moves

    def __minimax(self, board: Board, depth, is_max_player, lm_row, lm_col) -> tuple(int,int,int):
        # return the value of minimax
        if ConnectFour.is_endgame(board, lm_row, lm_col):
            if is_max_player:
                return ConnectFour.neg_inf
            else:
                return ConnectFour.pos_inf
        
        if depth == 0:
            return self.__evaluate(board)

        if is_max_player:
            value = ConnectFour.neg_inf
            all_moves = self.__generate_legal_moves(board)
           

            for i in range(0, all_moves.shape[0]):
                row = all_moves[i][0]
                col = all_moves[i][1]

                if row != -1:
                    board.board[row][col] = Board.player
                    value = max(value, self.__minimax(board, depth - 1, False, row, col))
                    board.board[row][col] = 0
                    
            return value
        
        else:
            value = ConnectFour.pos_inf
            all_moves = self.__generate_legal_moves(board)
            
            for i in range(0, all_moves.shape[0]):
                row = all_moves[i][0]
                col = all_moves[i][1]

                if row != -1:
                    board.board[row][col] = Board.ai
                    value = min(value, self.__minimax(board, depth - 1, True, row, col))
                    board.board[row][col] = 0
           
            return value
                           

    def __evaluate(self, board: Board):
        rng = np.random.default_rng()
        random_value = rng.integers(low=-100, high=100, size=1)
        
        return random_value[0]


    def __think(self, board: Board) -> tuple(int, int):
        all_moves = self.__generate_legal_moves(board)
        best_move = [-1, -1]
        best_evaluation = ConnectFour.neg_inf

        for i in range(0, all_moves.shape[0]):
            row = all_moves[i][0]
            col = all_moves[i][1]
            
            if row != -1:
                board.board[row][col] = Board.ai
                evaluate_move = -self.__minimax(board, self.max_depth, True, row, col)
                board.board[row][col] = 0

                if evaluate_move >= best_evaluation:
                    best_evaluation = evaluate_move
                    best_move[0] = row
                    best_move[1] = col


        return (best_move[0], best_move[1])

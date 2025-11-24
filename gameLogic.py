
# This file contains ConnectFourAI and ConnectFour classes and is_endgame() function


from board import Board
import numpy as np


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


class ConnectFourAI:

    
    neg_inf = -101
    pos_inf = 101

    def __init__(self, pruning: bool=True):
        self.pruning = pruning
        
    def think(self, board: Board, max_depth) -> tuple(int, int):
        all_moves = self.__generate_legal_moves(board)
        best_move = [-1, -1]
        best_evaluation = ConnectFourAI.neg_inf

        for i in range(0, all_moves.shape[0]):
            row = all_moves[i][0]
            col = all_moves[i][1]
            
            if row != -1:
                board.board[row][col] = Board.ai
                evaluate_move = -self.__minimax(board, max_depth, ConnectFourAI.neg_inf, ConnectFourAI.pos_inf, True, row, col)
                board.board[row][col] = 0

                if evaluate_move >= best_evaluation:
                    best_evaluation = evaluate_move
                    best_move[0] = row
                    best_move[1] = col


        return (best_move[0], best_move[1])

    
    def __generate_legal_moves(self, board: Board):
        # there is max number of columns moves at each turn
        all_moves = np.zeros((board.column, 2), dtype=np.int8)

        for c in range(0, board.column):
            row = ConnectFour.gravity(board, c)
            all_moves[c][0] = row
            all_moves[c][1] = c

        return all_moves

    
    def __minimax(self, board: Board, depth, alpha, beta, is_max_player, lm_row, lm_col) -> tuple(int,int,int):
        # return the value of minimax
        if is_endgame(board, lm_row, lm_col):
            if is_max_player:
                return ConnectFourAI.neg_inf
            else:
                return ConnectFourAI.pos_inf
        
        if depth == 0:
            return self.__evaluate(board)

        if is_max_player:
            value = ConnectFourAI.neg_inf
            all_moves = self.__generate_legal_moves(board)
           

            for i in range(0, all_moves.shape[0]):
                row = all_moves[i][0]
                col = all_moves[i][1]

                if row != -1:
                    board.board[row][col] = Board.player
                    value = max(value, self.__minimax(board, depth - 1, alpha, beta, False, row, col))
                    board.board[row][col] = 0
                    
                    if self.pruning:
                        alpha = max(alpha, value)
                        if beta <= alpha:
                            break
                    
            return value
        
        else:
            value = ConnectFourAI.pos_inf
            all_moves = self.__generate_legal_moves(board)
            
            for i in range(0, all_moves.shape[0]):
                row = all_moves[i][0]
                col = all_moves[i][1]

                if row != -1:
                    board.board[row][col] = Board.ai
                    value = min(value, self.__minimax(board, depth - 1, alpha, beta, True, row, col))
                    board.board[row][col] = 0

                    if self.pruning:
                        beta = min(beta, value)
                        if beta <= alpha:
                            break
           
            return value
                           

    def __evaluate(self, board: Board):
        rng = np.random.default_rng()
        random_value = rng.integers(low=-100, high=100, size=1)
        
        return random_value[0]



class ConnectFour:

    neg_inf = -100
    pos_inf = 100
    
    def __init__(self, difficulty_level: int):
        self.board: Board = Board(row=6, column=7)
        self.max_depth = difficulty_level

    def ai_move(self) -> tuple(int, int):
       AI = ConnectFourAI()
       [row, col] = AI.think(self.board, self.max_depth)
       return self.update_board(row, col, 'ai')

    def player_move(self, col: int) -> tuple(int, int):
        if col < 0 or col >= self.board.column:
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
        for i in range(board.row - 1, -1, -1):
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

    

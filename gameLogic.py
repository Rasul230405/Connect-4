

# This file contains ConnectFourAI and ConnectFour classes and is_endgame() function


from board import Board
import numpy as np


def is_endgame(board: Board, lm_row: int, lm_col: int) -> bool:
    # lm_row -> row number of last move
    # lm_col -> column number of last move
    # max 4 in horizontal direction, 1 in vertical direction, 6 in diagonal direction
    # no need to check North direction, because rows are filled from South towards the North
    flag: bool = True
    ch: int = board.board[lm_row][lm_col]

    # dont forget checking the case where board is full

    # S
    if lm_row <= 2:
        for i in range(lm_row + 1, lm_row + 4):
            if board.board[i][lm_col] != ch:
                flag = False
                break
        if flag == True:
            return True

    # Horizontal
    left = max(lm_col - 3, 0)
    right = min(lm_col + 3, board.column - 1)

    while left + 3 <= right:
        flag = True
        for i in range(0, 4):
            if board.board[lm_row][left + i] != ch:
                flag = False
                break

        if flag == True:
            return True

        left += 1

    # diagonal: NW + SE. starting from the upper left coordinate
    min_coord = min(lm_row, lm_col)
    left_row = lm_row - min_coord
    left_col = lm_col - min_coord

    while left_col + 3 < board.column and left_row + 3 < board.row:
        flag = True
        for i in range(0, 4):
            if board.board[left_row + i][left_col + i] != ch:
                flag = False
                break
            
        if flag == True:
            return True

        left_col += 1
        left_row += 1

    # diagonal: SW + NE. starting from the upper right coordinate
    min_coord = min(lm_row, board.column - 1 - lm_col) #  board.column - 1, because index from 0
    right_row = lm_row - min_coord
    right_col = lm_col + min_coord

    while right_row + 3 < board.row and right_col - 3 >= 0:
        flag = True
        for i in range(0, 4):
            if board.board[right_row + i][right_col - i] != ch:
                flag = False
                break
        if flag == True:
            return True

        right_row += 1
        right_col -= 1

       
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
                evaluate_move = self.__minimax(board, max_depth, ConnectFourAI.neg_inf, ConnectFourAI.pos_inf, False, row, col)
                board.board[row][col] = 0

                if evaluate_move >= best_evaluation:
                    best_evaluation = evaluate_move
                    best_move[0] = row
                    best_move[1] = col

                print(f"{i + 1}'th move is ({row}, {col}),  minimax value: {best_evaluation}")


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
            return self.evaluate(board)

        if is_max_player:
            value = ConnectFourAI.neg_inf
            all_moves = self.__generate_legal_moves(board)
           

            for i in range(0, all_moves.shape[0]):
                row = all_moves[i][0]
                col = all_moves[i][1]

                if row != -1:
                    board.board[row][col] = Board.ai
                    value = max(value, self.__minimax(board, depth - 1, alpha, beta, False, row, col))
                    board.board[row][col] = 0
                    
                    if self.pruning:
                        alpha = max(alpha, value)
                        if beta <= alpha:
                            break
                        
                    #print(f"depth: {5 - depth + 1}, minimax_value: {value}")
                    
            return value
        
        else:
            value = ConnectFourAI.pos_inf
            all_moves = self.__generate_legal_moves(board)
            
            for i in range(0, all_moves.shape[0]):
                row = all_moves[i][0]
                col = all_moves[i][1]

                if row != -1:
                    board.board[row][col] = Board.player
                    value = min(value, self.__minimax(board, depth - 1, alpha, beta, True, row, col))
                    board.board[row][col] = 0

                    if self.pruning:
                        beta = min(beta, value)
                        if beta <= alpha:
                            break
           
            return value
                           

    def evaluate(self, board: Board):

        score_max_p = 80    # 7*4 + 7*4 + 4*3 + 4*3
        score_min_p = 80    # 7*4 + 7*4 + 4*3 + 4*3

        for i in range(0, board.row):
            for j in range(0, board.column):
                ch = board.board[i][j]
                if ch != Board.empty:
                    
                     ch_opponent = -1
                     if ch == Board.ai:
                         ch_opponent = Board.player
                     else:
                         ch_opponent = Board.ai

                     # Vertical
                     vertical = 0
                     lower_row = max(i - 3, 0)
                     upper_row = min(i + 3, board.row - 1)

                     while lower_row + 3 <= upper_row:
                         flag = True
                         for k in range(0, 4):
                             if board.board[lower_row + k][j] == ch_opponent:
                                 flag = False
                                 break

                         if flag == True:
                             vertical += 1
                         lower_row += 1

                     if (ch == Board.ai):
                         score_min_p -= vertical

                     else:
                         score_max_p -= vertical


                     # horizontal
                     horizontal = 0
                     left = max(j - 3, 0)
                     right = min(j + 3, board.column - 1)

                     while left + 3 <= right:
                         flag = True
                         for k in range(0, 4):
                             if board.board[i][left + k] == ch_opponent:
                                 flag = False
                                 break

                         if flag == True:
                             horizontal += 1

                         left += 1

                     if (ch == Board.ai):
                         score_min_p -= horizontal
                     else:
                         score_max_p -= horizontal


                     # diagonal: NW + SE
                     diagonal_1 = 0
                     min_coord = min(i, j)
                     up_left_row = i - min_coord
                     up_left_col = j - min_coord

                     while up_left_col + 3 < board.column and up_left_row + 3 < board.row:
                         flag = True
                         for k in range(0, 4):
                             if board.board[up_left_row + k][up_left_col + k] == ch_opponent:
                                 flag = False
                                 break

                         if flag == True:
                             diagonal_1 += 1

                         up_left_col += 1
                         up_left_row += 1

                     if (ch == Board.ai):
                         score_min_p -= diagonal_1
                     else:
                         score_max_p -= diagonal_1


                     # diagonal: SW + NE. starting from the upper right coordinate
                     diagonal_2 = 0
                     min_coord = min(i, board.column - 1 - j) #  board.column - 1, because index from 0
                     up_right_row = i - min_coord
                     up_right_col = j + min_coord

                     while up_right_row + 3 < board.row and up_right_col - 3 >= 0:
                         flag = True
                         for k in range(0, 4):
                             if board.board[up_right_row + k][up_right_col - k] == ch_opponent:
                                 flag = False
                                 break

                         if flag == True:
                             diagonal_2 += 1

                         up_right_row += 1
                         up_right_col -= 1                    

                     if (ch == Board.ai):
                         score_min_p -= diagonal_2
                     else:
                         score_max_p -= diagonal_2


        return score_max_p - score_min_p

    

class ConnectFour:

    neg_inf = -100
    pos_inf = 100
    
    def __init__(self, difficulty_level: int):
        self.board: Board = Board(row=6, column=7)
        self.AI = ConnectFourAI()
        self.max_depth = difficulty_level

    def ai_move(self) -> tuple(int, int):
       [row, col] = self.AI.think(self.board, self.max_depth)
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

    

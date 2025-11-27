

# This file contains ConnectFour class

import numpy as np
from board import Board
from board_game_AI import BoardGameAI

class ConnectFour:

    max_eval = 80
    min_eval = -80
    
    def __init__(self, difficulty_level: int=3):
        self.board: Board = Board(row=6, column=7)
        
        self.AI = BoardGameAI(ConnectFour.__evaluation_func,
                              ConnectFour.max_eval,
                              ConnectFour.min_eval,
                              ConnectFour.is_endgame,
                              ConnectFour.__generate_legal_moves)
        
        self.max_depth = difficulty_level

    def ai_move(self) -> tuple(int, int):
       [row, col] = self.AI.think(self.board, self.max_depth)
       self.board.set(row, col, Board.ai)
       return (row, col)

    def player_move(self, col: int) -> tuple(int, int):
        if col < 0 or col >= self.board.column:
            raise ValueError("out of range column\n")
        
        row = ConnectFour.gravity(self.board, col)

        if row <= -1:
            raise ValueError("columns is full\n")

        else:
            self.board.set(row, col, Board.player)
            return (row, col)

    @staticmethod
    def gravity(board: Board, col: int) -> int:
        # given a column returns the 'lowest' row which is not occupied
        # if column is full returns -1
        row = -1
        for i in range(board.row - 1, -1, -1):
            if board.get(i, col) == 0:
                row = i
                break

        return row

    @staticmethod
    def __generate_legal_moves(board: Board):
        # there is max board.columns moves at each turn
        all_moves = np.zeros((board.column, 2), dtype=np.int8)

        for c in range(0, board.column):
            row = ConnectFour.gravity(board, c)
            all_moves[c][0] = row
            all_moves[c][1] = c

        return all_moves

    
    @staticmethod
    def __evaluation_func(board: Board) -> int:

        score_max_p = 80    # 7*4 + 7*4 + 4*3 + 4*3
        score_min_p = 80    # 7*4 + 7*4 + 4*3 + 4*3

        for i in range(0, board.row):
            for j in range(0, board.column):
                ch = board.get(i, j)
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
                             if board.get(lower_row + k, j) == ch_opponent:
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
                             if board.get(i, left + k) == ch_opponent:
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
                             if board.get(up_left_row + k, up_left_col + k) == ch_opponent:
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
                             if board.get(up_right_row + k, up_right_col - k) == ch_opponent:
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


    @staticmethod
    def is_endgame(board: Board, lm_row: int, lm_col: int) -> int:

        # returns 1 if any player wins, -1 if it is draw, 0 if it is not endgame

        # lm_row -> row number of last move
        # lm_col -> column number of last move

        # no need to check all possible combinations of end game. By knowing the last move, it is
        # more efficient to only check the possible ending combinations which the last move created

        # max 4 in a row in horizontal direction, 1 in a row in vertical direction, max 6 in a row in diagonal direction
        # no need to check North direction, because rows are filled from South towards the North
        
        def check_south(board: Board, lm_row: int, lm_col: int) -> bool:
            ch: int = board.get(lm_row, lm_col)

            if lm_row <= 2:
                flag = True
                for i in range(lm_row + 1, lm_row + 4):
                    if board.get(i, lm_col) != ch:
                        flag = False
                        break
                if flag == True:
                    return True

            return False

        def check_horizontal(board, lm_row, lm_col) -> bool:

            ch: int = board.get(lm_row, lm_col)
            left = max(lm_col - 3, 0)
            right = min(lm_col + 3, board.column - 1)

            while left + 3 <= right:
                flag = True
                for i in range(0, 4):
                    if board.get(lm_row, left + i) != ch:
                        flag = False
                        break

                if flag == True:
                    return True

                left += 1

            return False


        def check_diagonals(board, lm_row, lm_col) -> bool:

            ch: int = board.get(lm_row, lm_col)
            # diagonal: NW + SE. starting from the upper left coordinate
            min_coord = min(lm_row, lm_col)
            left_row = lm_row - min_coord
            left_col = lm_col - min_coord

            while left_col + 3 < board.column and left_row + 3 < board.row:
                flag = True
                for i in range(0, 4):
                    if board.get(left_row + i, left_col + i) != ch:
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
                    if board.get(right_row + i, right_col - i) != ch:
                        flag = False
                        break
                if flag == True:
                    return True

                right_row += 1
                right_col -= 1

            return False

        
        if check_south(board, lm_row, lm_col):
            return 1

        if check_horizontal(board, lm_row, lm_col):
            return 1

        if check_diagonals(board, lm_row, lm_col):
            return 1

        # when board is full and there is no winner - draw
        if board.is_full():
            return -1

        return 0

    

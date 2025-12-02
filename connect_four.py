
# This file contains the implementation of ConnectFour class

"""
This class manages the game logic of Connect4 game.
The only public functions are ai_move(), player_move(), and is_endgame() 

player_move() takes column numberas an argument and returns a tuple of form (row, column) 
that represents the coordinates of the player's move after the gravity is applied at the 
column that is passed as an argument.

ai_moves() returns the AI move, takes no argument

is_endgame() ,as the name implies, checks if game ended or not after the last move

Other functions are used for deciding the move of AI at each turn 
"""

import numpy as np
from board import Board
from board_game_AI import BoardGameAI


class ConnectFour:

    max_eval = 80
    min_eval = -80
    
    def __init__(self, p_colour: str, difficulty_level: int=3, n_row: int=6,
                 n_column: int=7):
        self.board: Board = Board(row=n_row, column=n_column, p_colour=p_colour)
        
        self.AI = BoardGameAI(ConnectFour.evaluation_func,
                              ConnectFour.max_eval,
                              ConnectFour.min_eval,
                              ConnectFour.is_endgame,
                              ConnectFour.generate_legal_moves)
        
        self.max_depth: int = difficulty_level

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
        # given a column returns the bottom row which is not occupied
        # if column is full returns -1
        row = -1
        for i in range(board.row - 1, -1, -1):
            if board.get(i, col) == 0:
                row = i
                break

        return row

    @staticmethod
    def generate_legal_moves(board: Board) -> List[List[int, int]]:
        # returns all the possible moves at each turn
        
        def gravity_l(board: Board, col: int) -> int:
           # given a column returns the bottom row which is not occupied
           # if column is full returns -1
           row = -1
           for i in range(board.row - 1, -1, -1):
               if board.get(i, col) == 0:
                   row = i
                   break

           return row

        all_moves = []

        for c in range(0, board.column):
            row = gravity_l(board, c)
            if row != -1:
                all_moves.append([row, c])
                
        return all_moves

    
    @staticmethod
    def evaluation_func(board: Board) -> int:
        """
        Evaluation function checks for possible 4 in rows that each player can make and subtract
        that from each other's scores.
        Each player starts with the max score of 80: 
        7*4 (horizontal) + 7*4 (vertical) + 4*3 (diagonal1) + 4*3 (diagonal2) = 80

        diagonal1 refers to the diagonal : [top left to bottom right]
        diagonal2 refers to the diagonal : [top right to bottom left]

        Example: Let's say AI makes a move to the bottom middle cell. Now AI has 4 (horizontal) +
        + 1 (vertical) + 1 (diagonal1) + 1 (diagonal2) = 7 possible 4 in rows. So we subtract 7
        from the score of player 80 - 7 = 73.
        Instead of the bottom middle cell, AI could have made a move to bottom left corner. Then
        1 (horizontal) + 1 (vertical) + 1 (diagonal2) = 3. 80 - 3 = 77. AI would have decreased
        the score of player just by 3.


        Brief explanation of the implementation: 
        at each cell first we check if there is a tile placed or not. If there is a tile, we 
        start counting possible 4 in rows for 4 directions specified above.
        The one way of doing this is using loop, starting from the cell that is in 3 
        cell away from the current tile. Because that cell would be the leftmost or rightmost 
        cell that can potentially create a 4 in row with the current tile. The loop should end 
        again in the cell that is in 3 cells away from the current tile but in the opposite
        direction. 
        We have to check that the cases where +-3 can go outside of the board, and adjust them.
        In the example below '2' represent a tile, and 'x's are the starting points of potential
        4 in rows

                           0 1 2 3 4 5 6
                           _____________
                        0 |x 0 0 x 0 0 x
                        1 |0 x 0 x 0 x 0 
                        2 |0 0 x x x 0 0 
                        3 |x x x 2 0 0 0 
                        4 |0 0 0 0 0 0 0 
                        5 |0 0 0 0 O 0 0
        """
        
        score_max_p = 80    # 7*4 (horizontal) + 7*4 (vertical) + 4*3 (diagonal) + 4*3 (diagonal)
        score_min_p = 80    # 7*4 (horizontal) + 7*4 (vertical) + 4*3 (diagonal) + 4*3 (diagonal)

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
                     # find the starting point for row, so that we can loop over starting from
                     # this row which is the max of 3 row above and 0.
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
                     # find the leftmost column, so that we can start the loop from this column
                     # which is the max of 3 columns left and 0.
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
                     up_left_row = i - min(3, min_coord)
                     up_left_col = j - min(3, min_coord)

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
                     min_coord = min(i, board.column - 1 - j) #  board.column - 1, because indexing is from 0
                      # start from the cell that is in 3 cells distance from the current cell in diagonal
                     up_right_row = i - min(min_coord, 3)
                     up_right_col = j + min(min_coord, 3) 

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

        # max 4 ending combinations in a horizontal direction, always 1 in a vertical direction (south), max 6 in diagonal directions
        # no need to check North direction, because rows are filled from South towards the North
        
        def check_south(board: Board, lm_row: int, lm_col: int) -> bool:
            ch: int = board.get(lm_row, lm_col)

            if lm_row <= (board.row - 4):
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


    def print_game_stats(self):
        filename = f"ai_perf_{self.max_depth}.csv"
        self.AI.print_AI_stats(filename)

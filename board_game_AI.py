# This file contains the implementation of BoardGameAI class

"""
BoardGameAI class can be used in any SIMPLE board game (ConnectFour, tic tac toe etc.) 
to implement AI moves. Underlying algorithm used is minimax with alpha-beta pruning, but 
pruning can be turned off by passing pruning=False when creating object of the class (why 
would anyone do that?). Additionally each game has to provide its own evaluation function, 
endgame function, a function for generating all the legal moves at each turn, and max and min
values of evaluation.

For getting the best move for AI at the turn just use
think() function which returns a tuple(row, column)

User of this class only needs to use think() function
"""

from board import Board

class BoardGameAI:

    def __init__(self, evaluation_func, endgame_func, legal_moves_func, pruning: bool=True):
        self._pos_inf = float("inf")
        self._neg_inf = float("-inf")
        
        self.evaluation_func = evaluation_func
        self.endgame_func = endgame_func
        self.legal_moves_func = legal_moves_func
        
        self.pruning = pruning
        self._max_depth = 0
        
    def think(self, board: Board, max_depth: int=3) -> tuple(int, int):
        # check all moves and return the move with highest minimax value
        # use this function for generating AI move for the game
        self._max_depth = max_depth
        move_scores = []
        
        all_moves = self.legal_moves_func(board)
        best_move = [-1, -1]
        best_evaluation = self._neg_inf

        for i in range(0, len(all_moves)):
            row = all_moves[i][0]
            col = all_moves[i][1]
            
            board.set(row, col, Board.ai)
            evaluate_move = self.__minimax(board, max_depth, self._neg_inf, self._pos_inf, False, row, col)
            board.remove(row, col)

            if evaluate_move >= best_evaluation:
                best_evaluation = evaluate_move
                best_move[0] = row
                best_move[1] = col

            print(f"{i + 1}'th move is ({row}, {col}),  minimax value: {evaluate_move}")
            move_scores.append([(row, col), evaluate_move])

        print()
        
        # print all the moves and their score again
        print("High Level summary of moves:")
        for i in range(0, len(move_scores)):
            print(f"{i + 1}'th move is {move_scores[i][0]}, ",end="")

            val = move_scores[i][1]
            if val == self._pos_inf:
                print("its score is +inf")
            elif val == self._neg_inf:
                print("its score is -inf")
            else:
                print(f"its score is {val}")
                
        return (best_move[0], best_move[1])

    
    def __minimax(self, board: Board, depth: int, alpha: int, beta: int, is_max_player: bool, lm_row: int, lm_col: int) -> int:
        # returns the value of minimax

        # game ends with a winner
        endgame = self.endgame_func(board, lm_row, lm_col)
        if endgame == 1:
            if is_max_player:
                return self._neg_inf 
            else:
                return self._pos_inf - (self._max_depth - depth) # win sooner. higher depth is better

        # draw
        if endgame == -1:
            return 0
        
        # max depth reached 
        if depth == 0:
            return self.evaluation_func(board) 

        if is_max_player:
            value = self._neg_inf

            # generate all the legal moves at this turn
            all_moves = self.legal_moves_func(board)
           
            
            for i in range(0, len(all_moves)):
                row = all_moves[i][0]
                col = all_moves[i][1]

                board.set(row, col, Board.ai)
                value = max(value, self.__minimax(board, depth - 1, alpha, beta, False, row, col))
                board.remove(row, col)

                alpha = max(alpha, value)
                
                if self.pruning:
                    
                    if beta <= alpha:
                        print(f"Depth {self._max_depth - depth + 1}, Move: ({row}, {col}), Minimax value: ", end="")
                        # print infinity values in a nice fromat
                        self.__print_val(value)
                        print()
                        print(f"beta is {beta}, alpha is {alpha}")
                        print(f"Depth {self._max_depth - depth + 1}, {len(all_moves) - i - 1} branches pruned.")
                        
                        break
                
                    
                print(f"Depth {self._max_depth - depth + 1}, Move: ({row}, {col}), Minimax value:", end="")
                self.__print_val(value)
                print()
                print(f"beta is {beta}, alpha is {alpha}")

            return value
        
        else:
            value = self._pos_inf
            all_moves = self.legal_moves_func(board)
            
            for i in range(0, len(all_moves)):
                row = all_moves[i][0]
                col = all_moves[i][1]

                board.set(row, col, Board.player)
                value = min(value, self.__minimax(board, depth - 1, alpha, beta, True, row, col))
                board.remove(row, col)
                beta = min(beta, value)
                
                if self.pruning:
                    
                    if beta <= alpha:
                        print(f"Depth {self._max_depth - depth + 1}, Move: ({row}, {col}), Minimax value: ", end="")
                        # print infinity values in a nice fromat
                        self.__print_val(value)
                        print()
                        print(f"beta is {beta}, alpha is {alpha}")
                        print(f"Depth {self._max_depth - depth + 1}, {len(all_moves) - i - 1} branches pruned.")
                        
                        break
                    

                print(f"Depth {self._max_depth - depth + 1}, Move: ({row}, {col}), Minimax value:", end="")
                self.__print_val(value)
                print()
                print(f"beta is {beta}, alpha is {alpha}")


            return value
                           
        
    def __print_val(self, val: int) -> None:
        if val == self._pos_inf:
            print(f"+inf", end="")
        elif val == self._neg_inf:
            print(f"-inf", end="")
        else:
            print(f"{val}", end="")

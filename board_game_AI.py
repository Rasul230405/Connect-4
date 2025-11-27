
from board import Board

class BoardGameAI:


    def __init__(self, evaluation_func, max_eval, min_eval, endgame_func, legal_moves_func, pruning: bool=True):
        self._pos_inf = max_eval + 1
        self._neg_inf = min_eval - 1
        self.evaluation_func = evaluation_func
        self.endgame_func = endgame_func
        self.legal_moves_func = legal_moves_func
        self.pruning = pruning
        
    def think(self, board: Board, max_depth: int=3) -> tuple(int, int):
        
        all_moves = self.legal_moves_func(board)
        best_move = [-1, -1]
        best_evaluation = self._neg_inf

        for i in range(0, all_moves.shape[0]):
            row = all_moves[i][0]
            col = all_moves[i][1]
            
            if row != -1:
                board.set(row, col, Board.ai)
                evaluate_move = self.__minimax(board, max_depth, self._neg_inf, self._pos_inf, False, row, col)
                board.remove(row, col)

                if evaluate_move >= best_evaluation:
                    best_evaluation = evaluate_move
                    best_move[0] = row
                    best_move[1] = col

                print(f"{i + 1}'th move is ({row}, {col}),  minimax value: {best_evaluation}")


        return (best_move[0], best_move[1])

    
    def __generate_legal_moves_func_func(self, board: Board):
        # there is max number of columns moves at each turn
        all_moves = np.zeros((board.column, 2), dtype=np.int8)

        for c in range(0, board.column):
            row = ConnectFour.gravity(board, c)
            all_moves[c][0] = row
            all_moves[c][1] = c

        return all_moves

    
    def __minimax(self, board: Board, depth: int, alpha: int, beta: int, is_max_player: bool, lm_row: int, lm_col: int) -> int:
        # return the value of minimax
        endgame = self.endgame_func(board, lm_row, lm_col)
        if endgame == 1:
            if is_max_player:
                return self._neg_inf
            else:
                return self._pos_inf

        if endgame == -1:
            return 0
        
        if depth == 0:
            return self.evaluation_func(board)

        if is_max_player:
            value = self._neg_inf
            all_moves = self.legal_moves_func(board)
           

            for i in range(0, all_moves.shape[0]):
                row = all_moves[i][0]
                col = all_moves[i][1]

                if row != -1:
                    board.set(row, col, Board.ai)
                    value = max(value, self.__minimax(board, depth - 1, alpha, beta, False, row, col))
                    board.remove(row, col)
                    
                    if self.pruning:
                        alpha = max(alpha, value)
                        if beta <= alpha:
                            break
                        
                    #print(f"depth: {5 - depth + 1}, minimax_value: {value}")
                    
            return value
        
        else:
            value = self._pos_inf
            all_moves = self.legal_moves_func(board)
            
            for i in range(0, all_moves.shape[0]):
                row = all_moves[i][0]
                col = all_moves[i][1]

                if row != -1:
                    board.set(row, col, Board.player)
                    value = min(value, self.__minimax(board, depth - 1, alpha, beta, True, row, col))
                    board.remove(row, col)

                    if self.pruning:
                        beta = min(beta, value)
                        if beta <= alpha:
                            break
           
            return value
                           


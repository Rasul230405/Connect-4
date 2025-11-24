from board import Board
import numpy as np

class AI:

    def move(self, board: Board) -> int:
       rng = np.random.default_rng()

       col = rng.integers(low=0, high=Board.column, size=1)[0]

       return col

    def __minimax(self):
        pass

    def __evaluate(self):
        pass

  


    



import pytest
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from board import Board
from gameLogic import ConnectFourAI

def test_evaluation_one():
    B = Board()
    AI = ConnectFourAI()
    
    # put tile to the lower leftmost corner
    B.update(B.row - 1, 0, 'ai')   
    assert AI.evaluate(B) == 5

    
    # put tile to the lower middle column
    B.update(B.row - 1, 3, 'player')
    B.print()
    assert AI.evaluate(B) == -2


    
    

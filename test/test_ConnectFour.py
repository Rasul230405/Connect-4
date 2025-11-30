
import pytest
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from board import Board
from connect_four import ConnectFour

def test_player_move():
    C4 = ConnectFour(3)

    moves = [
        [0, (5, 0)],
        [1, (5, 1)],
        [2, (5, 2)],
        [2, (4, 2)],
        [1, (4, 1)],
        [2, (3, 2)],
        [2, (2, 2)]
    ]

    for col, expected in moves:
        assert C4.player_move(col) == expected

def test_illegal__moves():
    C4 = ConnectFour(3)

    # fill one column completely and then test what happens if another pile is put there
    for i in range(0, 6):
        C4.player_move(0)
    
    moves = [0, -1, 8]

    for m in moves:
        with pytest.raises(ValueError):
            C4.player_move(m)

            
def test_evaluation_function():    
    boards = []
    expected = []
    
    b1 = Board()
    b1.set(5, 0, Board.ai)
    b1.set(5, 3, Board.ai)
    boards.append(b1)
    expected.append(10)

    b2 = Board()
    b2.set(5, 5, Board.ai)
    boards.append(b2)
    expected.append(4)

    b3 = Board()
    b3.set(5, 5, Board.ai)
    b3.set(5, 3, Board.player)
    b3.set(5, 1, Board.ai)
    boards.append(b3)
    expected.append(1)

    b4 = Board()
    b4.set(5, 0, Board.ai)
    b4.set(5, 6, Board.player)
    boards.append(b4)
    expected.append(0)

    b5 = Board()
    b5.set(5, 3, Board.ai)
    b5.set(4, 5, Board.ai)
    b5.set(3, 3, Board.ai)
    b5.set(5, 0, Board.player)
    b5.set(4, 0, Board.player)
    b5.set(3, 0, Board.player)
    boards.append(b5)
    expected.append(14)
    
    for i in range(0, 5):
        assert ConnectFour.evaluation_func(boards[i]) == expected[i]

    

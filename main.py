
from gameLogic import ConnectFour, is_endgame


def game_loop(flag, game) -> None:

    player_turn = 1
    
    game.board.print()
    
    while flag:   
        
        col = 0
        row = 0

        if player_turn:
            while True:
                try:
                    col = int(input(f"Enter the column to which you want to put a disc: ")) 
                    [row, col] = game.player_move(col)
                    break
                except ValueError as e:
                    print(f"Error: {e}")
        else:
            
             [row, col] = game.ai_move()
             
        
        game.board.print()

        if is_endgame(game.board, row, col):
            flag = False
            if not player_turn:
                print("You Lost!")

            else:
                print("You won!")

        player_turn = not player_turn
            
        

        
connect4 = ConnectFour(difficulty_level=5)
game_loop(True, connect4)

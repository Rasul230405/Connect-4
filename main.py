
from gameLogic import ConnectFour


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
             print(f"AI moves: {[row, col]}\n")
        
        game.board.print()

        if ConnectFour.is_endgame(game.board, row, col):
            flag = False
            if not player_turn:
                print("You Lost!")

            else:
                print("You won!")

        player_turn = not player_turn
            
        

        
connect4 = ConnectFour(max_depth=5)
game_loop(True, connect4)

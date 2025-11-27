
from connect_four import ConnectFour


def game_loop(flag, game) -> None:

    
    game.board.print()
    player_turn = 0
    
    while flag:   
        
        col = 0
        row = 0

        # keep prompting for the column number until it is valid column number
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
        endgame = ConnectFour.is_endgame(game.board, row, col)
        
        if endgame == 1:
            flag = False
            if not player_turn:
                print("You Lost!")

            else:
                print("You won!")
        if endgame == -1:
            flag = False
            print("Draw!")

        player_turn = not player_turn
            
        

        
connect4 = ConnectFour(difficulty_level=6)
game_loop(True, connect4)

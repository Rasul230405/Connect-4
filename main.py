# This file executes the Connect4 game

from connect_four import ConnectFour
import argparse
import sys

def game_loop(game: ConnectFour, player_turn: int=1) -> None:
    
    flag = True # to control the game loop
    
    # display the intial board before player makes a move
    if player_turn:
        game.board.display()
    
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
             
        game.board.display()
        endgame = ConnectFour.is_endgame(game.board, row, col)
        
        if endgame == 1:
            flag = False
            if not player_turn:
                print("You Lost. Hades awaits to escort you to the Underworld! Do pay my respects to Sophocles there - his tragedies rival your gameplay!")

            else:
                print("Congrats, You won! You are the smartest person in the world now!")
        if endgame == -1:
            flag = False
            print("Draw! Humanity still have a chance against AI!")

        player_turn = not player_turn
            
        

# parse the command line arguments
parser =  argparse.ArgumentParser()

parser.add_argument("-d", "--difficulty_level", type=int, help="difficulty level of the game. between [0-15]",
                    default = 5)
parser.add_argument("-c", "--colour", type=str, help="colour of the player's tiles. r for red, b for blue",
                    default = 'r')
parser.add_argument("-t", "--turn", type=int, help="1 for taking first turn, 0 for not taking first turn",
                    default = 0)
parser.add_argument("-r", "--n_rows", type=int, help="number of rows in a board. must be between [4-30]",
                    default = 6)
parser.add_argument("-cols", "--n_columns", type=int, help="number of rows in a board. must be between [4-30]",
                    default = 7)

args = parser.parse_args()

# check the command line arguments
if args.difficulty_level < 0 or args.difficulty_level > 15:
    print(f"difficulty level must be between [0-15]. You entered {args.difficulty_level}")
    sys.exit(1)

if args.colour != 'r' and args.colour != 'b':
    print(f"colour must be either r or b. You entered {args.colour}")
    sys.exit(1)
    
if args.turn != 1 and args.turn != 0:
    print(f"turn must be set to either 1 or 0. You entered {args.turn}")
    sys.exit(1)

if args.n_rows < 4 or args.n_rows > 30:
    print(f"number of rows must be between [4-30]. You entered {args.n_rows}")
    sys.exit(1)
    
if args.n_columns < 4 or args.n_columns > 30:
    print(f"number of columns must be between [4-30]. You entered {args.n_columns}")
    sys.exit(1)

    
# run the game
connect4 = ConnectFour(difficulty_level=args.difficulty_level, n_row=args.n_rows,
                       n_column=args.n_columns, p_colour=args.colour)
game_loop(connect4, args.turn)

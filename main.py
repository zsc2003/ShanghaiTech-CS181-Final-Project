import pygame
import pygame_menu
from utils.config import WIDTH ,HEIGHT, SIZE, BLACK, WHITE, POSI_INFI, NEGA_INFI
from utils.draught_game import Game

from algorithms.minimax import minimax, negamax, alpha_beta_pruning
# from algorithms.reforcement_learning import reforcement_learning

depth = 3         # search depth
ai_turn = BLACK   # the color for the ai piece
algorithm = 1     # search algorithm

# select algorithm for AI
def select_algorithm(value, index):
    global algorithm
    algorithm = index

# select the color for the player
def select_turn(value, index):
    global ai_turn
    if index == 2:
        ai_turn = WHITE
    else:
        ai_turn = BLACK


# select the depth for searching
def select_depth(value, index):
    global depth
    depth = index


# run draught
def run_game():
    global depth, ai_turn, algorithm
    is_run = True

    # initialize
    if ai_turn == BLACK:
       game = Game(window, WHITE)
    else:
        game = Game(window, BLACK)
    
    while is_run:
        for event in pygame.event.get():
            # Esc to quit the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_run = False 
            
            # judge the turn
            if game.turn == ai_turn:
                if algorithm == 1: # random
                    pass
                    # current it is negamax
                    score, new_board = negamax([0], game.board, ai_turn, depth, game)
                elif algorithm == 2: # search
                    score, new_board = alpha_beta_pruning([0], game.board, ai_turn, NEGA_INFI, POSI_INFI, depth, game)              
                elif algorithm == 3: # reforcement learning
                    raise ValueError("reforcement learning is under construction")
                elif algorithm == 4: # MCTS
                    raise ValueError("MCTS is under construction")
                else:
                    raise ValueError("Unconstructed algorithm")
                
                if new_board:
                    game.ai_move(new_board)
            else:
                game.get_moves()

            # judge if anyone wins
            if game.board.winner() != None:
                game.draw_winner()
                is_run = False
            
            # select and move the pieces
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x , y = pos
                game.after_click(y // SIZE, x // SIZE)
        
        game.update()


if __name__ == '__main__':
    pygame.init()

    window = pygame.display.set_mode((WIDTH,HEIGHT))

    # initialize menu
    font = pygame_menu.font.FONT_NEVIS
    menu = pygame_menu.Menu('Welcome',
                            400,
                            300,
                            theme=pygame_menu.themes.THEME_SOLARIZED,
                            )

    algorithm_list = [('random', 1),
                      ('search', 2),
                      ('reforcement', 3),
                      ('MCTS', 4),
                     ]

    menu.add.selector('Algorithm : ', algorithm_list,
                      onchange=select_algorithm, font_name=font)
    menu.add.selector('My Turn : ', [('WHITE',1), ('BLACK',2)],
                      onchange=select_turn, font_name=font)
    menu.add.selector('Depth : ', [(f'{i}', i) for i in range(1, 11)],
                      onchange=select_depth, font_name=font, default=2)

    menu.add.button('Play', run_game, font_name=font)
    menu.add.button('Quit', pygame_menu.events.EXIT, font_name=font)

    menu.mainloop(window)

    run_game()
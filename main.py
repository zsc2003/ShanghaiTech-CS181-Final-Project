import pygame
import pygame_menu
from utils.config import WIDTH ,HEIGHT, SIZE, BLACK, WHITE, POSI_INFI, NEGA_INFI
from utils.draught import Game
# from algorithms.AI import  negamax, alpha_beta_pruning
from algorithms.minimax import minimax, negamax, alpha_beta_pruning


depth = 4   #搜索深度,默认搜索4层
ai_turn = BLACK   #AI棋子的颜色
algorithm = 1     #搜索算法,1为negamax;2为alpha-bate pruning

#选择使用的搜索算法
def select_algorithm(value, index):
    global algorithm
    algorithm = index

#选择自己棋子的颜色
def select_turn(value, index):
    print(index)
    global ai_turn
    if index == 2:
        ai_turn = WHITE
    else:
        ai_turn = BLACK

#设置搜索深度
def set_depth(value):
    global depth
    #如果输入字符串为纯数字，将深度设为该数字；否则使用默认深度
    if value.isdigit():
        value_ = int(value)
        #搜索深度为奇数时，最后一层无意义
        if value_ % 2:
            depth = value_ - 1
        else:
            depth = value_

#运行跳棋ai游戏
def run_game():
    global depth,ai_turn,algorithm
    is_run = True
    #初始化游戏类
    if ai_turn == BLACK:
       game = Game(window,WHITE)
    else:
        game = Game(window,BLACK)
    
    while is_run:
        for event in pygame.event.get():
            #当按Esc时退出游戏
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_run = False 
            
            #判断当前是玩家还是ai的回合
            if game.turn == ai_turn:
                if algorithm == 1:
                    score,new_board = negamax([0],game.board, ai_turn, depth, game)
                else:
                    score,new_board = alpha_beta_pruning([0],game.board, ai_turn,NEGA_INFI , POSI_INFI, depth, game)              
                if new_board:
                    game.ai_move(new_board)
            else:
                game.get_moves()

            
            #判断是否有人获胜
            if game.board.winner() != None:
                game.draw_winner()
                is_run = False
            
            #获取鼠标点击信息，对棋子进行选中和移动
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x , y = pos
                game.after_click(y//SIZE,x//SIZE)
        
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

    menu.add.selector('Algorithm :', [('random',1)],
                      onchange=select_algorithm, font_name=font)
    menu.add.selector('My Turn :', [('WHITE',1), ('BLACK',2)],
                      onchange=select_turn, font_name=font)
    menu.add.selector('Depth :', [(f'{i}', i) for i in range(1, 11)],
                      onchange=select_turn, font_name=font, default=2)

    menu.add.button('Play', run_game, font_name=font)
    menu.add.button('Quit', pygame_menu.events.EXIT, font_name=font)

    menu.mainloop(window)

    run_game()
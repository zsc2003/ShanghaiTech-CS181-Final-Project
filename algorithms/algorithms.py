import pygame
from copy import deepcopy
from utils.config import WHITE, BLACK, POSI_INFI, NEGA_INFI



# from utils.draught import get_valid_moves, get_all_pieces

def get_all_moves(path_num, board, color, game):
    boards = []
    valid_moves = board.get_valid_moves(color) #所有棋子可移动位置
    for piece in board.get_all_pieces(color): 
        if piece in valid_moves:
            path_num[0] += 1
            moves = valid_moves[piece]
            show_path(path_num[0],color,piece,board,game,moves)
            for move,skipped in moves.items():
                temp_board = deepcopy(board)#深拷贝，可以对子对象进行复制
                temp_piece = temp_board.pieces[piece.row][piece.col]
                new_board = simulate_move(temp_piece, move,temp_board, skipped)
                boards.append(new_board)
    return boards





# #模拟移动
def simulate_move(piece, move, board,  skip):
    '''
     模拟棋盘棋子的移动，返回移动后的新棋盘
    '''
    board.move_piece(piece, move[0], move[1])
    if skip:
        board.remove_pieces(skip)
    return board
    
#获取ai模拟移动后产生的所有棋盘


#显示搜索路径
def show_path(path_num,color,piece,board,game,valid_moves):
    board.draw(game.win)
    game.draw_turn()
    game.draw_path_num(path_num)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 40, 4)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(500)



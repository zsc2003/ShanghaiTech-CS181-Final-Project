import pygame
from copy import deepcopy
from utils.config import WHITE,BLACK,POSI_INFI,NEGA_INFI

from algorithms.algorithms import get_all_moves, simulate_move, show_path

def minimax(self, path_num, current_board, color, depth, game):
    if depth == 0 or current_board.winner():
        return current_board.evaluate(game.my_turn),current_board
    
    best_move = None
    #颜色转换
    if color == WHITE:
        other_color = BLACK
    else:
        other_color = WHITE
    if color != game.my_turn:
        max_score = NEGA_INFI
        for move in get_all_moves(path_num, current_board, color, game):
            score = minimax(path_num, move, other_color, depth - 1, game)[0]
            max_score = max(score,max_score)
            if max_score == score:
                best_move = move
        return max_score , best_move
    else:
        min_score = POSI_INFI
        for move in get_all_moves(path_num, current_board, color, game):
            score = minimax(path_num, move, other_color, depth - 1, game)[0]
            min_score = min(score,min_score)
            if min_score == score:
                best_move = move
        return min_score , best_move



def negamax(path_num,current_board,color,depth,game):
    '''
      negamax(负极值算法)是对 minimax(极大极小算法)做出的小改进
      通过max(a,b) = - min(-a,-b)思想将极大、极小情况统一，精简代码量
    '''
    #当深度为0或者已经搜索除有一方获胜，没有继续搜索的必要，返回
    if depth == 0 or current_board.winner() != None:
        return current_board.evaluate(game.my_turn),current_board
    
    best_move = None
    best = NEGA_INFI
    #颜色转换
    if color == WHITE:
        other_color = BLACK
    else:
        other_color = WHITE
    for move in get_all_moves(path_num, current_board, color, game):
        score = -negamax(path_num, move, other_color, depth - 1, game)[0]
        #选择最优解
        best = max(score, best)
        if best == score:
            best_move = move

    return best, best_move
    
def alpha_beta_pruning(path_num, current_board, color, alpha, beta, depth, game):
    '''
     基于nagamax的 alpha-beta剪枝
    '''
    #当深度为0或者已经搜索出有一方获胜，没有继续搜索的必要，返回
    if depth == 0 or current_board.winner() != None:
        return current_board.evaluate(game.my_turn),current_board  
    #颜色转换
    if color == WHITE:
        other_color = BLACK
    else:
        other_color = WHITE
    best_move = None
    moves = get_all_moves(path_num, current_board, color, game)
    if moves:
        for move in moves:
            score = -alpha_beta_pruning(path_num, move, other_color, -beta, -alpha, depth - 1, game)[0]
            if score >= beta:
                return beta,best_move
            if score > alpha:
                alpha = score
                best_move = move
        return alpha,best_move
    else:#无可移动的路径时返回负无穷
        return 1+NEGA_INFI,best_move
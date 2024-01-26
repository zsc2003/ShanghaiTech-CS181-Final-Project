from algorithms.algorithms import *
import numpy as np
import random, pickle
import copy
import math
from utils.config import *

class mcts_node():
    def __init__(self, color = WHITE):
        self.parent = None
        self.children = []
        self.possible_moves = None
        self.turn = color
        self.board = None
        self.playouts = 0
        self.wins = 0
        
    def reverse_node(self):
        if self.turn == WHITE:
            return BLACK
        elif self.turn == BLACK:
            return WHITE
        else:
            raise ValueError("Error turn in reverse_node")
        
    def get_moves(self):
        # get all moves
        valid_moves = self.board.get_valid_moves(self.turn)
        child_nodes = []
        # loop all valid moves and generate new board
        for piece in self.board.get_all_pieces(self.turn):
            # simulate move
            if piece in valid_moves:
                moves = valid_moves[piece]
                for move, skipped in moves.items():
                    child_board = copy.deepcopy(self.board)
                    child_piece = child_board.pieces[piece.row][piece.col]
                    child_board.move_piece(child_piece, move[0], move[1])
                    if skipped:
                        child_board.remove_pieces(skipped)
                    
                    # generate new node
                    child_node = mcts_node()
                    child_node.turn = self.reverse_node()
                    child_node.parent = self
                    child_node.playouts = 0
                    child_node.wins = 0
                    child_node.board = child_board
                    # append
                    child_nodes.append(child_node)
        
        # print(child_nodes)
        
        # return
        return child_nodes

# compute ucb1
def ucb1(node):
    deterministic_value = node.wins/node.playouts
    constant_c = 1 / math.sqrt(2)
    explore_value = constant_c * math.sqrt(2 * math.log(node.parent.playouts)/node.playouts)
    return deterministic_value + explore_value

# uct algorithm
def uct(node):
    best_score = float('-inf')
    best_node = None
    # loop all node in the children
    for child_node in node.children:
        # compute the ucb value
        score = ucb1(child_node)
        if score > best_score:
            best_score = score
            best_node = child_node
    return best_node

def selection(node):
    current_node = node
    # test if child is none
    if current_node.possible_moves == None:
        possible_children = current_node.get_moves()
        current_node.possible_moves = possible_children
    else:
        possible_children = current_node.possible_moves
    
    # while still all child node are explored
    while (len(current_node.children) == len(possible_children)):
        # get best child
        best_child = uct(current_node)
        current_node = best_child
        if current_node.possible_moves == None:
            possible_children = current_node.get_moves()
            current_node.possible_moves = possible_children
        else:
            possible_children = current_node.possible_moves
            
        # if not explored
        if (len(possible_children) == 0):
            return current_node, possible_children
    
    return current_node, possible_children

def expansion(parent, possible_children):
    # if leaf node
    if len(possible_children) == 0:
        return parent
    # find the move
    for move in possible_children:
        move_found = False
        # check if move explored
        for child in parent.children: 
            # may have problem...
            if move.board.pieces == child.board.pieces:
                move_found = True
                break
        # not found
        if not move_found:
            if move.possible_moves == None:
                moves = move.get_moves()
                move.possible_moves = moves
            else:
                moves = move.possible_moves
            if (len(moves) == 0):
                turn = parent.turn
            else:
                turn = parent.reverse_node()
            move.turn = turn
            parent.children.append(move)
            return move
    return None

def simulation(node):
    move = 0
    while node.board.winner() is None:
        # limit the loop
        if move >= 20:
            break
        valid_moves = node.get_moves()
        if valid_moves:
            node = random.choice(valid_moves)
        move += 1
        
    if node.board.board_score() > 0:
        return True
    else:
        return False
    
def backpropagation(node, winner):
    while node is not None:
        node.playouts += 1
        if node.turn and not winner:
            node.wins += 1
        if not node.turn and winner:
            node.wins += 1
        node = node.parent
        
class mcts_agent():
    def __init__(self, board, color):
        self.root = mcts_node(color)
        self.root.board = copy.deepcopy(board)
        self.root.possible_moves = self.root.get_moves()
        
    def step(self, board, iterations):
        self.root.board = copy.deepcopy(board)
        self.root.possible_moves = self.root.get_moves()
        self.root.children = []
        
        for _ in range(iterations):
            current_node, possible_children = selection(self.root)
            # print("currend possible_children: ", possible_children)
            # print("currend_node children: ", current_node.children)
            new_node = expansion(current_node, possible_children)
            # print("node children: ", new_node.children)
            white_win = simulation(new_node)
            backpropagation(new_node, white_win)

        # print("After back root children: ", self.root.children)

        # find the most explored
        max_playouts = 0
        best_child = None
        for child in self.root.children:
            if child.playouts > max_playouts:
                max_playouts = child.playouts
                best_child = child
        return best_child.board
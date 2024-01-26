# mcts algothrim
from algorithms.algorithms import *
import numpy as np
import random, pickle
import copy
import math
from utils.config import *
         
class Node:
    def __init__(self):
        self.valid_actions = []
        self.parent = None
        self.state = None
        self.children = {}
        self.visit_times = 0
        self.value = 0
        # white or black
        self.color = None
        
    def next_color(self):
        if self.color == WHITE:
            return BLACK
        if self.color == BLACK:
            return WHITE
        raise ValueError("Error Color")
    
    def next_state(self, action):
        for piece, move in action.items():
            temp_board = deepcopy(self.state)
            temp_piece = temp_board.pieces[piece.row][piece.col]
            new_board = simulate_move(temp_piece, move[0],temp_board, move[1])
        return new_board
        
    def full_expand(self):
        return len(self.valid_actions) == len(self.children)
    
    def set_all_valid_action(self):
        if self.state == None:
            raise ValueError("Unconstructed node")
        else:
            # print(11111111)
            # print(self.state)
            # self.valid_actions = get_all_moves([0], self.state, self.color, game)
            # print("Color: ", self.color)
            self.valid_actions = self.state.get_valid_moves(self.color)
            # print("Board: ", self.state.pieces)
            # for piece in self.state.pieces:
            #     for piece2 in piece:
            #         if piece2 != 0:
            #             print(piece2.color)
            #         else:
            #             print(piece2)
            #     print('\n')
            # print("\n")
            # print(self.state.white_left)
            # print(self.state.black_left)
            
            # print("valid actions: ", self.valid_actions)
            # print("\n")
            # print("color: ", self.color)
            
    def compute_value(self, state, color):
        if state == None:
            raise ValueError("Unconstructed node")
        else:
            self.value = state.evaluate(color)
            
    def expand(self):
        next_state, action = self.randomChooseNextState()
        next_node = Node()
        next_node.state = next_state
        next_node.color = self.next_color()
        next_node.set_all_valid_action()
        self.children[next_state] = (next_node, action)
        next_node.parent = self
        return next_node
    
    def randomExpand(self):
        # print(self.valid_actions)
        random_piece = random.choice(list(self.valid_actions.keys()))
        random_action = random.choice(list(self.valid_actions[random_piece].keys()))
        action = {random_piece: [random_action, self.valid_actions[random_piece][random_action]]}        
        next_state = self.next_state(action)
        if next_state not in self.children.keys():
            next_node = Node()
            next_node.state = next_state
            next_node.color = self.next_color()
            next_node.set_all_valid_action()
            next_node.compute_value(next_state, self.next_color())
            self.children[next_state] = (next_node, action)
            next_node.parent = self
        else:
            next_node = self.children[next_state][0]
        return next_node
    
    def randomChooseNextState(self):
        if len(self.valid_actions) == 0:
            raise ValueError("Empty valid action")
        else:
            random_piece = random.choice(list(self.valid_actions.keys()))
            random_action = random.choice(list(self.valid_actions[random_piece].keys()))
            action = {random_piece: [random_action, self.valid_actions[random_piece][random_action]]}        
            next_state = self.next_state(action)
        return next_state, action
    
    def bestChild(self, is_exploration):
        if is_exploration:
            c = 1 / math.sqrt(2.0)
        else:
            c = 0.0
        UCB_list = np.array([self.calUCB(c, child) for child, _ in self.children.values()])
        # print("children ", self.children.values())
        best_score = np.amax(UCB_list)
        best_idx = np.argwhere(np.isclose(UCB_list, best_score)).squeeze()
        if best_idx.size > 1:
            best_choice = np.random.choice(best_idx)
        else:
            best_choice = np.argmax(UCB_list)
        best_child, best_action = list(self.children.values())[best_choice]
        if not is_exploration:
            print(f"choose child node with visit_time = {best_child.visit_times}")
        return best_child, best_action
    
    # def calRewardFromState(self, direction):
    #     winner = self.state.getWinner()
    #     # if self.state.findPiece(Piece.RGeneral) is not [] and self.state.findPiece(Piece.BGeneral) is not []:
    #     if winner == direction:
    #         return 1
    #     elif winner == Player.reverse(direction):
    #         return -1
    #     return 0

    def calUCB(self, c, child):
        # UCB = quality_value / visit_time + c * sqrt(2 * ln(parent_visit_time) / visit_time)
        if child.visit_times == 0:
            return 0.0
        UCB = child.value / child.visit_times + c * math.sqrt(2 * math.log(self.visit_times) / child.visit_times)
        return UCB
    
def mcts_agent(current_board, color, game):
    root = Node()
    new_state = current_board
    root.state = new_state
    root.color = color
    root.compute_value(root.state, color)
    root.set_all_valid_action()
    tie = 0
    for i in range(3):
        expanded_node = MCTS_Policy(root, color)
        expanded_node, reward = default(expanded_node, tie)
        backup(expanded_node, reward, color)
    root, action = root.bestChild(False)
    new_board = simulate_move(list(action.keys())[0], action[list(action.keys())[0]][0], current_board, action[list(action.keys())[0]][1])
    return new_board

def MCTS_Policy(root, color):
    if root.state.winner() == None:
        if root.full_expand():
            root, _ = root.bestChild(True)
        else:
            root = root.expand()
            root.compute_value(root.state, color)
            return root
    return root

def default(node, tie):
    round_limit = 3
    r = 0
    while node.state.winner() == None:
        # node = self.treePolicy(node)
        node = node.randomExpand()
        r += 1
        if r > round_limit:
            tie += 1
            return node, 0
    node.color = node.next_color()
    reward = 0
    if node.state.winner() == node.color:
        reward = 1
    else:
        reward = -1
    node.color = node.next_color()
    return node, reward, tie

def backup(node, reward, color):
    while node.parent is not None:
        node.visit_times += 1
        if node.color == color:
            # reward = 0.9 * reward
            node.value -= reward
        else:
            # reward = 0.9 * reward
            node.value += reward
        node = node.parent
    node.visit_times += 1
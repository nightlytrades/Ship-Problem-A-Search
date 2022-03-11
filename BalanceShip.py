from copy import deepcopy
from Node import *

class BalanceShip:
    def __init__(self, board=None):
        self.board = board
        self.goal = .9

    def generate_children(self, node):
        board = node.get_board()
        children = []
        available, containers = find_empty_position(board)
        for posi in containers:
            for a_posi in available:
                board_cpy = deepcopy(board)
                if a_posi[1] != posi[1]:
                    tmp_weight = board_cpy[posi[0]]
                    
    
    def search(self):
        # declare open and closed list
        open_list, close_list = [],[]
        
        # create initial node
        init = Node(None, self.board)

        # append inital node to open list
        open_list.append(init)

        while(open_list):
            # sort open list based on total cost [smallest -> largest]
            open_list.sort(key=lambda x:x.f)
            q = open_list.pop()
            self.generate_children(q) # WRITE THIS


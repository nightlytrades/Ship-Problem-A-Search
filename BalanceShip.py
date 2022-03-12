from copy import deepcopy
from Node import *

class BalanceShip:
    def __init__(self, board=None):
        self.board = board
        self.goal = .9

    def generate_children(self, node):
        board = node.get_board()
        children = []
        available, containers = self.find_empty_position(board)
        for posi in containers:
            if board[posi[0]][posi[1] != 0]:
                for a_posi in available:
                    board_cpy = deepcopy(board)
                    if a_posi[1] != posi[1]:
                        tmp_weight = board_cpy[posi[0]][posi[1]]
                        board_cpy[posi[0]][posi[1]] = 0
                        board_cpy[a_posi[0]][a_posi[1]] = tmp_weight
                        child = Node(node, board)
                        child.set_f(node.get_f())
                        child.set_g(node.get_g())
                        node.set_children(child)

    def find_empty_position(self, board):
        empty_list, top_list = [],[]
        for row in range(8):
            for column in range(12):
                ##print("r/c", row,column)
                
                if board[row][column]==-1:
                    continue
                elif board[row][column]==0 and row<7 and board[row+1][column]==-1:
                    empty=(row,column)
                    empty_list.append(empty)
                    

                elif board[row][column]==0 and row==7:
                    empty=(row,column)
                    empty_list.append(empty)
                    
                elif board[row][column]==0 and board[row-1][column]!=0 and row!=0:
                    empty=(row,column)
                    empty_list.append(empty)
                
                elif board[row][column]!=0 and board[row-1][column]==0:
                    empty=(row-1,column)
                    empty_list.append(empty)
                    container=(row,column)
                    top_list.append(container)  

        return empty_list, top_list

    
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


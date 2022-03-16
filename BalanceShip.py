import numpy as np
from copy import deepcopy
from Node import *

def is_balanced(child): # child = [board, f, g]
    board = child.get_board()
    weight_left = 0
    weight_right = 0
    for row in range(8):
        for col in range(12):
            if col < 6:
                weight_left += board[row][col]
            else:
                weight_right += board[row][col]
    return (min(weight_left, weight_right) / max(weight_left, weight_right)) > 0.9


class BalanceShip:
    def __init__(self, board=None):
        self.board = board
        self.goal = .9

    def generate_children(self, node):
        # get board from node
        board = node.get_board()

        # find available spots and containers at the top of their respective columns
        available, containers = self.find_empty_position(board)

        # find every posible movement and add set them as chidren for the node passed in
        for posi in containers:
            if board[posi[0]][posi[1] != 0]:
                for a_posi in available:
                    board_cpy = deepcopy(board)
                    if a_posi[1] != posi[1]:
                        tmp_weight = board_cpy[posi[0]][posi[1]]
                        board_cpy[posi[0]][posi[1]] = 0
                        board_cpy[a_posi[0]][a_posi[1]] = tmp_weight
                        child = Node(node, board_cpy)
                        child.set_parent(node)
                        child.set_f(node.get_f())
                        child.set_g(node.get_g())
                        node.set_children(child)

    def find_empty_position(self, board):
        empty_list, top_list = [],[]
        for row in range(8):
            for column in range(12):
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
    
    def find_weight(self,board):
  
        left_list,right_list=[],[]
        weight,left_weight,right_weight=0,0,0
        
        for row in range(8):
            for column in range(12):
                if board[row][column]==-1:
                    continue
                elif column<6:
                    weight=board[row][column]
                    left_list.append(weight)
                    ##print("c/r: ", column, row, "left value",weight)
                else:
                    weight=board[row][column]
                    right_list.append(weight)
                    ##print("c/r: ", column, row, "right value",weight)

        left_weight=sum(left_list)
        right_weight=sum(right_list)

        ##print("left: ", left_list)
        ##print("right: ", right_list)

        #print("total weight left: ", left_weight, "total weight right: ", right_weight)

        return left_weight,right_weight  

    def get_heuristic(self):
        
        # start=init_board
        # goal=new_board
        start=np.array([ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 99, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0] ])
        new=np.array([ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 99, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0] ])
        distance=0
        this_val=np.argwhere(new==100)

        print("this", this_val)
        print("7:", this_val[0][0])
        print("9:", this_val[0][1])
        for row in range(8):
            for column in range(12):
                start_value = start[row][column]
                if start_value !=0:
                    pos=np.argwhere(new==start_value)
                    pos_row=pos[0][0]
                    pos_column=pos[0][1]
                    distance += abs(column - pos_column) + abs(row - pos_row)
        heuristic=distance
        print("man dis ", heuristic)

        return heuristic
            

    def search(self):
        # declare open and closed list
        open_list, close_list = [],[]
        
        # create initial node
        init = Node(None, self.board)

        # append inital node to open list
        open_list.append(init)
        init.print_board()

        while(open_list):
            # sort open list based on total cost [smallest -> largest]
            open_list.sort(key=lambda x:x.f)

            # pop the highest priority node off of the list
            q = open_list.pop(0)

            # generate children of the node popped off
            self.generate_children(q) # WRITE THIS
            for child in q.get_children():
                if is_balanced(child):
                    child.print_board()
                    return child
                else:
                    child.set_g(1)
                    init_board=q.get_board
                    new_board=child.get_board
                    ##calling the heuristic function and returning h value
                    h=child.get_heuristic(init_board,new_board)
                    child.set_h(h)
                    ##child.set_h(1)
                    child.set_f(child.get_g() + child.get_h())
                    if any(x.get_board() == child.get_board() for x in open_list):
                        continue
                    else:
                        open_list.append(child)
            close_list.append(q)



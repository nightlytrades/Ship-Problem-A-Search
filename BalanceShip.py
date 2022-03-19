
import numpy as np
from copy import deepcopy
from numpy import empty

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
            if board[posi[0]][posi[1]] != 0:
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

    def find_weight(self, board):
        left_list,right_list=[],[]
        weight,left_weight,right_weight=0,0,0
        
        for row in range(8):
            for column in range(12):
                if board[row][column]==-1:
                    continue
                elif column<6:
                    weight=board[row][column]
                    left_list.append(weight)
                else:
                    weight=board[row][column]
                    right_list.append(weight)

        left_weight=sum(left_list)
        right_weight=sum(right_list)

        return left_weight,right_weight 

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
                    top_list.append(container)
                elif board[row][column]!=0 and row-1 < 0:
                    container=(row,column)
                    top_list.append(container)
        empty_list.sort(key=lambda x:x[1])
        return empty_list, top_list

    def find_moved_container(self, q, child):
        moves = []

        # go through board and find the positions that have changed
        for row in range(8):
            for col in range(12):
                # if parent baord and child board do not match in the same
                # position append that pos to moves
                if q.get_board()[row][col] != child.get_board()[row][col]:
                    moves.append([row, col])

        # check position of first tuple
        # if its 0 on the parent(q) node then swap the 2 tuples
        board = q.get_board()
        if moves:
            if board[moves[0][0]][moves[0][1]] == 0:
                moves[0],moves[1] = moves[1],moves[0]
        return moves

    def calc_g(self, moved_containers):
        # calculate the distance between the moved containers
        if moved_containers:
            return abs(moved_containers[0][0] - moved_containers[1][0]) + abs(moved_containers[0][1] - moved_containers[1][1])
        return 1

    def get_balance_heuristic(self, board):
        # find weights of the left and right side
        left_weight, right_weight = self.find_weight(board)

        # find the balance mass
        balance_mass = (left_weight + right_weight) / 2

        # determine what side is heavier
        heavy_side = max(left_weight, right_weight)
        lighter_side = min(left_weight, right_weight)

        # find the deficit
        deficit = balance_mass - lighter_side

        # get current balance score
        balance_score = lighter_side / heavy_side

        # find weights on the heavy side
        # add those weights to a list
        # *NOTE: for now just taking weights, 
        # will account for containder positions 
        # after I get this simple heuristic working*
        heavy_side_weights = []

        if heavy_side == left_weight: # heavy side is left side
            for i in range(len(board)):
                for j in range(6):
                    if board[i][j] != 0:
                        heavy_side_weights.append(board[i][j])
        else: # else heavy side is the right side
            for i in range(len(board)):
                for j in range(6,12):
                    if board[i][j] != 0:
                        heavy_side_weights.append(board[i][j])

        # sort the weights in decending order
        heavy_side_weights.sort(reverse=True)

        # slide down the list to find weights <= our deficit
        heuristic = 0

        # move weights to find minimum number of containers that can be moved
        for weight in heavy_side_weights:
            if (balance_score < .90) & (deficit * 1.2 > weight):
                heavy_side -= weight
                lighter_side += weight
                deficit -= weight
                balance_score = min(heavy_side,lighter_side)/max(heavy_side,lighter_side)
                heuristic += 1
        # if balance score is < .9 then balance is not possible
        if balance_score < .90:
            return 0
        return heuristic

    def get_heuristic(self,parent_board,child_board):
        
        distance=0
        boards=[parent_board,child_board]
        
        ##putting zero for "NAN"
        for board in boards:
            for row in range(8):
                for column in range(12):
                    #it was =='NAN' but I noticed that 'NAN' is replaced with -1, 
                    #when parent/child board is passed
                    if board[row][column]==-1:
                        board[row][column]=0

        parent_board=np.array(parent_board)
        child_board=np.array(child_board)
      
        ##calculating manhattan distance
        for row in range(8):
            for column in range(12):
                _value = parent_board[row][column]
                ##calculating distance for the containers moved
                if _value !=0:
                    pos=np.argwhere(child_board==_value)
                    #print("pos",pos)
                    pos_row=pos[0][0]
                    pos_column=pos[0][1]
                    distance += abs(column - pos_column) + abs(row - pos_row)
        
        heuristic=distance
        #here our heuristic value h, is in minutes
        #print("manhattan distance: ", heuristic)

        return heuristic
            


    def search(self):
        # declare open and closed list
        open_list, close_list = [],[]
        
        # create initial node
        init = Node(None, self.board)

        # check if balance is possible
        if self.get_balance_heuristic(init.get_board()) == 0:
            print('Balance is not possible')
            return init

        # append inital node to open list
        open_list.append(init)
        init.print_board()

        while(open_list):
            # sort open list based on total cost [smallest -> largest]
            open_list.sort(key=lambda x:x.f)

            # pop the highest priority node off of the list
            q = open_list.pop(0)

            # generate children of the node popped off
            self.generate_children(q)
            for child in q.get_children():
                if is_balanced(child):
                    return child
                else:
                    moves = self.find_moved_container(q,child)
                    child.set_g(self.calc_g(moves) + q.get_f())
                    #getting parent/child boards to compute h
                    child_board=child.get_board()
                    ##calling the heuristic function and returning h value
                    h=self.get_balance_heuristic(child_board)
                    child.set_h(h)
                    child.set_f(child.get_g() + child.get_h())
                    if any(x.get_board() == child.get_board() for x in open_list):
                        continue
                    elif any(x.get_board() == child.get_board() for x in close_list):
                        continue
                    else:
                        open_list.append(child)
            close_list.append(q)
        
    def balance(self, node, file_name):
        # declare stack for the nodes in the proper order
        nodes = []
        
        # trace back through the parents of the terminating node
        while node is not None:
            nodes.append(node)
            node = node.get_parent()

        # reverse the list to get correct order
        nodes.reverse()
        moves = []

        # go through the list and find the containers that were moved
        for i in range(len(nodes)):
            if i+1 < len(nodes):
                move = self.find_moved_container(nodes[i], nodes[i+1])
                moves.append(move)
        
        count = 0
        build_string = ''

        # TODO: still need to calculate total time
        total_time = 0

        # output moves
        for i in range(len(moves)):
            if count == 0:
                # calculations to get the positions to match the manifest
                tup = deepcopy(moves[i][0])
                tup[0] = abs(8-tup[0])
                tup[1] = abs(1+tup[1])
                build_string += 'Move crane from [8, 1] to ' + str(tup) + '\n'
                tup1 = deepcopy(moves[i][1])
                tup1[0] = abs(8-tup1[0])
                tup1[1] = abs(1+tup1[1])
                build_string += 'Move container in position ' + str(tup) + ' to position ' + str(tup1) + '\n'
                count += 1
            else: # finish this, similar to above
                tup = deepcopy(moves[i-1][1])
                tup[0] = abs(8-tup[0])
                tup[1] = abs(1+tup[1])
                tup1 = deepcopy(moves[i][0])
                tup1[0] = abs(8-tup1[0])
                tup1[1] = abs(1+tup1[1])
                tup2 = deepcopy(moves[i][1])
                tup2[0] = abs(8-tup2[0])
                tup2[1] = abs(1+tup2[1])
                build_string += 'Move crane from position ' + str(tup) + ' to ' + str(tup1) + '\n'
                build_string += 'Move container in position ' + str(tup1) + ' to position ' + str(tup2) + '\n'

        # get distance
        dist_list = []
        distance = 0
        for move in moves:
            dist_list.append(move[0])
            dist_list.append(move[1])
        for i in range(len(dist_list)):
            if i + 1 < len(dist_list):
                distance += abs(dist_list[i][0] - dist_list[i+1][0]) + abs(dist_list[i][1] - dist_list[i+1][1])

        if (distance > 0):
            distance += 10
        build_string += 'Estimated time to balance is ' + str(distance) + ' minutes'

        # write moves to a file
        write = file_name.split('.')[0] + 'TRACE.txt'
        with open(write, 'w') as f: 
            f.write(build_string)
        f.close()
        return moves
    
    def swap_dict_pos(self, dict, moves, file_name):
        for move in moves:
            # changing values of the positions to match the dictionary
            tup = deepcopy(move[0])
            tup[0] = abs(8-tup[0])
            tup[1] = abs(1+tup[1])

            tup1 = deepcopy(move[1])
            tup1[0] = abs(8-tup1[0])
            tup1[1] = abs(1+tup1[1])

            # modifying the string1 to match the format
            str1 = str(tup).replace(' ','').replace('[','').replace(']','')
            str1_edit = '0' + str1

            # checking length of str if its < 5 add a 0 in 3rd pos
            if len(str1_edit) < 5:
                str1_edit = str1_edit[0:3] + '0' + str1_edit[3:]

            # modifying str2 to match format
            str2 = str(tup1).replace(' ', '').replace('[','').replace(']','')
            str2_edit = '0' + str2

            # checking length of str if its < 5 add a 0 in 3rd pos
            if len(str2_edit) < 5:
                str2_edit = str2_edit[0:3] + '0' + str2_edit[3:]

            # swap the values in the dictionary
            dict[str1_edit],dict[str2_edit] = dict[str2_edit],dict[str1_edit]

        # printing the values in the dictionary
        #for key, value in dict.items():
        #    print('[' + str(key) + '], ' + '{' + value[0] + '}, ' + value[1])

        # write to file
        self.write_to_file(file_name,dict)
        return dict

    # used for testing purposes
    def test_container_func(self, node):
        node2 = node.get_parent()
        board = node2.get_board()

        node2.print_board()
        node.print_board()

        move = self.find_moved_container(node2, node)
        print(move[0][0])
        print(move[0][1])

        print(board[move[0][0]][move[0][1]])
        print(move)

    def print_trace(self, node):
        nodes = []

        # trace back through the parents of the terminating node
        while node is not None:
            nodes.append(node)
            node = node.get_parent()

        # reverse the list to get correct order
        nodes.reverse()

    def write_to_file(self, file_name, dict):
        # update the name of the file
        write = file_name.split('.')[0] + 'UPDATED.txt'

        # open file and write the values to file
        with open(write, 'w') as f: 
            for key, value in dict.items(): 
                f.write('[' + str(key) + '], ' + '{' + value[0] + '}, ' + value[1] + '\n')
        f.close()
#from project import get_heuristic
from copy import deepcopy

def is_balanced(child): # child = [board, f, g]
    board = child[0]
    weight_left = 0
    weight_right = 0
    for row in range(8):
        for col in range(12):
            if col < 6:
                weight_left += board[row][col]
            else:
                weight_right += board[row][col]
    return (min(weight_left, weight_right) / max(weight_left, weight_right)) > 0.9


def find_container_to_move(board,left_weight,right_weight):
    
    heavy_side=""
    to_move=[]
    move_dict={}

    if left_weight>right_weight:
        heavy_side='left'
    else:
        heavy_side='right'

    ##finding containers on the heavy side
    if heavy_side=='left':
        for row in range(8):
            for column in range(6):
                if board[row][column]==-1:
                    continue
                container_weight=board[row][column]
                move_dict[container_weight]=(row,column)
                to_move.append(container_weight)
    else:
        for row in range(8):
            for column in range(6,12):
                if board[row][column]==-1:
                    continue
                container_weight=board[row][column]
                move_dict[container_weight]=(row,column)
                to_move.append(container_weight)
    
    ##picking heavier container to move to the other side
    flg = 1
    while(flg==1):
        to_move.sort(reverse=True)
        max_weight=max(to_move)
        ##print(to_move)
        ##print(max_weight)

        position_max=move_dict[max_weight]
        _row=position_max[0]
        _column=position_max[1]
        
        ##if the heavy container has another container on top of it, it cannot be moved 
        ##therefore it is removed from the list and we pick the next heavy container

        if board[_row-1][_column]!=0:
            to_move.pop(max_weight)
            flg=1
        else:
            container_to_move=(_row, _column)
            flg = 0
            #print("moving this", container_to_move)

            return container_to_move


def find_empty_position(board):

    empty_list=[]
    top_list=[]

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


    #print("empty positions: ", empty_list)
    #print("top list:", top_list)

    return empty_list, top_list
  
def find_weight(board):
  
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
    
def second_tuple(tup):
    return tup[1]

def generate_children(q): # q = (board, f, g) only appends children with different board. f and g are copied from parent
    board = q[0]
    children = []
    available, containers = find_empty_position(board) # [[7,0],[7,1],[6,2], ...]
    for posi in containers:
        #print('position of container', posi)
        if board[posi[0]][posi[1]] != 0:
            #available = find_empty_position(board_cpy) # [[7,0], [6,1], [5,2], [7,3], ...]
            for a_posi in available:
                board_cpy = deepcopy(board)
                #print('new board', board_cpy)
                if a_posi[1] != posi[1]: # avoid moving to the original position
                    #print('movable position', a_posi)
                    tmp_weight = board_cpy[posi[0]][posi[1]]
                    board_cpy[posi[0]][posi[1]] = 0
                    board_cpy[a_posi[0]][a_posi[1]] = tmp_weight
                    children.append([board_cpy, q[1], q[2]])
    return children


def get_g(q, child): # find difference of q's board and child's board, return # of moves required to achieve (board, f, g)
    moves = []
    for row in range(8):
        for col in range(12):
            if q[0][row][col] != child[0][row][col]:
                moves.append([row, col])
    #print('move', moves)
    return abs(moves[0][0] - moves[1][0]) + abs(moves[0][1] - moves[1][1])


def search(init): # init
    open_list, close_list = [],[] # open list has tuple (board, cost)
    open_list.append([init, 0, 0]) #init has a board of weight
    while(open_list):
        open_list.sort(key=second_tuple) #open list sorted by cost
        q = open_list.pop()
        q_children = generate_children(q) # q_children = [(new_borad, f, g), ...] # only generating new board
        for child in q_children:
            if is_balanced(child):
                print(child)
                return child
            else:
                child[2] += get_g(q, child) # TO DO updating g
                child[1] = child[2] + get_balance_heuristic(child[0]) # f = g + h

                for board, f, g in enumerate(close_list):
                    if not (child[0] == board and f < child[1]):
                        open_list.append(child)
        close_list.append(q)


def get_balance_heuristic(board):
    # find weights of the left and right side
    left_weight, right_weight = find_weight(board)

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

    for weight in heavy_side_weights:
        if (balance_score < .90) & (deficit * 1.2 > weight):
            heavy_side -= weight
            lighter_side += weight
            deficit -= weight
            balance_score = min(heavy_side,lighter_side)/max(heavy_side,lighter_side)
            heuristic += 1
    return heuristic
  



def main():

    print("Begin")

    f1 = open('ship_cases/ShipCase1.txt')
    board= [[0 for j in range(12)] for i in range(8)]
    ##print(board)

    dict = {}
    _row_limit = 8
    _column_limit = 12
    _row = 7
    _column = 0
    for line in f1:
    
        key, item1, item2 = line.split()
        key = key[1:-2]
        item1 = item1[1:-2]
        dict[key] = [item1, item2]

        if item2=="NAN":
            board[_row][_column] = -1
        else:
            board[_row][_column] = int(item1)
        # Next one
        if (_column + 1 == _column_limit):
            _row -= 1
            _column = 0
        else:
            _column += 1
    print(board)
    print('end')


#visual of the intial state of the ship, 8x12 matrix
#INDX   0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12

##[     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       0
#       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       1
#       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       2 
#       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       3 
#       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       4
#       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       5
#       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       6
#       [0, 99, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0]     7
#  ]

##[     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       0
#       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       1
#       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       2
#       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       3
#       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       4
#       [40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],      5
#       [-, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, -],      6
#       [-, -, -, 120, 0, 0, 0, 0, 35, -, -, -]     7
#  ]

# 99, 100

#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# [40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
# ['NAN', 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'NAN'], 
# ['NAN', 'NAN', 'NAN', 120, 0, 0, 0, 0, 35, 'NAN', 'NAN', 'NAN']
# ============================================================================================
#
# ============================================================================================
if __name__ == "__main__":
    main()
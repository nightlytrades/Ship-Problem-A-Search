


def pick_container_to_move(board,left_weight,right_weight):
    
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
                if board[row][column]=="NAN":
                    continue
                container_weight=board[row][column]
                move_dict[container_weight]=(row,column)
                to_move.append(container_weight)
    else:
        for row in range(8):
            for column in range(6,12):
                if board[row][column]=="NAN":
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
            print("moving this", container_to_move)

            return container_to_move


def find_empty_position(board):

    empty_list=[]
    top_list=[]

    for row in range(8):
        for column in range(12):
            ##print("r/c", row,column)
            
            if board[row][column]=="NAN":
                continue
            elif board[row][column]==0 and row<7 and board[row+1][column]=="NAN":
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

    print("empty positions: ", empty_list)
    print("top list:", top_list)

    return empty_list, top_list
            
    

def search():
    open_list, close_list = [],[]

def find_weight(board):

    left_list,right_list=[],[]
    weight,left_weight,right_weight=0,0,0
    
    for row in range(8):
        for column in range(12):
            if board[row][column]=="NAN":
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

    print("total weight left: ", left_weight, "total weight right: ", right_weight)

    return left_weight,right_weight    



def main():

    print("Begin")

    f1 = open('ship_cases/ShipCase2.txt')
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
            board[_row][_column] = item2
        else:
            board[_row][_column] = int(item1)
        # Next one
        if (_column + 1 == _column_limit):
            _row -= 1
            _column = 0
        else:
            _column += 1
    print("--initial board--")
    print(board)

    left,right=find_weight(board)
    empty_list,top_list=find_empty_position(board)
    pick_container_to_move(board,left,right)
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
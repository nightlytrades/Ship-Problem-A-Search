

def find_empty_position(board, left_weight, right_weight):
    
    balanced_mass = (left_weight + right_weight) / 2
    deficit = balanced_mass - min(left_weight, right_weight)
    balanced_score = min(left_weight, right_weight)/ max(left_weight, right_weight)

    if(balanced_score > 0.9):
        return 

    light_side=""

    if left_weight>right_weight:
        light_side='right'
    else:
        light_side='left'

    empty_list=[]

    if (light_side=='right'):
        for row in range(8):
            for column in range(6,12):
                empty=()
                if board[row][column]==0:
                    empty=(row,column)
                    empty_list.append(empty)
    else:
        for row in range(8):
            for column in range(0,6):
                empty=()
                if board[row][column]==0:
                    empty=(row,column)
                    empty_list.append(empty)
    
    print("empty positions: ", empty_list, " on the lighter side: ", light_side)
            
    

def search():
    open_list, close_list = [],[]

def find_weight(board):

    left_list,right_list=[],[]
    weight,left_weight,right_weight=0,0,0
    
    for row in range(8):
        for column in range(12):
            if column<6:
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
        board[_row][_column] = int(item1)
        # Next one
        if (_column + 1 == _column_limit):
            _row -= 1
            _column = 0
        else:
            _column += 1
    print(board)

    left,right=find_weight(board)
    find_empty_position(board,left,right)

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

# ============================================================================================
#
# ============================================================================================
if __name__ == "__main__":
    main()
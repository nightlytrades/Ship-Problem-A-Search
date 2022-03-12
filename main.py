from BalanceShip import *

def main():
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
            board[_row][_column] = -1
        else:
            board[_row][_column] = int(item1)
        # Next one
        if (_column + 1 == _column_limit):
            _row -= 1
            _column = 0
        else:
            _column += 1

    obj_1 = BalanceShip(board)
    obj_1.search()


if __name__ == "__main__":
    main()
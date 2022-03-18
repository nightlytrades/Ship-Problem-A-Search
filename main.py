from BalanceShip import *
import sys

def read_file(file_name):
    f1 = open(file_name)
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
    f1.close()
    return dict, board

def main():
    # take command line arguments for file name
    n = len(sys.argv)

    if n < 2:
        print('Not enough arguments')
        return 1
    elif n > 2:
        print('Too many arguments')
    else:
        try:
            # read in the new file
            read_file(sys.argv[1])
            manifest, board = read_file(sys.argv[1])

            # create new balance object
            obj_1 = BalanceShip(board)

            # search for a balance
            sol = obj_1.search()

            # show final maifest preview
            print('Final Manifest Preview')
            sol.print_board()

            # balance the ship
            move = obj_1.balance(sol, sys.argv[1])

            # update the manifest
            obj_1.swap_dict_pos(manifest, move, sys.argv[1])
        except IOError:
            print('Could not read file: ', sys.argv[1])

    # TODO: write new manifest to file
    # TODO: write steps to new file


if __name__ == "__main__":
    main()
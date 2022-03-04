# ============================================================================================
#   Definition
# ============================================================================================
from operator import itemgetter

# ============================================================================================
#   find_masses
#   Input: dictionary, Output: weight(left), weight(right)
# ============================================================================================
def find_masses(dict):
    total_weight_left = 0
    total_weight_right = 0
    for line in dict:
        # print(line)
        row = line[:2]
        col = line[3:]
        idx = row + ',' + col

        if int(col) < 7: # left
            total_weight_left += int(dict[idx][0])
        else:
            total_weight_right += int(dict[idx][0])
    return total_weight_left, total_weight_right

# ============================================================================================
#   Heuristic
#   Input: dictionary, Output: heuristic value (int)
# ============================================================================================
def add_tuple(tup):
    return tup[0] + tup[1]
def sub_tuple(tup):
    return tup[0] - tup[1]
def third_tuple(tup):
    return tup[2]

def get_heuristic(dict):
    heuristic_value = 0
    dict_cpy = dict
    weight_left, weight_right = find_masses(dict)
    balanced_mass = (weight_left + weight_right) / 2
    deficit = balanced_mass - min(weight_left, weight_right)
    balanced_score = min(weight_left, weight_right) / max(weight_left, weight_right)
    if(balanced_score > 0.9):
        return 0

    list = []
    list_unused = []

    for line in dict_cpy:
        row = line[:2]
        col = line[3:]
        idx = row + ',' + col

        if max(weight_left, weight_right) == weight_left:  # left is heavier
            if int(col) < 7:  # left
                if int(dict[idx][0]) != 0:
                    list.append(int(dict[idx][0]))
                if dict[idx][1] == "UNUSED":
                    list_unused.append([int(row), int(col), 0])
        else: # right is heavier
            if int(col) > 6:  # right
                if int(dict[idx][0]) != 0:
                    list.append(int(dict[idx][0]))
                if dict[idx][1] == "UNUSED":
                    list_unused.append([int(row), int(col), 0]) # 0 meaning not bottom

    # here, list contains weights of whichever the heavier side
    list.sort(reverse=True)
    print('initial                    ', list_unused)
    # To DO
    # set the third tuple 1 for the bottom container
    bottom = []
    for tuple in list_unused:
        if tuple[1] not in bottom:
            tuple[2] = 1
            bottom.append(tuple[1])

    print('set 1 for bottom           ', list_unused)

    # find open spots on the lighter side
    if max(weight_left, weight_right) == weight_left:
        list_unused.sort(key=add_tuple, reverse=True)
    else:
        list_unused.sort(key=sub_tuple, reverse=True)

    print('sorted                     ', list_unused)

    list_unused.sort(key=third_tuple, reverse=True)
    # bottom one first


    print('sorted & bottom comes first', list_unused)
    # find pos of heavier side

    list_ptr = 0
    #while(balanced_score < 0.9):
    #    if balanced_mass > list[list_ptr]:

    #print(list)
# ============================================================================================
#   Main
# ============================================================================================
def main():
    print("Begin")

    f1 = open('ship_cases/ShipCase1.txt')
    dict = {}
    for line in f1:
        key, item1, item2 = line.split()
        key = key[1:-2]
        item1 = item1[1:-2]
        dict[key] = [item1, item2]

    #print(dict)
    get_heuristic(dict)
    #print(dict['01,02'][0])
    '''
    print(col)
    print('left', total_weight_left)
    print('right', total_weight_right)
    balance_score = min(total_weight_right, total_weight_left) / max(total_weight_right, total_weight_left) # > 0.9
    print(balance_score)
    '''


    print("End")



# ============================================================================================
#
# ============================================================================================
if __name__ == "__main__":
    main()
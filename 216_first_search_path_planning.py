from collections import deque

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0,0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0], # up
         [0, -1], # left
         [1, 0], # down
         [0, 1]] # right

delta_name = ['^', '<', 'v', '>']
cost = 1

def valid_position(i, j):
    #print("i = ", i, " j =", j)
    if ((i >= 0 and i <= len(grid)-1) and
        (j >= 0 and j <= len(grid[0])-1) and
        (grid[i][j] != 1)):
        return True

    return False

def expand_children(current_state, visited_position, new_open_list):
    for i in range(len(delta)):
        new_position_i = current_state[1] + delta[i][0]
        new_position_j = current_state[2] + delta[i][1]
        if valid_position(new_position_i, new_position_j):
            child_state_cost = current_state[0] + 1
            child_state = [child_state_cost, new_position_i, new_position_j]
            if ('{},{}'.format(new_position_i, new_position_j) not in visited_position and
                child_state not in new_open_list):
                new_open_list.append(child_state)

def determine_goal(state):
    if [state[1], state[2]] == goal:
        return True

    return False

def search(starting_position):
    new_open_list = deque()
    visited_position = {}

    current_cost = [0]
    new_open_list.append(current_cost + starting_position)
#    print('initial open list:')
#    print('    {}'.format(new_open_list))

    while new_open_list:
#        print('----')
        visiting_state = new_open_list.popleft()
#        print('take list item')
#        print(visiting_state)
        current_state = visiting_state
        is_goal = determine_goal(current_state)
        visited_position["{},{}".format(current_state[1], current_state[2])] = 1
        if is_goal:
            print(visiting_state)
            print('###### Search successful')
            return visiting_state
        else:
            expand_children(current_state, visited_position, new_open_list)
#            print('new open list')
#            print('\t{}'.format(new_open_list))

    print('fail')
    return ['fail']

search(init)

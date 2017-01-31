from collections import deque

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]

init = [0,0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0], # up
         [0, -1], # left
         [1, 0], # down
         [0, 1]] # right

delta_name = ['^', '<', 'v', '>']
cost = 1

expand = [[-1 for column in range(len(grid[0]))] for row in range(len(grid))]
expand_index = 0

goal_path_grid = [[' ' for column in range(len(grid[0]))] for row in range(len(grid))]

def valid_position(i, j):
    #print("i = ", i, " j =", j)
    if ((i >= 0 and i <= len(grid)-1) and
        (j >= 0 and j <= len(grid[0])-1) and
        (grid[i][j] == 0)):
        return True

    return False

def expand_children(current_state, visited_position, new_open_list, viable_pathes):
    for i in range(len(delta)):
        new_position_i = current_state[1] + delta[i][0]
        new_position_j = current_state[2] + delta[i][1]
        if valid_position(new_position_i, new_position_j):
            child_state_cost = current_state[0] + 1
            child_state = [child_state_cost, new_position_i, new_position_j]
            child_position = '{},{}'.format(new_position_i, new_position_j)
            if (child_position not in visited_position and
                child_state not in new_open_list):
                new_open_list.append(child_state)
                viable_pathes[child_position] = [current_state[1], current_state[2]]

def determine_goal(state):
    if [state[1], state[2]] == goal:
        return True

    return False

def determine_goal_path(goal_state, viable_pathes):
    current_position = '{},{}'.format(goal_state[1], goal_state[2])
    goal_path = []
    goal_path.append([goal[0], goal[1]])
    while current_position in viable_pathes:
        goal_path.append(viable_pathes[current_position])
        current_position = '{},{}'.format(viable_pathes[current_position][0], viable_pathes[current_position][1])

    for i in range(1, len(goal_path)):
        motion = [goal_path[i-1][0] - goal_path[i][0], goal_path[i-1][1] - goal_path[i][1]]
        delta_index = delta.index(motion)
        goal_path_grid[goal_path[i][0]][goal_path[i][1]] = delta_name[delta_index]

    goal_path_grid[goal[0]][goal[1]] = '*'

def search(starting_position, expand_index=0):
    new_open_list = deque()
    visited_position = {}
    viable_pathes = {}

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
        expand[current_state[1]][current_state[2]] = expand_index
        expand_index = expand_index + 1
        if is_goal:
            print(visiting_state)
            print('###### Search successful')
#            print('Viable Pathes')
#            print('\t\t', viable_pathes)
            determine_goal_path(visiting_state, viable_pathes)
            return visiting_state
        else:
            expand_children(current_state, visited_position, new_open_list, viable_pathes)
#            print('new open list')
#            print('\t{}'.format(new_open_list))

    print('fail')
    return ['fail']

search(init, expand_index)
for i in range(len(expand)):
    print(expand[i])

for i in range(len(goal_path_grid)):
    print(goal_path_grid[i])

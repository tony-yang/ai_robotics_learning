grid = [[0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]

heuristic = [[9, 8, 7, 6, 5, 4],
             [8, 7, 6, 5, 4, 3],
             [7, 6, 5, 4, 3, 2],
             [6, 5, 4, 3, 2, 1],
             [5, 4, 3, 2, 1, 0]]

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

goal_policy = [[' ' for column in range(len(grid[0]))] for row in range(len(grid))]

def valid_position(i, j):
    #print("i = ", i, " j =", j)
    if ((i >= 0 and i <= len(grid)-1) and
        (j >= 0 and j <= len(grid[0])-1) and
        (grid[i][j] == 0)):
        return True

    return False

def expand_children(current_state, visited_position, new_open_list, viable_pathes):
    for i in range(len(delta)):
        new_position_i = current_state[2] + delta[i][0]
        new_position_j = current_state[3] + delta[i][1]
        if valid_position(new_position_i, new_position_j):
            child_state_cost = current_state[1] + 1
            total_cost_to_goal = child_state_cost + heuristic[new_position_i][new_position_j]
            child_state = [total_cost_to_goal, child_state_cost, new_position_i, new_position_j]
            child_position = '{},{}'.format(new_position_i, new_position_j)
            if (child_position not in visited_position and
                child_state not in new_open_list):
                new_open_list.append(child_state)
                # The class solution stored the action took to reach this child
                # I stored the parent position, and calculated the action based on the
                # parent position and child position difference. I guess storing directly
                # the action took is more convenient!
                viable_pathes[child_position] = [current_state[2], current_state[3]]

def determine_goal(state):
    if [state[2], state[3]] == goal:
        return True

    return False

def determine_goal_path(goal_state, viable_pathes):
    current_position = '{},{}'.format(goal_state[2], goal_state[3])
    goal_path = []
    goal_path.append([goal[0], goal[1]])
    while current_position in viable_pathes:
        goal_path.append(viable_pathes[current_position])
        current_position = '{},{}'.format(viable_pathes[current_position][0], viable_pathes[current_position][1])

    for i in range(1, len(goal_path)):
        motion = [goal_path[i-1][0] - goal_path[i][0], goal_path[i-1][1] - goal_path[i][1]]
        delta_index = delta.index(motion)
        goal_policy[goal_path[i][0]][goal_path[i][1]] = delta_name[delta_index]

    goal_policy[goal[0]][goal[1]] = '*'

def search(starting_position, expand_index=0):
    new_open_list = []
    visited_position = {}
    viable_pathes = {}

    current_position_i = starting_position[0]
    current_position_j = starting_position[1]
    current_state_cost = [0]
    total_cost_to_goal = [current_state_cost[0] + heuristic[current_position_i][current_position_j]]
    # The class uses 5 item list for each state representation. I used 4. I store the original state
    # cost and the final total cost to goal. The heusristic cost can always be calculated by
    # total cost to goal - original state cost
    new_open_list.append(total_cost_to_goal + current_state_cost + starting_position)
    print('initial open list:')
    print('    {}'.format(new_open_list))

    while new_open_list:
        print('----')
        # Previously I used operator itemgetter to sort by only the first element of each state
        # It seems that is less deterministic and is up to the behavior how the sort orders
        # subsequent elements in the list. The pure list sort will compare each elements in orders
        # So just use list.sort should do, although it might be less efficient
        new_open_list.sort(reverse=True)
        print('### After sort')
        print('\t\t', new_open_list)
        visiting_state = new_open_list.pop()
        print('take list item')
        print(visiting_state)
        current_state = visiting_state
        is_goal = determine_goal(current_state)
        visited_position["{},{}".format(current_state[2], current_state[3])] = 1
        expand[current_state[2]][current_state[3]] = expand_index
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
            print('new open list')
            print('\t{}'.format(new_open_list))

    print('fail')
    return ['fail']

search(init, expand_index)
for i in range(len(expand)):
    print(expand[i])

for i in range(len(goal_policy)):
    print(goal_policy[i])

from collections import deque

grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

goal = [2, 0]
init = [4, 3, 0] # coordination x, y, direction

forward = [[-1, 0], # up
         [0, -1], # left
         [1, 0], # down
         [0, 1]] # right
forward_name = ['up', 'left', 'down', 'right']

cost = [2, 1, 20] # cost for right turn, no turn, left turn
action = [-1, 0, 1] # -1 = right turn, 1 = left turn
action_name = ['R', '#', 'L']

goal_state = [2, 0, 1]
value = [
    [[999 for item in row] for row in grid],
    [[999 for item in row] for row in grid],
    [[999 for item in row] for row in grid],
    [[999 for item in row] for row in grid]
]
strategy = [
    [1, 2, 0], # forward, left, right
    [1, 0, 2], # forward, right, left
    [0, 1, 2], # right, forward, left
    [2, 1, 0]  # left, forward, right
]
policy = [[' ' for item in row] for row in grid]

def valid_position(i, j):
    if (i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]) and
        grid[i][j] != 1):
        return True
    return False

def expand_children_from_goal(state, current_state_cost, value_index, visited_position, new_open_list):
    # Since we are calculating value from goal, which is in reverse
    # The action for calculating orientation and cost is reversed.
    # Treating forward as backward
    for strategy_index in range(len(strategy[value_index])):
        action_index = strategy[value_index][strategy_index]
#        print('Action index = {}'.format(action_index))
        car_orientation = (state[2] - action[action_index]) % 4
#        print('Car orientation = {}'.format(car_orientation))
        new_position_i = state[0] + forward[car_orientation][0]
        new_position_j = state[1] + forward[car_orientation][1]
#        print('    Proposed new position = {},{}'.format(new_position_i, new_position_j))
        if (valid_position(new_position_i, new_position_j) and
                [new_position_i, new_position_j] not in new_open_list):
            value[value_index][new_position_i][new_position_j] = current_state_cost + cost[action_index]
            new_open_list.append([new_position_i, new_position_j, car_orientation])
            break

def update_value():
    for value_index in range(len(value)):
        goal_state_cost = 0
        grid_position_i = goal[0]
        grid_position_j = goal[1]
        goal_state = goal + [0]
        value[value_index][grid_position_i][grid_position_j] = goal_state_cost
        new_open_list = deque()
        new_open_list.append(goal_state)
        visited_position = {}

        while new_open_list:
            explore_state = new_open_list.popleft()
#            print('----- explore state')
#            print(explore_state)
            state_cost = value[value_index][explore_state[0]][explore_state[1]]
            expand_children_from_goal(explore_state, state_cost, value_index, visited_position, new_open_list)
            visited_position['{},{}'.format(explore_state[0], explore_state[1])] = 1
#            print('open_list')
#            print('    ', new_open_list)
        #    print('visited position')
        #    print('    ', visited_position)

def update_policy():
    policy[goal[0]][goal[1]] = '*'
    starting_state = init
    # Find which value grid has the smallest starting value
    starting_value = 999
    smallest_value_grid = 0
    for i in range(len(value)):
        if value[i][init[0]][init[1]] < starting_value:
            starting_value = value[i][init[0]][init[1]]
            smallest_value_grid = i

    print("==== Smallest value gride = {}".format(smallest_value_grid))
    current_i = init[0]
    current_j = init[1]
    current_orientation = init[2]
    while [current_i, current_j] != goal:
        for strategy_index in range(len(strategy[smallest_value_grid])):
            action_index = strategy[smallest_value_grid][strategy_index]
            orientation = (current_orientation + action[action_index]) % 4
            neighbor_i = current_i + forward[orientation][0]
            neighbor_j = current_j + forward[orientation][1]
            if valid_position(neighbor_i, neighbor_j):
                if (policy[neighbor_i][neighbor_j] != ' ' or value[smallest_value_grid][current_i][current_j] > value[smallest_value_grid][neighbor_i][neighbor_j]):
                    policy[current_i][current_j] = action_name[action_index]
                    current_i = neighbor_i
                    current_j = neighbor_j
                    current_orientation = orientation
                    break

update_value()
update_policy()

print('----value----')
for i in range(len(value)):
    print('==== Value {}'.format(i))
    for j in range(len(value[0])):
        print('[', end='')
        for z in range(len(value[0][0])):
            print("{:>3d}  ".format(value[i][j][z]), end='')
        print(']')

print('----policy----')
for i in range(len(policy)):
    print(policy[i])

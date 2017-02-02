from collections import deque

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]

goal = [len(grid) - 1, len(grid[0]) - 1]

delta = [[-1, 0], # up
         [0, -1], # left
         [1, 0], # down
         [0, 1]] # right

delta_name = ['^', '<', 'v', '>']
cost_step = 1

value = [[99 for item in row] for row in grid]
policy = [[' ' for item in row] for row in grid]

def valid_position(i, j):
    if (i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]) and
        grid[i][j] != 1):
        return True
    return False

def expand_children(state, current_state_cost, visited_position, new_open_list):
    for i in range(len(delta)):
        new_position_i = state[0] + delta[i][0]
        new_position_j = state[1] + delta[i][1]
        if (valid_position(new_position_i, new_position_j) and
            '{},{}'.format(new_position_i, new_position_j) not in visited_position and
            [new_position_i, new_position_j] not in new_open_list):
            value[new_position_i][new_position_j] = current_state_cost + cost_step
            new_open_list.append([new_position_i, new_position_j])

def update_value():
    goal_state_cost = 0
    grid_position_i = goal[0]
    grid_position_j = goal[1]
    value[grid_position_i][grid_position_j] = goal_state_cost
    new_open_list = deque()
    new_open_list.append([grid_position_i, grid_position_j])
    visited_position = {}

    while new_open_list:
        explore_state = new_open_list.popleft()
    #    print('----- explore state')
    #    print(explore_state)
        state_cost = value[explore_state[0]][explore_state[1]]
        expand_children(explore_state, state_cost, visited_position, new_open_list)
        visited_position['{},{}'.format(explore_state[0], explore_state[1])] = 1
    #    print('open_list')
    #    print('    ', new_open_list)
    #    print('visited position')
    #    print('    ', visited_position)

def update_policy():
    policy[goal[0]][goal[1]] = '*'
    for i in range(len(value)):
        for j in range(len(value[0])):
            if value[i][j] != 99:
                for m in range(len(delta)):
                    neighbor_i = i + delta[m][0]
                    neighbor_j = j + delta[m][1]
                    if valid_position(neighbor_i, neighbor_j):
                        if value[i][j] > value[neighbor_i][neighbor_j]:
                            policy[i][j] = delta_name[m]
                            break

update_value()
update_policy()

print('----value----')
for i in range(len(value)):
    print(value[i])

print('----policy----')
for i in range(len(policy)):
    print(policy[i])

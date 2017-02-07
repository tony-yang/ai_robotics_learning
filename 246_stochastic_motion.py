from collections import deque

# grid = [[0, 0, 0],
#         [0, 0, 0]]

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]

goal = [0, len(grid[0])-1]

delta = [[-1, 0], # up
         [0, -1], # left
         [1, 0], # down
         [0, 1]] # right

delta_name = ['^', '<', 'v', '>']
cost_step = 1

success_prob = 0.5
collision_cost = 100.0
error_margin = 0.000001

value = [[1000.0 for item in row] for row in grid]
policy = [[' ' for item in row] for row in grid]

def valid_position(child_state):
    if (child_state[0] >= 0 and child_state[0] < len(grid) and
        child_state[1] >= 0 and child_state[1] < len(grid[0]) and
        grid[child_state[0]][child_state[1]] == 0):
        return True
    return False

def not_expanded_before(child_state, new_open_list, visited_position):
    if (child_state not in new_open_list and
        '{},{}'.format(child_state[0], child_state[1]) not in visited_position):
        return True
    return False

def get_position_value(state):
    if valid_position(state):
        return value[state[0]][state[1]]
    else:
        return collision_cost

def expand_children(state, new_open_list, visited_position):
    need_update = []
    for i in range(len(delta)):
        child_state = [state[0] + delta[i][0], state[1] + delta[i][1]]
        if valid_position(child_state) and not_expanded_before(child_state, new_open_list, visited_position):
#            print('----- expand value ----------', child_state)
            new_open_list.append(child_state)
            child_left_index = (i - 1) % 4
            child_right_index = (i + 1) % 4
            child_left_position = [child_state[0] + delta[child_left_index][0], child_state[1] + delta[child_left_index][1]]
#            print('    left of child', child_left_position)
            child_right_position = [child_state[0] + delta[child_right_index][0], child_state[1] + delta[child_right_index][1]]
#            print('    right of child', child_right_position)
#            print('    value = ', value, ' and value -1 ', value[-1][0])
            child_value = (success_prob * value[state[0]][state[1]]
                        + ((1 - success_prob) / 2) * get_position_value(child_left_position)
                        + ((1 - success_prob) / 2) * get_position_value(child_right_position)
                        + cost_step)
#            print('    child value = ', child_value)
            if abs(child_value - value[child_state[0]][child_state[1]]) < error_margin:
                need_update.append('converged')
            else:
                value[child_state[0]][child_state[1]] = child_value
                need_update.append('updated')

    if 'updated' in need_update:
        return 'updated'
    else:
        return 'converged'

def update_value():
    iteration = 1
    starting_state = goal
    visited_position = {}
    new_open_list = deque()
    new_open_list.append(starting_state)
    value[starting_state[0]][starting_state[1]] = 0.0
    need_update = []

    while new_open_list:
        print('---- open list')
        print(new_open_list)
        visit_state = new_open_list.popleft()
        print('---- visiting state')
        print('    ', visit_state)
        result = expand_children(visit_state, new_open_list, visited_position)
        need_update.append(result)
        visit_state_key = '{},{}'.format(visit_state[0], visit_state[1])
        visited_position[visit_state_key] = 1
        if visit_state == goal:
            value[visit_state[0]][visit_state[1]] = 0.0
        if not new_open_list and 'updated' in need_update:
            new_open_list.append(starting_state)
            visited_position = {}
            need_update = []
            iteration += 1
            for i in range(len(value)):
                print(value[i])

    print('## Total {} iterations to converge'.format(iteration))


def update_policy():
    for i in range(len(value)):
        for j in range(len(value[0])):
            if valid_position([i, j]):
                for m in range(len(delta)):
                    new_i = i + delta[m][0]
                    new_j = j + delta[m][1]
                    if valid_position([new_i, new_j]):
                        if value[new_i][new_j] < value[i][j]:
                            policy[i][j] = delta_name[m]
                            break;
    policy[goal[0]][goal[1]] = '*'



update_value()
update_policy()

for i in range(len(value)):
    print(value[i])

for i in range(len(policy)):
    print(policy[i])

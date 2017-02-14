path = [
    [0, 0], # fixed
    [1, 0],
    [2, 0],
    [3, 0],
    [4, 0],
    [5, 0],
    [6, 0], # fixed
    [6, 1],
    [6, 2],
    [6, 3], # fixed
    [5, 3],
    [4, 3],
    [3, 3],
    [2, 3],
    [1, 3],
    [0, 3], # fixed
    [0, 2],
    [0, 1]
]

fix = [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]

def smooth(path, fix, weight_data = 0.1, weight_smooth = 0.1, tolerance = 0.000001):
    newpath = [[0 for col in row] for row in path]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]
    print(newpath)
    iteration_error = [1]
    while max(iteration_error) > tolerance:
        iteration_error = []
        # We want to connect the first and last position smoothly, so it needs to be calculated
        for i in range(len(path)):
            if not fix[i]:
                current_position = newpath[i]

                new_position_x = current_position[0] + weight_smooth * (newpath[(i + 1) % len(path)][0] + newpath[(i - 1) % len(path)][0] - 2 * current_position[0])
                new_position_y = current_position[1] + weight_smooth * (newpath[(i + 1) % len(path)][1] + newpath[(i - 1) % len(path)][1] - 2 * current_position[1])
                neighbor_min_position = [new_position_x, new_position_y]

                new_position_x = neighbor_min_position[0] + weight_smooth / 2 * (2 * newpath[(i - 1) % len(path)][0] - newpath[(i - 2) % len(path)][0] - neighbor_min_position[0])
                new_position_y = neighbor_min_position[1] + weight_smooth / 2 * (2 * newpath[(i - 1) % len(path)][1] - newpath[(i - 2) % len(path)][1] - neighbor_min_position[1])
                smoothed_min_position = [new_position_x, new_position_y]

                new_position_x = smoothed_min_position[0] + weight_smooth / 2 * (2 * newpath[(i + 1) % len(path)][0] - newpath[(i + 2) % len(path)][0] - smoothed_min_position[0])
                new_position_y = smoothed_min_position[1] + weight_smooth / 2 * (2 * newpath[(i + 1) % len(path)][1] - newpath[(i + 2) % len(path)][1] - smoothed_min_position[1])
                neighbor_min_position = [new_position_x, new_position_y]
                newpath[i] = neighbor_min_position

                error_x = abs(neighbor_min_position[0] - current_position[0])
                error_y = abs(neighbor_min_position[1] - current_position[1])
                iteration_error.append(error_x if error_x > error_y else error_y)

        #print('iteration error = ', iteration_error)

    return newpath

newpath = smooth(path, fix)
for i in range(len(path)):
    print('[{:.3f}, {:.3f}] -> [{:.3f}, {:.3f}]'.format(float(path[i][0]), float(path[i][1]), float(newpath[i][0]), float(newpath[i][1])))

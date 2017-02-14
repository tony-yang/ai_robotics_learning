path = [
    [0, 0],
    [1, 0],
    [2, 0],
    [3, 0],
    [4, 0],
    [5, 0],
    [6, 0],
    [6, 1],
    [6, 2],
    [6, 3],
    [5, 3],
    [4, 3],
    [3, 3],
    [2, 3],
    [1, 3],
    [0, 3],
    [0, 2],
    [0, 1]
]

def smooth(path, weight_data = 0.1, weight_smooth = 0.1, tolerance = 0.000001):
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
            unsmoothed_position = path[i]
            current_position = newpath[i]
            new_position_x = current_position[0] + weight_data * (unsmoothed_position[0] - current_position[0])
            new_position_y = current_position[1] + weight_data * (unsmoothed_position[1] - current_position[1])
            unsmoothed_min_position = [new_position_x, new_position_y]

            new_position_x = unsmoothed_min_position[0] + weight_smooth * (newpath[(i + 1) % len(path)][0] + newpath[(i - 1) % len(path)][0] - 2 * unsmoothed_min_position[0])
            new_position_y = unsmoothed_min_position[1] + weight_smooth * (newpath[(i + 1) % len(path)][1] + newpath[(i - 1) % len(path)][1] - 2 * unsmoothed_min_position[1])
            neighbor_min_position = [new_position_x, new_position_y]
            newpath[i] = neighbor_min_position

            error_x = abs(neighbor_min_position[0] - current_position[0])
            error_y = abs(neighbor_min_position[1] - current_position[1])
            iteration_error.append(error_x if error_x > error_y else error_y)

        #print('iteration error = ', iteration_error)

    return newpath

newpath = smooth(path)
for i in range(len(path)):
    print('[{:.3f}, {:.3f}] -> [{:.3f}, {:.3f}]'.format(float(path[i][0]), float(path[i][1]), float(newpath[i][0]), float(newpath[i][1])))

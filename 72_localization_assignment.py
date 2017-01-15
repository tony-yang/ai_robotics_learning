colors=[['red', 'green', 'green', 'red', 'red'],
        ['red', 'red', 'green', 'red', 'red'],
        ['red', 'red', 'green', 'green', 'red'],
        ['red', 'red', 'red', 'red', 'red'],]
measurements = ['green','green','green','green','green']
motions = [[0, 0], [0, 1], [1,0], [1,0], [0, 1]]

sensor_right = 0.7
p_move = 0.8

sensor_wrong = 1 - sensor_right
p_stay = 1 - p_move

def len_2d_lists(list):
    row_count = len(list)
    column_count = len(list[0])
    return (row_count, column_count)

def print_distribution(dist):
    for i in range(len(dist)):
        print(dist[i])

def sense(p, measurement):
    row_count, column_count = len_2d_lists(p)
    output_sense_distribution = []
    total = 0

    for i in range(row_count):
        output_sense_distribution.append([])
        for j in range(column_count):
            hit = (measurement == colors[i][j])
            probability = p[i][j] * (hit * sensor_right + (1 - hit) * sensor_wrong)
            output_sense_distribution[i].append(probability)
            total += probability

    for i in range(row_count):
        for j in range(column_count):
            output_sense_distribution[i][j] /= total

    return output_sense_distribution


def move(p, motion):
    row_count, column_count = len_2d_lists(p)
    output_movement_distribution = []

    for i in range(row_count):
        output_movement_distribution.append([])
        for j in range(column_count):
            movement = p_move * p[(i - motion[0]) % row_count][(j - motion[1]) % column_count]
            movement = movement + p_stay * p[i][j]
            output_movement_distribution[i].append(movement)

    return output_movement_distribution


if len(measurements) != len(motions):
    raise(ValueError, "error in size of measurement/motion vector")

row_count, column_count = len_2d_lists(colors)
uniform_distribution = 1 / (row_count * column_count)

probability = []
for i in range(row_count):
    probability.append([])
    for j in range(column_count):
        probability[i].append(uniform_distribution)

print("=======Initial output=======")
print_distribution(probability)
for k in range(len(measurements)):
    probability = move(probability, motions[k])
    probability = sense(probability, measurements[k])

print("=======Final output=======")
print_distribution(probability)

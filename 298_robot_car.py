from math import *
import random

steering_noise = 0.1
distance_noise = 0.03
measurement_noise = 0.3

class robot:
    def __init__(self, length = 0.5):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.measurement_noise = 0.0
        self.num_collisions = 0
        self.num_steps = 0

    def set(self, new_x, new_y, new_orientation):
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)

    def set_noise(self, new_steering_noise, new_distance_noise, new_measurement_noise):
        self.steering_noise = float(new_steering_noise)
        self.distance_noise = float(new_distance_noise)
        self.measurement_noise = float(new_measurement_noise)

    def check_collision(self, grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    dist = sqrt((self.x - float(i)) ** 2 +
                                (self.y - float(j)) ** 2)
                    if dist < 0.5:
                        self.num_collisions += 1
                        return False

        return True

    def check_goal(self, goal, threshold = 1.0):
        dist = sqrt((float(goal[0]) - self.x) ** 2 + (float(goal[1]) - self.y) ** 2)
        return dist < threshold

    def move(self, grid, steering, distance, tolerance = 0.001, max_steering_angle = pi / 4.0):
        if steering > max_steering_angle:
            steering = max_steering_angle
        elif steering < -max_steering_angle:
            steering = -max_steering_angle

        if distance < 0.0:
            distance = 0.0

        res = robot()
        res.length = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.measurement_noise = self.measurement_noise
        res.num_collisions = self.num_collisions
        res.num_steps = self.num_steps

        steering_with_noise = random.gauss(steering, self.steering_noise)
        distance_with_noise = random.gauss(distance, self.distance_noise)

        turn = tan(steering_with_noise) * distance_with_noise / res.length

        if abs(turn) < tolerance:
            res.x = self.x + distance_with_noise * cos(self.orientation)
            res.y = self.y + distance_with_noise * sin(self.orientation)
            res.Orientation = (self.orientation + turn) % (2 * pi)
        else:
            radius = distance_with_noise / turn
            global_x = self.x - sin(self.orientation) * radius
            global_y = self.y + cos(self.orientation) * radius

            res.x = global_x + sin(self.orientation + turn) * radius
            res.y = global_y - cos(self.orientation + turn) * radius
            res.orientation = (self.orientation + turn) % (2 * pi)

        return res

    def sense(self):
        return [random.gauss(self.x, self.measurement_noise),
                random.gauss(self.y, self.measurement_noise)]

    def measurement_prob(self, measurement):
        error_x = measurement[0] - self.x
        error_y = measurement[1] - self.y

        error = exp(- (error_x ** 2) / (self.measurement_noise ** 2) / 2.0) / sqrt(2.0 * pi * (self.measurement_noise ** 2))
        error *= exp(- (error_y ** 2) / (self.measurement_noise ** 2) / 2.0) / sqrt(2.0 * pi * (self.measurement_noise ** 2))
        return error

    def __repr__(self):
        return '[x={:.5f} y={:.5f} orientation={:.5f}]'.format(self.x, self.y, self.orientation)

def run(grid, goal, spath, PDparams, printflag=False, speed=0.1, timeout=1000):
    myrobot = robot()
    myrobot.set(0., 0., 0.)
    myrobot.set_noise(steering_noise, distance_noise, measurement_noise)
    filter = particles(myrobot.x, myrobot.y, myrobot.orientation, steering_noise, distance_noise, measurement_noise)

    cte = 0.0
    err = 0.0
    N = 0

    index = 0

    while not myrobot.check_goal(goal) and N < timeout:
        diff_cte = -cte

        estimate = filter.get_position()
        cte =

        diff_cte += cte
        steer = -params[0] * cte - params[1] * diff_cte
        myrobot = myrobot.move(grid, steer, speed)
        filter.move(grid, steer, speed)

        Z = myrobot.sense()
        filter.sense(Z)

        if not myrobot.check_collision(grid):
            print '##### Collision #####'

        err += (cte ** 2)


def main(grid, init, goal, steering_noise, distance_noise, measurement_noise, weight_data, weight_smooth, p_gain, d_gain):
    path = plan(grid, init, goal)
    path.astar()
    path.smooth(weight_data, weight_smooth)
    return run(grid, goal, path.spath, [p_gain, d_gain])


grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0]) - 1]

# Initial implementation from the class
# myrobot = robot()
# myrobot.set_noise(steering_noise, distance_noise, measurement_noise)
# print(myrobot)
#
# while not myrobot.check_goal(goal):
#     theta = atan2(goal[1] - myrobot.y, goal[0] - myrobot.x) - myrobot.orientation
#     myrobot = myrobot.move(grid, theta, 0.1)
#     if not myrobot.check_collision(grid):
#         print('##### Collision #####')
#     print(myrobot)

weight_data = 0.1
weight_smooth - 0.2
p_gain = 2.0
d_gain = 6.0

print main(grid, init, goal, steering_noise, distance_noise, measurement_noise, weight_data, weight_smooth, p_gain, d_gain)

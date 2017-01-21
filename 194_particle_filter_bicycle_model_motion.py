from math import *
import random

landmarks = [[20.0, 20.0],
             [80.0, 80.0],
             [20.0, 80.0],
             [80.0, 20.0]]
world_size = 100.0

class robot:
    def __init__(self, length):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0
        self.length = length
        self.bearing_noise = 0.0
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.max_steering_angle = pi

    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError('X coordinate out of bound')
        if new_y < 0 or new_y >= world_size:
            raise ValueError('Y coordinate out of bound')
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise_old(self, new_forward_noise, new_turn_noise, new_sense_noise):
        self.forward_noise = float(new_forward_noise)
        self.turn_noise = float(new_turn_noise)
        self.sense_noise = float(new_sense_noise)

    def set_noise(self, new_bearing_noise, new_steering_noise, new_distance_noise):
        self.bearing_noise = float(new_bearing_noise)
        self.steering_noise = float(new_steering_noise)
        self.distance_noise = float(new_distance_noise)

    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z

    def __repr__(self):
        return '[x={} y={} orientation={}]\n'.format(str(self.x), str(self.y), str(self.orientation))

    def move(self, motion, tolerance=0.001):
        steering_angle = motion[0]
        distance = motion[1]

        if abs(steering_angle) > self.max_steering_angle:
            raise ValueError('Exceeding max steering angle')

        turning_angle = distance / self.length * tan(steering_angle)
        print()
        print("motion = ", steering_angle, distance, " and turning angle = ", turning_angle)

        if abs(turning_angle) < tolerance:
            new_robot_x = self.x + distance * cos(self.orientation)
            new_robot_y = self.y + distance * sin(self.orientation)
            new_robot_orientation = (self.orientation + turning_angle) % (2 * pi)
        else:
            radius = distance / turning_angle
            global_x = self.x - sin(self.orientation) * radius
            global_y = self.y + cos(self.orientation) * radius
            print("radius = ", radius, global_x, global_y)

            new_robot_x = global_x + sin(self.orientation + turning_angle) * radius
            new_robot_y = global_y - cos(self.orientation + turning_angle) * radius
            new_robot_orientation = (self.orientation + turning_angle) % (2 * pi)
            print("new coordinate: ", new_robot_x, new_robot_y, new_robot_orientation)

        new_robot_coordinate = robot(self.length)
        new_robot.bearing_noise = self.bearing_noise
        new_robot.steering_noise = self.steering_noise
        new_robot.distance_noise = self.distance_noise

        steering_noise = random.gauss(steering_angle, self.steering_noise)
        distance_noise = random.gauss(distance, self.distance_noise)

        new_robot_coordinate.set(new_robot_x, new_robot_y, new_robot_orientation)
        return new_robot_coordinate


length = 20
bearing_noise = 0.0
steering_noise = 0.0
distance_noise = 0.0

myrobot = robot(length)
myrobot.set(0.0, 0.0, 0.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

motions = [[0.0, 10.0], [pi / 6.0, 10.0], [0.0, 20.0]]

T = len(motions)

print('Robot:', myrobot)
for t in range(T):
    myrobot = myrobot.move(motions[t])
    print('Robot:', myrobot)

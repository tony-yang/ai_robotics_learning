from math import *
import random

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]]
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
        self.max_steering_angle = 0.0

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

    def set_max_steering_angle(self, new_max_steering_angle):
        self.max_steering_angle = new_max_steering_angle

    def set_noise(self, new_bearing_noise, new_steering_noise, new_distance_noise):
        self.bearing_noise = float(new_bearing_noise)
        self.steering_noise = float(new_steering_noise)
        self.distance_noise = float(new_distance_noise)

    def sense(self, add_noise=1):
        bearing = []

        # This is the implementation from the course
        # I believe the x and y order got reversed. I commented out my implementation
        # just to keep it aligned with the course. But shouldn't the x coordiante be the [0] index
        # and the y coordinate be the [1] index?
        for i in range(len(landmarks)):
            # delta_x = landmarks[i][0] - self.x
            # delta_y = landmarks[i][1] - self.y
            delta_x = landmarks[i][1] - self.x
            delta_y = landmarks[i][0] - self.y
            bearing_to_landmark = atan2(delta_y, delta_x) - self.orientation
            if add_noise:
                bearing_to_landmark += random.gauss(0.0, self.bearing_noise)

            bearing_to_landmark %= 2.0 * pi
            bearing.append(bearing_to_landmark)

        return bearing

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
max_steering_angle = pi / 4.0
bearing_noise = 0.0
steering_noise = 0.0
distance_noise = 0.0

myrobot = robot(length)
myrobot.set(30.0, 20.0, 0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)
myrobot.set_max_steering_angle(max_steering_angle)

#motions = [[0.0, 10.0], [pi / 6.0, 10.0], [0.0, 20.0]]
motions = [[-0.2, 10.] for row in range(10)]

T = len(motions)

print('Robot:', myrobot)
print('Measurement:', myrobot.sense())

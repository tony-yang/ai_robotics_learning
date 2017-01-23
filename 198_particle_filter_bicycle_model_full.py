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

        if abs(turning_angle) < tolerance:
            new_robot_x = self.x + distance * cos(self.orientation)
            new_robot_y = self.y + distance * sin(self.orientation)
            new_robot_orientation = (self.orientation + turning_angle) % (2 * pi)
        else:
            radius = distance / turning_angle
            global_x = self.x - sin(self.orientation) * radius
            global_y = self.y + cos(self.orientation) * radius

            new_robot_x = global_x + sin(self.orientation + turning_angle) * radius
            new_robot_y = global_y - cos(self.orientation + turning_angle) * radius
            new_robot_orientation = (self.orientation + turning_angle) % (2 * pi)

        new_robot_coordinate = robot(self.length)
        new_robot_coordinate.bearing_noise = self.bearing_noise
        new_robot_coordinate.steering_noise = self.steering_noise
        new_robot_coordinate.distance_noise = self.distance_noise
        new_robot_coordinate.max_steering_angle = self.max_steering_angle

        steering_noise = random.gauss(steering_angle, self.steering_noise)
        distance_noise = random.gauss(distance, self.distance_noise)

        new_robot_x = (new_robot_x + distance_noise) % world_size
        new_robot_y = (new_robot_y + distance_noise) % world_size
        new_robot_orientation = (new_robot_orientation + steering_noise) % (2 * pi)

        new_robot_coordinate.set(new_robot_x, new_robot_y, new_robot_orientation)
        return new_robot_coordinate

    def measurement_prob(self, measurements):
        # calculate the correct measurement
        predicted_measurements = self.sense(0)

        # compute errors
        error = 1.0
        for i in range(len(measurements)):
            error_bearing = abs(measurements[i] - predicted_measurements[i])
            error_bearing = (error_bearing + pi) % (2.0 * pi) - pi # truncate
            # update Gaussian
            error *= (exp(- (error_bearing ** 2) / (self.bearing_noise ** 2) / 2.0) /
                      sqrt(2.0 * pi * (self.bearing_noise ** 2)))
        return error



length = 20
max_steering_angle = pi / 4.0
bearing_noise = 0.1
steering_noise = 0.1
distance_noise = 5.0
tolerance_xy = 15.0
tolerance_orientation = 0.25

def get_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # orientation is tricky because it is cyclic. By normalizing
        # around the first particle we are somewhat more robust to
        # the 0=2pi problem
        orientation += (((p[i].orientation - p[0].orientation + pi) % (2.0 * pi))
                        + p[0].orientation - pi)
    return [x / len(p), y / len(p), orientation / len(p)]

def check_output(final_robot, estimated_position):

    error_x = abs(final_robot.x - estimated_position[0])
    error_y = abs(final_robot.y - estimated_position[1])
    error_orientation = abs(final_robot.orientation - estimated_position[2])
    error_orientation = (error_orientation + pi) % (2.0 * pi) - pi
    correct = error_x < tolerance_xy and error_y < tolerance_xy \
              and error_orientation < tolerance_orientation
    return correct

def generate_ground_truth(motions):
    myrobot = robot(length)
    myrobot.set_noise(bearing_noise, steering_noise, distance_noise)
    myrobot.set_max_steering_angle(max_steering_angle)

    Z = []
    T = len(motions)

    for t in range(T):
        myrobot = myrobot.move(motions[t])
        Z.append(myrobot.sense())
    return [myrobot, Z]

def particle_filter(motions, measurements, N=500):
    p = []
    for i in range(N):
        r = robot(length)
        r.set_noise(bearing_noise, steering_noise, distance_noise)
        r.set_max_steering_angle(max_steering_angle)
        p.append(r)

    for t in range(len(motions)):
        p2 = []
        for i in range(N):
            p2.append(p[i].move(motions[t]))
        p = p2

    w = []
    for i in range(N):
        w.append(p[i].measurement_prob(measurements[t]))

    p3 = []
    index = random.randint(0, N-1)
    beta = 0.0
    weight_max = max(w)
    for i in range(N):
        beta += random.uniform(0, 2 * weight_max)
        while w[index] < beta:
            beta -= w[index]
            index = (index + 1) % N

        p3.append(p[index])
    p = p3
    return get_position(p)



#motions = [[0.0, 10.0], [pi / 6.0, 10.0], [0.0, 20.0]]
motions = [[2. * pi / 10, 20.] for row in range(8)]
measurements = [[4.746936, 3.859782, 3.045217, 2.045506],
               [3.510067, 2.916300, 2.146394, 1.598332],
               [2.972469, 2.407489, 1.588474, 1.611094],
               [1.906178, 1.193329, 0.619356, 0.807930],
               [1.352825, 0.662233, 0.144927, 0.799090],
               [0.856150, 0.214590, 5.651497, 1.062401],
               [0.194460, 5.660382, 4.761072, 2.471682],
               [5.717342, 4.736780, 3.909599, 2.342536]]

particle_filter(motions, measurements)

#Test cases for verifying the code
number_of_iterations = 8
motions = [[2. * pi / 10, 20.] for row in range(number_of_iterations)]
measurements = [[4.746936, 3.859782, 3.045217, 2.045506],
               [3.510067, 2.916300, 2.146394, 1.598332],
               [2.972469, 2.407489, 1.588474, 1.611094],
               [1.906178, 1.193329, 0.619356, 0.807930],
               [1.352825, 0.662233, 0.144927, 0.799090],
               [0.856150, 0.214590, 5.651497, 1.062401],
               [0.194460, 5.660382, 4.761072, 2.471682],
               [5.717342, 4.736780, 3.909599, 2.342536]]

x = generate_ground_truth(motions)
final_robot = x[0]
measurements = x[1]
estimated_position = particle_filter(motions, measurements)

print('Ground truth:', final_robot)
print('Particle filter:', estimated_position)
print('Code check:', check_output(final_robot, estimated_position))

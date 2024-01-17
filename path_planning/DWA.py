import math
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np

show_animation = True
DT = 0.2

def obstacle_particles(x, y, w, l):
    D = 3
    top = [[i, y + l/2] for i in np.linspace(x-w/2, x+w/2, D)]
    bottom = [[i, y - l/2] for i in np.linspace(x-w/2, x+w/2, D)]
    left = [[x - w/2, i] for i in np.linspace(y-l/2, y+l/2, D)]
    right = [[x + w/2, i] for i in np.linspace(y-l/2, y+l/2, D)]

    return top + bottom + left + right

def boundary(w, l):
    D = 15

    y_bottom = -5

    top = [[i, l/2] for i in np.linspace(-w/2, w/2, D)]
    bottom = [[i, -l/2] for i in np.linspace(-w/2, w/2, D)]
    left = [[-w/2, i] for i in np.linspace(-l/2, l/2, D)]
    right = [[w/2, i] for i in np.linspace(-l/2, l/2, D)]

    return top + bottom + left + right

def create_map(positions, w, l):
    m = []
    for x, y in positions:
        m += obstacle_particles(x, y, w, l)

    b = boundary(2.4, 2.4)

    return m + b

def dwa_control(x, config, goal, ob):

    dw = calc_dynamic_window(x, config)

    u, trajectory = calc_control_and_trajectory(x, dw, config, goal, ob)

    return u, trajectory


class RobotType(Enum):
    circle = 0
    rectangle = 1


class Config:

    def __init__(self):
        # robot parameter
        self.max_speed = 4.0  # [m/s]
        self.min_speed = -1.5  # [m/s]
        self.max_yaw_rate = 60.0 * math.pi / 180.0  # [rad/s]
        self.max_accel = 0.3  # [m/ss]
        self.max_delta_yaw_rate = 60.0 * math.pi / 180.0  # [rad/ss]
        self.v_resolution = 0.01  # [m/s]
        self.yaw_rate_resolution = 0.1 * math.pi / 180.0  # [rad/s]
        self.dt = DT  # [s] Time tick for motion prediction
        self.predict_time = 3.0  # [s]


        # (1)Change paremeters
        #####
        self.to_goal_cost_gain = 0.15
        self.speed_cost_gain = 1.2
        self.obstacle_cost_gain = 0.13
        #####




        self.robot_stuck_flag_cons = 0.001  # constant to prevent robot stucked
        self.robot_type = RobotType.circle

        # if robot_type == RobotType.circle
        # Also used to check if goal is reached in both types
        self.robot_radius = 0.15  # [m] for collision check

        # if robot_type == RobotType.rectangle
        self.robot_width = 0.2  # [m] for collision check
        self.robot_length = 0.2  # [m] for collision check
        # obstacles [x(m) y(m), ....]

        space_y = 0.5
        self.ob = np.array(create_map([[-0.35, 0.35], [-0.35, -0.35], [0.35, 0.35], [0.35, -0.35]], 0.2, 0.2))
        
    
    @property
    def robot_type(self):
        return self._robot_type

    @robot_type.setter
    def robot_type(self, value):
        if not isinstance(value, RobotType):
            raise TypeError("robot_type must be an instance of RobotType")
        self._robot_type = value


config = Config()

def motion(x, u, dt):

    x[2] += u[1] * dt
    x[0] += u[0] * math.cos(x[2]) * dt
    x[1] += u[0] * math.sin(x[2]) * dt
    x[3] = u[0]
    x[4] = u[1]

    return x


def calc_dynamic_window(x, config):

    # Dynamic window from robot specification
    Vs = [config.min_speed, config.max_speed,
          -config.max_yaw_rate, config.max_yaw_rate]

    # Dynamic window from motion model
    Vd = [x[3] - config.max_accel * config.dt,
          x[3] + config.max_accel * config.dt,
          x[4] - config.max_delta_yaw_rate * config.dt,
          x[4] + config.max_delta_yaw_rate * config.dt]

    #  [v_min, v_max, yaw_rate_min, yaw_rate_max]
    dw = [max(Vs[0], Vd[0]), min(Vs[1], Vd[1]),
          max(Vs[2], Vd[2]), min(Vs[3], Vd[3])]

    return dw


def predict_trajectory(x_init, v, y, config):


    x = np.array(x_init)
    trajectory = np.array(x)
    time = 0
    while time <= config.predict_time:
        x = motion(x, [v, y], config.dt)
        trajectory = np.vstack((trajectory, x))
        time += config.dt

    return trajectory


def calc_control_and_trajectory(x, dw, config, goal, ob):

    x_init = x[:]
    min_cost = float("inf")
    best_u = [0.0, 0.0]
    best_trajectory = np.array([x])

    # evaluate all trajectory with sampled input in dynamic window
    for v in np.arange(dw[0], dw[1], config.v_resolution):
        for y in np.arange(dw[2], dw[3], config.yaw_rate_resolution):

            trajectory = predict_trajectory(x_init, v, y, config)
            # calc cost
            to_goal_cost = config.to_goal_cost_gain * calc_to_goal_cost(trajectory, goal)
            speed_cost = config.speed_cost_gain * (config.max_speed - trajectory[-1, 3])
            ob_cost = config.obstacle_cost_gain * calc_obstacle_cost(trajectory, ob, config)

            final_cost = to_goal_cost + speed_cost + ob_cost

            # search minimum trajectory
            if min_cost >= final_cost:
                min_cost = final_cost
                best_u = [v, y]
                best_trajectory = trajectory
                if abs(best_u[0]) < config.robot_stuck_flag_cons \
                        and abs(x[3]) < config.robot_stuck_flag_cons:
                    # to ensure the robot do not get stuck in
                    # best v=0 m/s (in front of an obstacle) and
                    # best omega=0 rad/s (heading to the goal with
                    # angle difference of 0)
                    best_u[1] = -config.max_delta_yaw_rate
    return best_u, best_trajectory


def calc_obstacle_cost(trajectory, ob, config):
    """
    calc obstacle cost inf: collision
    """
    ox = ob[:, 0]
    oy = ob[:, 1]
    dx = trajectory[:, 0] - ox[:, None]
    dy = trajectory[:, 1] - oy[:, None]
    r = np.hypot(dx, dy)

    if config.robot_type == RobotType.rectangle:
        yaw = trajectory[:, 2]
        rot = np.array([[np.cos(yaw), -np.sin(yaw)], [np.sin(yaw), np.cos(yaw)]])
        rot = np.transpose(rot, [2, 0, 1])
        local_ob = ob[:, None] - trajectory[:, 0:2]
        local_ob = local_ob.reshape(-1, local_ob.shape[-1])
        local_ob = np.array([local_ob @ x for x in rot])
        local_ob = local_ob.reshape(-1, local_ob.shape[-1])
        upper_check = local_ob[:, 0] <= config.robot_length / 2
        right_check = local_ob[:, 1] <= config.robot_width / 2
        bottom_check = local_ob[:, 0] >= -config.robot_length / 2
        left_check = local_ob[:, 1] >= -config.robot_width / 2
        if (np.logical_and(np.logical_and(upper_check, right_check),
                           np.logical_and(bottom_check, left_check))).any():
            return float("Inf")
    elif config.robot_type == RobotType.circle:
        if np.array(r <= config.robot_radius).any():
            return float("Inf")

    min_r = np.min(r)
    return 1.0 / min_r  


def calc_to_goal_cost(trajectory, goal):

    dx = goal[0] - trajectory[-1, 0]
    dy = goal[1] - trajectory[-1, 1]
    error_angle = math.atan2(dy, dx)
    cost_angle = error_angle - trajectory[-1, 2]
    cost = abs(math.atan2(math.sin(cost_angle), math.cos(cost_angle)))

    return cost


def plot_arrow(x, y, yaw, length=0.5, width=0.1):  # pragma: no cover
    plt.arrow(x, y, length * math.cos(yaw), length * math.sin(yaw),
              head_length=width, head_width=width)
    plt.plot(x, y)


def plot_trajectory_data(trajectory):
    x_data = [state[0] for state in trajectory]
    y_data = [state[1] for state in trajectory]
    yaw_data = [state[2] for state in trajectory]
    v_data = [state[3] for state in trajectory]
    omega_data = [state[4] for state in trajectory]

    # Creating time data assuming constant dt between states
    dt = DT  # Change this value to your actual dt
    time_data = [i * dt for i in range(len(trajectory))]
    fig, axs = plt.subplots(5, 1, figsize=(12, 6))  # 5 subplots for x, y, yaw, v, omega

    axs[0].plot(time_data, x_data, label='X Position')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('X [m]')
    axs[0].legend()

    axs[1].plot(time_data, y_data, label='Y Position')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('Y [m]')
    axs[1].legend()

    axs[2].plot(time_data, [math.degrees(yaw) for yaw in yaw_data], label='Yaw Angle')
    axs[2].set_xlabel('Time [s]')
    axs[2].set_ylabel('Yaw [degrees]')
    axs[2].legend()

    axs[3].plot(time_data, v_data, label='Linear Velocity')
    axs[3].set_xlabel('Time [s]')
    axs[3].set_ylabel('Velocity [m/s]')
    axs[3].legend()

    axs[4].plot(time_data, [math.degrees(omega) for omega in omega_data], label='Angular Velocity')
    axs[4].set_xlabel('Time [s]')
    axs[4].set_ylabel('Angular Velocity [degrees/s]')
    axs[4].legend()

    plt.tight_layout()
def plot_robot(x, y, yaw, config):  # pragma: no cover
    if config.robot_type == RobotType.rectangle:
        outline = np.array([[-config.robot_length / 2, config.robot_length / 2,
                             (config.robot_length / 2), -config.robot_length / 2,
                             -config.robot_length / 2],
                            [config.robot_width / 2, config.robot_width / 2,
                             - config.robot_width / 2, -config.robot_width / 2,
                             config.robot_width / 2]])
        Rot1 = np.array([[math.cos(yaw), math.sin(yaw)],
                         [-math.sin(yaw), math.cos(yaw)]])
        outline = (outline.T.dot(Rot1)).T
        outline[0, :] += x
        outline[1, :] += y
        plt.plot(np.array(outline[0, :]).flatten(),
                 np.array(outline[1, :]).flatten(), "-k")
    elif config.robot_type == RobotType.circle:
        circle = plt.Circle((x, y), config.robot_radius, color="b")
        plt.gcf().gca().add_artist(circle)
        out_x, out_y = (np.array([x, y]) +
                        np.array([np.cos(yaw), np.sin(yaw)]) * config.robot_radius)
        plt.plot([x, out_x], [y, out_y], "-k")


def main(robot_type=RobotType.circle):
    print(__file__ + " start!!")
    # initial state [x(m), y(m), yaw(rad), v(m/s), omega(rad/s)]
    x = np.array([-0.9, -1, math.pi/2.0, 0.0, 0.0])
   
    # (2) Expeirment with different position [x(m), y(m)]
    gx = 0.6
    gy = 1.0
    goal = np.array([gx, gy])

    config.robot_type = robot_type
    trajectory = np.array(x)
    ob = config.ob

    v_history = []
    while True:
        u, predicted_trajectory = dwa_control(x, config, goal, ob)

        print("type of u", type(u))
        print(u)

        print("type of predicted_trajector", type(predicted_trajectory))
        print(predicted_trajectory)
        v_history.append(u)
        np.transpose(np.array(v_history))

        x = motion(x, u, config.dt)  # simulate robot
        trajectory = np.vstack((trajectory, x))  # store state history

        if show_animation:
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
            plt.plot(predicted_trajectory[:, 0], predicted_trajectory[:, 1], "-g")
            plt.plot(x[0], x[1], "xr")
            plt.plot(goal[0], goal[1], "xb")

            plt.plot(ob[:, 0], ob[:, 1], "ok", markersize=3)
            
            plot_robot(x[0], x[1], x[2], config)
            plot_arrow(x[0], x[1], x[2])
            plt.axis("equal")
            plt.xlim(-2, 2)
            plt.ylim(-2, 2)
            plt.grid(True)
            plt.pause(0.0001)

        # check reaching goal
        dist_to_goal = math.hypot(x[0] - goal[0], x[1] - goal[1])
        if dist_to_goal <= config.robot_radius:
            print("Goal!!")
            break

    print("Done")
    if show_animation:
        plt.plot(trajectory[:, 0], trajectory[:, 1], "-r")
        plt.pause(0.0001)

        plot_trajectory_data(trajectory)

        plt.show()

        


if __name__ == '__main__':

    # obstacle_particles(-4.5, 5, 3, 6)
    main(robot_type=RobotType.rectangle)
    # main(robot_type=RobotType.circle)
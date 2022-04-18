import numpy as np
import matplotlib.pyplot as plt

TIME_STEP = 0.01
AT_TARGET_ACCEPTANCE_THRESHOLD = 0.01
SHOW_ANIMATION = True
SHOW_TRAJECTORY = True
PLOT_WINDOW_SIZE_X = 20
PLOT_WINDOW_SIZE_Y = 20
PLOT_FONT_SIZE = 8
TIME_DURATION = 10.0

simulation_running = True
all_robots_are_at_target = False

def run_simulation(robots):
    """Simulates all robots simultaneously"""
    global all_robots_are_at_target
    global simulation_running

    trajectories = dict()

    robot_names = []
    for instance in robots:
        robot_names.append(instance.name)
        trajectories[instance.name] = instance.generate_trajectory(TIME_STEP)

    time = 0
    while simulation_running and time < TIME_DURATION:
        time += TIME_STEP
        robots_are_at_target = []

        for instance in robots:
            if not instance.is_at_target:
                instance.move()
            robots_are_at_target.append(instance.is_at_target)

        if all(robots_are_at_target):
            simulation_running = False

        if SHOW_ANIMATION:
            plt.cla()
            plt.xlim(0, PLOT_WINDOW_SIZE_X)
            plt.ylim(0, PLOT_WINDOW_SIZE_Y)

            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])

            plt.text(0.3, PLOT_WINDOW_SIZE_Y - 1,
                     'Time: {:.2f}'.format(time),
                     fontsize=PLOT_FONT_SIZE)

            plt.text(0.3, PLOT_WINDOW_SIZE_Y - 2,
                     'Reached target: {} = '.format(robot_names)
                     + str(robots_are_at_target),
                     fontsize=PLOT_FONT_SIZE)

            for instance in robots:
                plt.arrow(instance.pose_start.x,
                          instance.pose_start.y,
                          np.cos(instance.pose_start.theta),
                          np.sin(instance.pose_start.theta),
                          color='r',
                          width=0.1)
                plt.arrow(instance.pose_target.x,
                          instance.pose_target.y,
                          np.cos(instance.pose_target.theta),
                          np.sin(instance.pose_target.theta),
                          color='g',
                          width=0.1)
                plot_vehicle(instance.pose.x,
                             instance.pose.y,
                             instance.pose.theta,
                             instance.x_traj,
                             instance.y_traj, instance.color)

            plt.pause(TIME_STEP)

    if SHOW_TRAJECTORY:
        for k, v in trajectories.items():
            fig, ax = plt.subplots()
            new_poses = []
            for pose in v[1]:
                new_poses.append([pose.x, pose.y, pose.theta])
            new_poses = np.array(new_poses)
            ax.plot(v[0], new_poses)
            ax.set_title("Minimum Jerk Trajectory")
            ax.set_xlabel("Time")
            ax.set_ylabel("Position")
        
        plt.show()


def plot_vehicle(x, y, theta, x_traj, y_traj, color):
    # Corners of triangular vehicle when pointing to the right (0 radians)
    p1_i = np.array([0.5, 0, 1]).T
    p2_i = np.array([-0.5, 0.25, 1]).T
    p3_i = np.array([-0.5, -0.25, 1]).T

    T = transformation_matrix(x, y, theta)
    p1 = T @ p1_i
    p2 = T @ p2_i
    p3 = T @ p3_i

    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color+'-')
    plt.plot([p2[0], p3[0]], [p2[1], p3[1]], color+'-')
    plt.plot([p3[0], p1[0]], [p3[1], p1[1]], color+'-')

    plt.plot(x_traj, y_traj, color+'--')


def transformation_matrix(x, y, theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), x],
        [np.sin(theta), np.cos(theta), y],
        [0, 0, 1]
    ])

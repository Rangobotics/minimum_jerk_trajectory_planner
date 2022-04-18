from trajectory_planner.Pose import Pose
from trajectory_planner.TrajectoryPlanners import MinimumJerkTrajectoryPlanner
from trajectory_planner.Robot import Robot
from trajectory_planner.simulation import run_simulation

def main():
    controller = MinimumJerkTrajectoryPlanner()
    pose_target1 = Pose(10, 10, -3.14)
    pose_target2 = Pose(5, 5, 0)
    pose_target3 = Pose(18, 18, 1.57)

    pose_start_1 = Pose(10, 10, 0)
    pose_start_2 = Pose(1, 5, 0)
    pose_start_3 = Pose(18, 3, 1.57)

    robot_1 = Robot("Yellow Robot", "y", 0.5, controller, pose_start_1, pose_target1)
    robot_2 = Robot("Black Robot", "k", 1.0, controller, pose_start_2, pose_target2)
    robot_3 = Robot("Blue Robot", "b", 3.0, controller, pose_start_3, pose_target3)

    robots: list[Robot] = [robot_1, robot_2, robot_3]

    run_simulation(robots)


if __name__ == '__main__':
    main()
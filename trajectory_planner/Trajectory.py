from .Velocity import Velocity

class Trajectory:
    def __init__(self, timestamps, poses):
        self.timestamps = timestamps
        self.poses = poses
        self.__set_velocities()

    def __set_velocities(self):
        for k in range(len(self.poses)):
            if k > len(self.poses):
                break

            dt = self.timestamps[k+1] - self.timestamps[k]
            vx = (self.poses[k+1].x - self.poses[k].x) / dt
            vy = (self.poses[k+1].y - self.poses[k].y) / dt
            vtheta = (self.poses[k+1].theta - self.poses[k].theta) / dt
            
            v = Velocity(vx, vy, vtheta)
            self.trajectory.append(v)

    def __getitem__(self, item):
        return self.trajectory[item]
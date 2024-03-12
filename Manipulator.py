import numpy as np
from numpy import cos as c, sin as s
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

from scipy import optimize

np.random.seed(0)

class Manipulator:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

        self.target = np.zeros(2,)
        self.goal = np.zeros(2,)
        self.theta = np.array([np.pi/2, 0, 0])

        self.holding = False

    def reset(self):

        r, th = np.random.uniform([2, 0], [3, np.pi], 2)
        self.target = np.array([r*c(th), r*s(th)])

        r, th = np.random.uniform([2, 0], [3, np.pi], 2)
        self.goal = np.array([r*c(th), r*s(th)])

        self.holding = False


    def homogeneous(self, th, x, y):
        H = np.array([[c(th), -s(th), x],
                      [s(th),  c(th), y],
                      [0,      0,     1]])
        return H
    
    def fk_error(self, theta, args):
        th1, th2, th3 = theta
        target = args

        H1 = self.homogeneous(th1, c(th1), s(th1))
        H2 = self.homogeneous(th2, c(th2), s(th2))
        H3 = self.homogeneous(th3, c(th3), s(th3))

        o = np.array([[0], [0], [1]])
        o_ = H1 @ H2 @ H3 @ o

        return np.sum(np.square(o_[:2, 0] - target))
        # return o_[:2, 0] - target
    
    def get_robot_state(self):
        th1, th2, th3 = self.theta
        H1 = self.homogeneous(th1, c(th1), s(th1))
        H2 = self.homogeneous(th2, c(th2), s(th2))
        H3 = self.homogeneous(th3, c(th3), s(th3))

        o = np.array([[0],[0],[1]])
        o1 = H1 @ o
        o2 = H1 @ H2 @ o
        o3 = H1 @ H2 @ H3 @ o

        x = [o_[0, 0] for o_ in [o, o1, o2, o3]]
        y = [o_[1, 0] for o_ in [o, o1, o2, o3]]

        return x, y
    
    def render(self):
        self.ax.clear()

        x, y = self.get_robot_state()

        plt.plot(self.goal[0], self.goal[1], 'gs', markersize=10)
        if not self.holding:
            plt.plot(self.target[0], self.target[1], 'ko', markersize=10)
        else:
            plt.plot(x[-1], y[-1], 'ko', markersize=10)


        self.ax.plot(x, y, 'o-', linewidth=3)

        self.ax.plot([-5, 5], [0, 0], 'k--')  # Ground line
        self.ax.axis('equal')
        self.ax.set_xlim([-4, 4])
        self.ax.set_ylim([-1, 4])
        # self.ax.set_xlabel('X Position')
        # self.ax.set_ylabel('Y Position')
        self.ax.set_title('Planar 3dof Manipulator ')
        plt.pause(.01)


    def control(self, target):

        # th0 = [np.arctan2(target[1], target[2]), 0, 0]

        res = optimize.minimize(self.fk_error, x0=[np.arctan2(target[1], target[0])+.1, 0, 0], args=target, bounds=[(-np.pi, np.pi)]*3)
        # res = optimize.root(self.fk_error, x0=[0, 0, 0], args=target)

        th1, th2, th3 = res.x
        
        n = 25
        th1 = np.linspace(self.theta[0], th1, n)
        th2 = np.linspace(self.theta[1], th2, n)
        th3 = np.linspace(self.theta[2], th3, n)

        for theta in zip(th1, th2, th3):
            self.ax.clear()
            self.theta = np.array(theta)
            self.render()
        # plt.show()


if __name__ == "__main__":
    m = Manipulator()
    for i in range(5):
        m.reset()
        m.control(m.target)
        m.holding=True
        m.control(m.goal)
        plt.pause(1)


import numpy as np
from numpy import cos as c, sin as s
import matplotlib.pyplot as plt
import imageio
import os


# np.random.seed(0)

class Manipulator:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

        self.target = np.zeros(2,)
        self.goal = np.zeros(2,)
        self.theta = np.array([np.pi/2, 0])

        self.holding = False

    def reset(self):

        r, th = np.random.uniform([2, 0], [1.99, np.pi], 2)
        self.target = np.array([r*c(th), r*s(th)])

        r, th = np.random.uniform([.5, 0], [1.99, np.pi], 2)
        self.goal = np.array([r*c(th), r*s(th)])

        self.holding = False

    def homogeneous(self, th, x, y):
        return np.array([[c(th), -s(th), x],
                      [s(th),  c(th), y],
                      [0,      0,     1]])
    
    def get_robot_state(self):
        th1, th2 = self.theta
        H1 = self.homogeneous(th1, c(th1), s(th1))
        H2 = self.homogeneous(th2, c(th2), s(th2))

        o = np.array([[0],[0],[1]])
        o1 = H1 @ o
        o2 = H1 @ H2 @ o

        x = [o_[0, 0] for o_ in [o, o1, o2]]
        y = [o_[1, 0] for o_ in [o, o1, o2]]

        return x, y
    
    def render(self):
        self.ax.clear()

        x, y = self.get_robot_state()

        plt.plot(self.goal[0], self.goal[1], 'gs', markersize=10)

        if ((self.target[0] - x[-1])**2 +(self.target[1] - y[-1])**2)**.5 < .01:
            self.holding = True

        if not self.holding:
            plt.plot(self.target[0], self.target[1], 'ko', markersize=10)
        else:
            plt.plot(x[-1], y[-1], 'ko', markersize=10)

        self.ax.plot(x, y, 'o-', linewidth=3)

        self.ax.plot([-5, 5], [0, 0], 'k--')  # Ground line
        self.ax.axis('equal')
        self.ax.set_xlim([-3, 3])
        self.ax.set_ylim([-1, 3])
        # self.ax.set_title('Planar 3dof Manipulator ')

    def control(self, target):

        l1, l2 = 1, 1

        th2 = np.arccos((target[0]**2 + target[1]**2 - l1**2 - l2**2) / (2*l1*l2))
        th1 = np.arctan2(target[1], target[0]) - np.arctan2(l2*s(th2), l1 + l2*c(th2))

        n = int(max(abs(th1 - self.theta[0]), abs(th2 - self.theta[1])) * 10)

        th1 = np.linspace(self.theta[0], th1, n)
        th2 = np.linspace(self.theta[1], th2, n)

        return th1, th2

if __name__ == "__main__":
    m = Manipulator()
    frames = []
    for i in range(30):
        m.reset()

        for j in range(2):
            th1, th2 = m.control(m.target if j == 0 else m.goal)
            for theta in zip(th1, th2):
                m.theta = np.array(theta)
                m.render()
                plt.savefig("frame.png")  # Save each frame as the same PNG file
                frames.append(imageio.imread("frame.png"))
                os.remove("frame.png")  # Remove the PNG file after adding it to the frames list

        plt.savefig("frame.png")  # pause
        frames.append(imageio.imread("frame.png"))
        frames.append(imageio.imread("frame.png"))
        os.remove("frame.png")

    # Save frames as a GIF
    imageio.mimsave('Manipulator2d.gif', frames, fps=30)

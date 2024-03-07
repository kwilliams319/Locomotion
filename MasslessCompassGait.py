import numpy as np
from numpy import sin as s, cos as c
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class MasslessCompassGait:
    def __init__(self):
        self.length = .5  # Length of the pendulum
        self.damping = 0.1  # Damping coefficient
        self.dt = 0.0001  # seconds between state updates

        self.state = np.zeros(2, dtype=np.float32)  # Initial state: [theta, theta_dot]
        self.state[0] = .01

        self.gamma = np.pi/15
        self.alpha = np.pi/6

        self.x0 = 0
        self.y0 = 0

        self.swing_theta = 0
        self.j = 0

        self.fig, self.ax = plt.subplots()
        self.ani = FuncAnimation(self.fig, self._update, frames=260, interval=1, repeat=False)

    def _update(self, i):
        for _ in range(500):
            self.state += self.dynamics() * self.dt
        self.render()
        return self.ax

    def dynamics(self):
        theta, theta_d = self.state

        if theta >= (self.gamma + self.alpha):
            # plt.show()
            l = self.length
            leg = np.array([[0],
                            [-l],
                            [1]])
            th = -theta + 2*self.alpha
            xc = l*s(theta)
            yc = l*c(theta)
            H = np.array([[c(th), -s(th), xc],
                          [s(th),  c(th), yc],
                          [0,      0,     1]])
            leg_in_world = H @ leg
            self.x0 += leg_in_world[0, 0]
            self.y0 += leg_in_world[1, 0]
            self.state[0] -= 2*self.alpha
            self.state[1] *= c(2*self.alpha)

            self.swing_theta = -2*self.alpha

            self.j = (self.j + 1) % 2

        self.swing_theta += 4*self.dt

        return np.array([theta_d, 9.81*np.sin(theta)])
   
    def render(self):
        theta = self.state[0]
        l = self.length

        self.ax.clear()

        # Ground
        x = [-np.cos(self.gamma)*10, np.cos(self.gamma)*10]
        y = [np.sin(self.gamma)*10, -np.sin(self.gamma)*10]
        self.ax.plot(x, y, 'k-')

        leg = np.array([[0, 0, 0],
                        [-l, 0, l],
                        [1, 1, 1]])
        
        # for i in range(2):
        th = -theta
        xc = l*s(theta) + self.x0
        yc = l*c(theta) + self.y0
        H = np.array([[c(th), -s(th), xc],
                        [s(th),  c(th), yc],
                        [0,      0,     1]])
        leg_in_world = H @ leg
            

        # swing leg
        if self.swing_theta > 2*self.alpha:
             self.swing_theta = 2*self.alpha

        th = -theta + self.swing_theta
        xc = l*s(theta) + self.x0
        yc = l*c(theta) + self.y0
        H = np.array([[c(th), -s(th), xc],
                        [s(th),  c(th), yc],
                        [0,      0,     1]])
        leg_in_world2 = H @ leg

        if self.j == 0:
            self.ax.plot(leg_in_world[0], leg_in_world[1], '-')
            self.ax.plot(leg_in_world2[0], leg_in_world2[1], '-')
        else:
            self.ax.plot(leg_in_world2[0], leg_in_world2[1], '-')
            self.ax.plot(leg_in_world[0], leg_in_world[1], '-')


        self.ax.scatter(leg_in_world[0, 1], leg_in_world[1, 1])  # Mass

        self.ax.axis('equal')
        self.ax.set_xlim([-1, 7])
        self.ax.set_ylim([-1, 1])

        return self.ax

if __name__ == "__main__":
    env = MasslessCompassGait()
    env.ani.save('MasslessCompassGait.gif', writer='imagemagick', fps=30)
    # plt.show()

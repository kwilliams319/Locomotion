import numpy as np
import matplotlib.pyplot as plt
import imageio

class Bball:
    def __init__(self):
        self.g = 9.81  # Gravity acceleration
        self.dt = 0.01  # seconds between state updates
        self.frames = []

        # Initial state: [x, z, vx, vz]
        self.q = np.array([2, 2, 3, 5], dtype=np.float32)

        self.fig, self.ax = plt.subplots()
        # self.ani = self.animation()

        self.contact = False

    def update(self, i):
        for _ in range(5):
            self.q = self.dynamics()
        self.render()
        plt.savefig("frame.png")  # Save each frame as a PNG image
        self.frames.append(imageio.imread("frame.png"))  # Append each frame to the frames list

    def dynamics(self):
        x, z, xd, zd = self.q
        h = self.dt

        if z <= 0:
            self.q[3] = -self.q[3]
            self.q[2] =  self.q[2]
            self.contact = True

        if self.contact and z >= 0:
            self.contact = False
            self.q[3] *= .9
            self.q[2] *= .9

        q_dot = np.array([ self.q[2],
                    self.q[3],
                    0,
                    -self.g])

        return self.q + q_dot*self.dt

    def render(self):
        self.ax.clear()
        self.ax.plot([0, 20], [0, 0], 'k-')  # Ground line
        self.ax.plot(self.q[0], self.q[1], 'o', color='orange', markersize=20)

        self.ax.axis('equal')
        self.ax.set_xlim([0, 20])
        self.ax.set_ylim([-1, 6])  # Adjusted y limit to accommodate ground line
        # self.ax.set_xlabel('X Position')
        # self.ax.set_ylabel('Z Position')
        # self.ax.set_title('Basketball Trajectory')

    def animation(self):
        for i in range(150):
            self.update(i)
        # Save frames as a GIF
        imageio.mimsave('Basketball.gif', self.frames, fps=30, loop=0)

if __name__ == "__main__":
    bball = Bball()
    bball.animation()
    # plt.show()
    print('done')

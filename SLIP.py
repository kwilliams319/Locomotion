import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

class SLIP:
    def __init__(self):
        self.q = np.array([-1., 3., 5., 0.])  # x, z, xd, zd, 0
        self.th = 0
        self.free = 1

        self.c = 'g'

        # Create a folder to save images
        self.image_folder = "images"
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)
        self.frame_count = 0

    def render(self, save_image=True):
        plt.cla()

        plt.plot([-3, 3], [0, 0], 'b-')

        if self.free:
            x, z = self.q[:2]
            x_ = x + np.array([0, np.sin(self.th)])
            z_ = z + np.array([0, -np.cos(self.th)])

        if not self.free:
            r, th, rd, thd, x0 = self.q
            x_ = np.array([-r*np.sin(th), 0]) + x0
            z_ = np.array([r*np.cos(th), 0])

        plt.plot(x_, z_, 'ko--', markersize=4)
        plt.plot(x_[0], z_[0], 'o', markersize=12, color=self.c)

        plt.axis('equal')
        plt.xlim([-3, 3])
        plt.ylim([-1, 5])

        if save_image:
            plt.savefig(f"{self.image_folder}/frame_{self.frame_count:03d}.png")

        plt.pause(.01)
        self.frame_count += 1

    def free_dyn(self):
        x, z, xd, zd = self.q
        g = 9.81
        return np.array([xd, zd, 0, -g])

    def stance_dyn(self):
        g = 9.81

        r, th, rd, thd, _ = self.q

        m, l0, k = 1, 1, 500

        rdd = 1/m*(m*r*thd**2 - m*g*np.cos(th) + k*(l0 - r))

        thdd = 1/r*(-2*rd*thd + g*np.sin(th))

        return np.array([rd, thd, rdd, thdd, 0])

    def simulate(self, num_iterations):
        
        for _ in range(num_iterations):
            j = 0
            while self.free:
                self.th = self.q[0] * .1
                self.q += self.free_dyn()*.02

                if self.q[1] - np.cos(self.th) < 0:
                    self.free = 0
                    self.q = np.array([1., self.th, .4*self.q[3], 0., self.q[0] + np.sin(self.th)])

                if j % 5 == 0:
                    self.render()
                j += 1

            j = 0
            while not self.free:
                self.q += self.stance_dyn()*.02

                if self.q[0] > 1:
                    self.free = 1

                    r, th, rd, thd, x0 = self.q

                    # th += np.random.uniform(-.1, .1)

                    x = -r*np.sin(th) + x0
                    z =  r*np.cos(th)

                    xd = -rd*np.sin(th) - r*np.cos(th)*thd
                    zd =  rd*np.cos(th) - r*np.sin(th)*thd

                    self.q = np.array([x, z, xd, zd])  # x, z, xd, zd

                if j % 5 == 0:
                    self.render()
                j += 1

    def create_gif(self, gif_filename):
        images = []
        for filename in os.listdir(self.image_folder):
            if filename.endswith(".png"):
                images.append(imageio.imread(os.path.join(self.image_folder, filename)))

        imageio.mimsave(gif_filename, images, loop=0)

        # Delete the image folder
        if os.path.exists(self.image_folder):
            import shutil
            shutil.rmtree(self.image_folder)

s = SLIP()
for j in range(6):

    s.c = ['r', 'g', 'b'][j%3]

    s.q = np.random.uniform([-2, 2, -5, -2], [2, 4, 5, 2])
    s.th = s.q[0] * .1

    # for _ in range(5):
    #     s.render()

    s.simulate(4)



s.create_gif("SLIP.gif")


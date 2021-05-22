from pylab import *
from natsort import natsorted
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import os
import sliceViewer
from mpl_toolkits.mplot3d import Axes3D

path = "slice_data/"
list_files = os.listdir(path)  # looking for files in current directory
list_files = natsorted(list_files)  # sort list of images in order of timestamp
img_list = []

for file in list_files:
    try:
        # read in image as numpy array
        pltImage = img.imread(path + file)
        imageArr = np.array(pltImage)
        # rotate image 180 degrees so orientation is correct in 3d space
        for _ in range(2):
            imageArr = np.rot90(imageArr)
        img_list.append(imageArr)
    except (IOError, SyntaxError) as e:
        print('Bad file:', file)

# print out spatial dimensions of the image (y, x, alpha(3/4))
# results: RGBA(4) image 480x640
print(img_list[0].shape)
plt.imshow(img_list[0])
plt.show()

# maximum projections in different directions
# maximum projection in y
max_y = np.max(pltImage, axis=1)

# maximum projection in x
max_x = np.max(pltImage, axis=2)

# plotting 2d image in 3d space
# for image in img_list:
#     x_scale, y_scale = ogrid[0:image.shape[0], 0:image.shape[1]]
#     fig = plt.figure()
#     ax = gca(projection='3d')
#     ax.plot_surface(y_scale, np.atleast_2d(2), x_scale, rstride=3, cstride=3, facecolors=image)
#     show()

fig = plt.figure()
ax = gca(projection='3d')
x_scale, y_scale = ogrid[0:img_list[60].shape[0], 0:img_list[60].shape[1]]
ax.plot_surface(y_scale, np.atleast_2d(2), x_scale, rstride=3, cstride=3, facecolors=img_list[60])
# elev = 15.0
# azim = 25.0
# ax.view_init(elev, azim)
plt.show()

# sliceViewer.multi_slice_viewer(img_list)
# plt.show()

# add MplCanvas to view3d QWidget
        # sc = MplCanvas(self, width=7, height=6)
        
        # path = "/home/amalik/Documents/listener/src/python/slice_data/"
        # list_files = os.listdir(path)
        # newImg = matImg.imread(path+"5.128.png")
        # imageArr = np.array(newImg) #self.img
        # # print(img.shape)
        # # rotate image 180 degrees so orientation is correct in 3d space
        # for _ in range(2):
        #     imageArr = np.rot90(imageArr)

        # x_scale, y_scale = ogrid[0:imageArr.shape[0], 0:imageArr.shape[1]]
        # sc.axes.plot_surface(y_scale, np.atleast_2d(2), x_scale, rstride=3, cstride=3, facecolors=imageArr)
        # surfaceLayout = QtWidgets.QVBoxLayout()
        # surfaceLayout.addWidget(sc)
        # self.ui.view3d.setLayout(surfaceLayout)


        self.angle = -0.3
        # for image in self.img_list:
        #     self.sc.update_plot(image, self.angle)
        #     if self.angle < 0.4:
        #         self.angle += 0.05
        #     else:
        #         self.angle -= 0.8
        # self.sc.update_plot(self.img_list[10], 0)
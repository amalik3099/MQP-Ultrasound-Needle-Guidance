#!/usr/bin/env python

import sys
import os.path
import matplotlib.pyplot as plt
import matplotlib.image as matImg
import argparse
import cv2
import serial
from pylab import *
from PIL import Image
from natsort import natsorted, ns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt, Slot, Signal, QThread
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide2.QtGui import QPen, QPixmap
import pylisten
import sliceViewer
from mainGUI import Ui_MainWindow
from threading import Event
from arduinoControl import ControlArduino

# global variable 
encoder_reading = 0.0
start = 0.0 
flag = 0
previous_time = 1e-10

# custom event for handling change in freeze state
class FreezeEvent(QtCore.QEvent):
    def __init__(self, frozen):
        super().__init__(QtCore.QEvent.User)
        self.frozen = frozen

# custom event for handling button presses
class ButtonEvent(QtCore.QEvent):
    def __init__(self, btn, clicks):
        super().__init__(QtCore.QEvent.Type(QtCore.QEvent.User + 1))
        self.btn = btn
        self.clicks = clicks

# custom event for handling new images
class ImageEvent(QtCore.QEvent):
    def __init__(self):
        super().__init__(QtCore.QEvent.Type(QtCore.QEvent.User + 2))

# manages custom events posted from callbacks, then relays as signals to the main widget
class Signaller(QtCore.QObject):
    freeze = QtCore.Signal(bool)
    button = QtCore.Signal(int, int)
    image = QtCore.Signal(QtGui.QImage)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.usimage = QtGui.QImage()

    def event(self, evt):
        if evt.type() == QtCore.QEvent.User:
            self.freeze.emit(evt.frozen)
        elif evt.type() == QtCore.QEvent.Type(QtCore.QEvent.User + 1):
            self.button.emit(evt.btn, evt.clicks)
        elif evt.type() == QtCore.QEvent.Type(QtCore.QEvent.User + 2):
            self.image.emit(self.usimage)
        return True

# global required for the listen api callbacks
signaller = Signaller()

# draws the ultrasound image
class ImageView(QtWidgets.QGraphicsView):
    def __init__(self, listen):
        QtWidgets.QGraphicsView.__init__(self)
        self.listen = listen
        self.setScene(QtWidgets.QGraphicsScene())

    # set the new image and redraw
    def updateImage(self, img):
        self.image = img
        self.scene().invalidate()

    # resize the scan converter, image, and scene
    def resizeEvent(self, evt):
        w = evt.size().width()
        h = evt.size().height()
        self.listen.setOutputSize(w, h)
        self.image = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32)
        self.image.fill(QtCore.Qt.black);
        self.setSceneRect(0, 0, w, h)

    # black background
    def drawBackground(self, painter, rect):
        painter.fillRect(rect, QtCore.Qt.black)

    # draws the image
    def drawForeground(self, painter, rect):
        if not self.image.isNull():
            painter.drawImage(rect, self.image)

#draws sliceViewer plots
class MplGraphics(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        QtWidgets.QGraphicsView.__init__(self, parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.figure.subplots()
        self.canvas.axes.index = 15 #should be 0
        self.canvas.axes.set_title('Ultrasound Slice Viewer')
        self.canvas.axes.set_xlabel('Image Number: 0')
        self.setLayout(vertical_layout)

    def setVol(self, volume):
        # sliceViewer.remove_keymap_conflicts({'j', 'k'})
        self.canvas.axes.volume = volume
        self.canvas.axes.imshow(volume[self.canvas.axes.index])
        self.canvas.draw()
        self.canvas.mpl_connect('key_press_event', self.process_key)

    def process_key(self, event):
        print('nuggets')
        ax = self.canvas.axes.volume[15]
        if event.key == 'j':
            sliceViewer.previous_slice(ax)
        elif event.key == 'k':
            sliceViewer.next_slice(ax)
        self.canvas.draw()

# Plots 3d surface plot
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=6, height=5):
        fig = Figure(figsize=(width,height))
        self.axes = fig.add_subplot(111, projection='3d')
        super(MplCanvas, self).__init__(fig)

    # def displaySet(self, list): 

class Mpl3DPlot(FigureCanvas):
    def __init__(self, init_image):
        # plt.ion()
        self.fig = Figure(figsize=(10,9))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim3d(0, 480) #650
        self.ax.set_ylim3d(-200, 200)
        self.ax.set_zlim3d(0, 410) #490
        self.ax.view_init(190, 45)
        self.rows = init_image.shape[0]
        self.cols = init_image.shape[1]
        self.mat = cv2.getRotationMatrix2D((100, 100), 0, 1)
        self.new_img = cv2.warpAffine(init_image, self.mat, (self.cols, self.rows))
        self.y_new, self.x_new = ogrid[0:self.new_img.shape[0], 0:self.new_img.shape[1]]
        self.y_diff = np.multiply(self.y_new, 0)
        self.surf_plot = self.ax.plot_surface(self.x_new, self.y_diff, self.y_new, rstride=10, cstride=10,
                                              facecolors=init_image)
        super(Mpl3DPlot, self).__init__(self.fig)
        # plt.draw()

    def update_plot(self, updated_image, deg_rot):
        self.surf_plot.remove()
        # plt.pause(5)
        # self.ax.cla()
        # self.ax.set_xlim3d(0, 480) #650
        # self.ax.set_ylim3d(-200, 200)
        # self.ax.set_zlim3d(0, 410) #490
        self.rows = updated_image.shape[0]
        self.cols = updated_image.shape[1]
        self.mat = cv2.getRotationMatrix2D((100, 100), deg_rot, 1)
        self.new_img = cv2.warpAffine(updated_image, self.mat, (self.cols, self.rows))
        self.y_new, self.x_new = ogrid[0:self.new_img.shape[0], 0:self.new_img.shape[1]]
        self.y_diff = np.multiply(self.y_new, deg_rot)
        self.surf_plot = self.ax.plot_surface(self.x_new, self.y_diff, self.y_new, rstride=35, cstride=35, facecolors=updated_image)
        # self.surf_plot = self.ax.plot_surface(self.x_new, self.y_diff, self.y_new, rstride=10, cstride=10)
        # facecolors=updated_image)
        # plt.draw()
        self.fig.canvas.draw()
        # self.fig.canvas.flush_events()
        plt.pause(0.01)       

class MainWindow(QMainWindow):
    def __init__(self, listen):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.listen = listen
        
        #Encoder Graphic and esp setup
        # pen = QPen(Qt.red)
        # pen.setWidth(3)
        # pen.setCapStyle(Qt.RoundCap)
        # scene = QtWidgets.QGraphicsScene()
        # pen.setCosmetic(True)
        # scene.addPixmap(QPixmap('back.png'))
        # self.item = scene.addLine(60, 170, 97, 97, pen)
        # pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.gray))
        # brush = QtGui.QBrush(pen.color().darker(100))
        # scene.addEllipse(87, 87, 20, 20, pen, brush)
        # self.item.setTransformOriginPoint(97, 97)
        # self.ui.graphicsView.setScene(scene)

        self.stop_flag_time = Event()
        self.stop_flag_RS232 = Event()

        self.getArduino = ControlArduino(self.stop_flag_RS232)
        self.getArduino.newValue.connect(self.updateEncoder)
        self.getArduino.testRS232.connect(self.updateInfoESP32)
        self.getArduino.start()
        #Encoder graphic and esp setup
        
        # self.ui.pushButton.clicked.connect(self.sliceMethod)
        self.addToolBar(NavigationToolbar(self.ui.MplGraphics.canvas, self))

        # setting placeholder text and mask for IP and Port in Live Viewer
        self.ui.ip.setPlaceholderText("192.168.1.1")
        self.ui.ip.setInputMask("000.000.000.000")
        self.ui.port.setPlaceholderText("58285")
        self.ui.port.setInputMask("00000")

        # setting placeholder text and mask for IP and Port in Slice Viewer
        self.ui.ip2.setPlaceholderText("192.168.1.1")
        self.ui.ip2.setInputMask("000.000.000.000")
        self.ui.port2.setPlaceholderText("58285")
        self.ui.port2.setInputMask("00000")

        # try to connect/disconnect to/from the probe
        def tryConnect():
            if not listen.isConnected():
                if listen.connect(self.ui.ip.text(), int(self.ui.port.text())):
                    self.statusBar().showMessage("Connected")
                    self.ui.connect.setText("Disconnect")
                else:
                    self.statusBar().showMessage("Failed to connect to {0}".format(self.ui.ip.text()))
                    self.ui.connect.setText("Retry")
            else:
                if listen.disconnect():
                    self.statusBar().showMessage("Disconnected")
                    self.ui.connect.setText("Connect")
                else:
                    self.statusBar().showMessage("Failed to disconnect")

        self.ui.connect.clicked.connect(tryConnect)
        self.ui.Quit.clicked.connect(self.shutdown)

        # add widgets to layout
        self.img = ImageView(listen)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.img)
        self.ui.liveStr.setLayout(layout)

        # images slices in 3d view with angle info
        self.path = "/home/amalik/Documents/listener/src/python/sample_img/"
        self.list_files = os.listdir(self.path)  # looking for files in current directory
        self.list_files = natsorted(self.list_files)  # sort list of images in order of timestamp
        self.img_list = []

        for file in self.list_files:
            try:
                # read in image as numpy array
                pltImage = matImg.imread(self.path + file)
                # Crop out 64 rows off the top of the image (remove top 13.33% of image)
                croppedImage = pltImage[64:, :]
                self.img_list.append(croppedImage)
            except (IOError, SyntaxError) as e:
                print('Bad file:', file)

        #add Mpl3DPlot to view3d QWidget
        plt.ion()
        self.sc = Mpl3DPlot(self.img_list[0])
        surfaceLayout = QtWidgets.QVBoxLayout()
        surfaceLayout.addWidget(self.sc)
        self.ui.view3d.setLayout(surfaceLayout)

        # connect signals
        signaller.freeze.connect(self.freeze)
        signaller.button.connect(self.button)
        signaller.image.connect(self.image)

        # get home path
        path = os.path.expanduser("~/")
        if  listen.init(path, 640, 480):
            self.statusBar().showMessage("Initialized")
        else:
            self.statusBar().showMessage("Failed to initialize")
    
    # Slots to update encoder readings and esp32 info
    @Slot()
    def on_btnExit_clicked(self):
        self.stop_flag_time.set()
        self.stop_flag_RS232.set()
        sys.exit(0);

    def updateEncoder(self, poti, potiRotation):
        # self.item.setRotation(potiRotation)
        int_reading = int(poti)
        # int_reading = int_reading*2
        global encoder_reading
        if int_reading >= 0:
            encoder_reading = (int_reading/50)*-1
        else:
            # int_reading = int_reading-360
            encoder_reading = (int_reading/50)*-1
        # else:
        #     encoder_reading = 0     (150)
        self.ui.lcdNumber.display(str(int_reading))

    def updateInfoESP32(self, rs232):
        print(rs232)
        if rs232:
            print("Board is connected")
        else:
            print("Board is not connected")
            self.ui.lcdNumber.display(0)
            self.stop_flag_RS232.set()
    
    # handles freeze messages
    @Slot(bool)
    def freeze(self, frozen):
        if frozen:
            self.statusBar().showMessage("Image Stopped")
        else:
            self.statusBar().showMessage("Image Running")

    # handles button messages
    @Slot(int, int)
    def button(self, btn, clicks):
        self.statusBar().showMessage("Button {0} pressed w/ {1} clicks".format(btn, clicks))

    # handles new images
    @Slot(QtGui.QImage)
    def image(self, img):
        self.img.updateImage(img)
        img_arr = QImageToNumpyArray(img)
        img_arr = img_arr / 255
        # shape: (401, 471, 4)
        croppedImage = img_arr[70:, :]
        self.sc.update_plot(croppedImage, encoder_reading)
        # image type: QtGui.QImage

    # handles shutdown
    @Slot()
    def shutdown(self):
        self.listen.destroy()
        QtWidgets.QApplication.quit()
        
    # def sliceMethod(self):

    #     path = "/home/amalik/Documents/listener/src/python/slice_data/"

    #     list_files = os.listdir(path)  # looking for files in current directory
    #     list_files = natsorted(list_files) #sort list of images in order of timestamp

    #     img_list = []

    #     for filename in list_files:
    #         if filename.endswith('.png'):
    #             try:
    #                 # img.verify()  # verify that it is, in fact an image
    #                 img = matImg.imread(path + filename)
    #                 img_list.append(img)
    #             except (IOError, SyntaxError) as e:
    #                 print('Bad file:', filename)
    #                 os.remove(path+filename)

    #     self.ui.MplGraphics.setVol(img_list) #run images with sliceviewer
    #     plt.show()

        # self.ui.MplWidget.canvas.axes.clear()
        # self.ui.MplWidget.canvas.axes.set_title('Fried Chicken')
        # self.ui.MplWidget.canvas.draw()


def QImageToNumpyArray(incoming_img):
    # print(incoming_img.format())
    incoming_img = incoming_img.convertToFormat(QtGui.QImage.Format.Format_ARGB32)
    width = incoming_img.width()
    height = incoming_img.height()
    ptr = incoming_img.constBits()
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr


## called when a new processed image is streamed
# @param image the scan-converted image data
# @param width width of the image in pixels
# @param height height of the image in pixels
# @param bpp bits per pixel
# @param micronsPerPixel microns per pixel
# @param timestamp the image timestamp in nanoseconds
def newProcessedImage(image, width, height, bpp, micronsPerPixel, timestamp, imu):
    img = QtGui.QImage(image, width, height, QtGui.QImage.Format_ARGB32)
    # a deep copy is important here, as the memory from 'image' won't be valid after the event posting
    signaller.usimage = img.copy()
    evt = ImageEvent()
    QtCore.QCoreApplication.postEvent(signaller, evt)

    # uncomment to collect data v
    global start
    global positional_data
    global previous_time
    # global encoder_reading
     
    if(start == 0.0):
        start = np.round_((timestamp/1e+9), decimals = 3)

    # img = Image.frombytes('L', (width, height), image)
    if bpp == 32:
        img = Image.frombytes('RGBA', (width, height), image)
    else:
        img = Image.frombytes('L', (width, height), image)

    time_frame = abs(np.round_((timestamp/1e+9 - start), decimals = 3))
    path_img = "/home/amalik/Documents/listener/src/python/slice_data/" + f"{time_frame}{encoder_reading}.png"
    img.save(path_img)
    # uncomment to collect data ^
    return


## called when a new raw image is streamed
# @param image the raw pre scan-converted image data, uncompressed 8-bit or jpeg compressed
# @param lines number of lines in the data
# @param samples number of samples in the data
# @param bps bits per sample
# @param axial microns per sample
# @param lateral microns per line
# @param timestamp the image timestamp in nanoseconds
# @param jpg jpeg compression size if the data is in jpeg format
def newRawImage(image, lines, samples, bps, axial, lateral, timestamp, jpg):
    return


# Called when new processed image is streamed. Saves individual images with time frame
# def newProcessedSlice(image, width, height, bpp, micronsPerPixel, timestamp, imu):
#     print("new image (sc): {0}, {1}x{2} @ {3} bpp, {4:.2f} um/px, imu: {5} pts".format(timestamp, width, height, bpp, micronsPerPixel, len(imu)))
#     global start
#     global positional_data
#     global previous_time
     
#     if(start == 0.0):
#         start = np.round_((timestamp/1e+9), decimals = 3)

#     # img = Image.frombytes('L', (width, height), image)
#     if bpp == 32:
#         img = Image.frombytes('RGBA', (width, height), image)
#     else:
#         img = Image.frombytes('L', (width, height), image)

#     time_frame = abs(np.round_((timestamp/1e+9 - start), decimals = 3))
    
#     # /********************************************
#     # for raw imu data:
#     imu_data = imu_data_processing(imu, len(imu))
#     write_to_csv(imu_data,time_frame,previous_time)
    
#     # ********************************************/
#     previous_time = time_frame
#     # /********************************************
#     # for positional data:
#     # position_data = positional_data_processing(imu_data)
#     # write_to_csv(position_data,time_frame)
#     # ********************************************/
    
#     path_img = "/home/amalik/Documents/listener/src/python/slice_data/" + f"{time_frame}.png"
#     img.save(path_img)
#     return


# ## called when a new raw image is streamed
# # @param image the raw pre scan-converted image data, uncompressed 8-bit or jpeg compressed
# # @param lines number of lines in the data
# # @param samples number of samples in the data
# # @param bps bits per sample
# # @param axial microns per sample
# # @param lateral microns per line
# # @param timestamp the image timestamp in nanoseconds
# # @param jpg jpeg compression size if the data is in jpeg format
# def newRawSlice(image, lines, samples, bps, axial, lateral, timestamp, jpg):
#     print("new image (ps): {0}, {1}x{2} @ {3} bps, {4:.2f} um/s, {5:.2f} um/l".format(timestamp, lines, samples, bps, axial, lateral))
#     if jpg == 0:
#         img = Image.frombytes('L', (samples, lines), image, "raw")
#     else:
#         # note! this probably won't work unless a proper decoder is written
#         img = Image.frombytes('L', (samples, lines), image, "jpg")
#     img.save("raw_image.jpg")
#     return


## called when freeze state changes
# @param frozen the freeze state
def freezeFn(frozen):
    evt = FreezeEvent(frozen)
    QtCore.QCoreApplication.postEvent(signaller, evt)
    return


## called when a button is pressed
# @param button the button that was pressed
# @param clicks number of clicks performed
def buttonsFn(button, clicks):
    evt = ButtonEvent(button, clicks)
    QtCore.QCoreApplication.postEvent(signaller, evt)
    return


def main():
    path = os.path.expanduser("~/")
    listen = pylisten.Listener(newProcessedImage, newRawImage, freezeFn, buttonsFn)
    # listenSlice = pylisten.Listener(newProcessedSlice, newRawSlice, freezeFn, buttonsFn)
    app = QApplication(sys.argv)
    window = MainWindow(listen)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


# to convert ui to py file 
    # pyside2-uic -x /home/amalik/Documents/listener/src/python/mainGUI.ui -o mainGUI.py

# Edit needed when update mainGUI.py
    # from clariusGUI import MplGraphics

# Clarius network password:
    # xdOmUnr0

# self.ui.pushButton.clicked.connect(self.clickedMethod)

# def sliceMethod(self):
#         print('Clicked Push Button')
#         os.system('python sliceViewer.py')
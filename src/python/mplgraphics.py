# from PySide2.QtWidgets import *
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# import sliceViewer

# class MplGraphics(QGraphicsView):
#     def __init__(self, parent=None):
#         QGraphicsView.__init__(self, parent)

#         self.figure = Figure()
#         self.canvas = FigureCanvas(self.figure)

#         vertical_layout = QVBoxLayout()
#         vertical_layout.addWidget(self.canvas)

#         self.canvas.axes = self.figure.subplots()
#         self.canvas.axes.index = 0
#         self.canvas.axes.set_title('Ultrasound Slice Viewer')
#         self.canvas.axes.set_xlabel('Image Number: 0')
#         self.setLayout(vertical_layout)


#     def setVol(self, volume):
#         sliceViewer.remove_keymap_conflicts({'j', 'k'})
#         self.canvas.axes.volume = volume
#         self.canvas.axes.imshow(volume[self.canvas.axes.index])
#         self.canvas.draw()
#         self.canvas.mpl_connect('key_press_event', self.process_key)
#         print('khalas')


#     def process_key(event):
#         print('nuggets')
#         # ax = self.canvas.axes.volume[15]
#         # if event.key == 'j':
#         #     sliceViewer.previous_slice(ax)
#         # elif event.key == 'k':
#         #     sliceViewer.next_slice(ax)
#         # self.canvas.draw()
        
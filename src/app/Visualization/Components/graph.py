from collections import deque
import math
import os
import threading
from PyQt5.QtWidgets import QGraphicsPixmapItem, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from PIL import Image
from PIL import ImageQt

# Creates parent widget, pyqtgraph child widget, and data structures needed for visualizing the live sensor data. Includes class methods for adding coordinates to the respective deques and animating the resulting curve on the graph 
class Graph(QWidget):
    def __init__(self, settings):
        super().__init__()

        self.brush_flag = 0
        self.sensor_type = None
        # Define the length of the queue
        self.queue_length = settings["queue_length"]
        self.multi_sensor = settings["multi_sensor"]
        # Create a deque for x and y values
        self.x_queue = deque(maxlen=self.queue_length)
        self.y_queue = deque(maxlen=self.queue_length)

        # Lock for accessing the above deques
        self.lock = threading.Lock()

        # Domain and range of graph
        self.min_x = settings["min_x"]
        self.max_x = settings["max_x"]
        self.min_y = settings["min_y"]
        self.max_y = settings["max_y"]

        self.span_x = abs(self.min_x)+abs(self.max_x)
        self.span_y = abs(self.min_y)+abs(self.max_y)
        self.denominator = math.gcd(self.span_x, self.span_y)

        # Create PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setRange(xRange=[self.min_x, self.max_x], yRange=[self.min_y, self.max_y])
        self.plot_widget.setLabel('bottom', "X (cm)")
        self.plot_widget.setLabel('left', "Y (cm)")
        self.plot_widget.setTitle(f"<span style=\"color:black;font-size:35px;font-weight:bold;\">{settings['graph_title']}</span>")
        for axis in ['top', 'bottom', 'left', 'right']:
            self.plot_widget.getAxis(axis).setPen(pg.mkPen(color='#FFCE00', width=3))

        # Load image from file
        map_path = settings["map_path"]
        if os.path.exists(map_path):
            image = Image.open(map_path)
            # Flip the image vertically (Qpixmap scanner reads y-axis of most bitmap formats such as jgp, bmp, png, tif, etc in reverse)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            # Create QPixmap from the flipped image
            pixmap = QPixmap.fromImage(ImageQt.ImageQt(image))
            # Scale the image to fit plot
            scaled_pixmap = pixmap.scaled(self.span_x, self.span_y, aspectRatioMode=Qt.IgnoreAspectRatio)
            # Convert loaded image to supported format
            image_item = QGraphicsPixmapItem(scaled_pixmap)
            # Add the item to plot background
            self.plot_widget.addItem(image_item)
            image_item.setPos(self.min_x, self.min_y)

        # Create artist object for adding select points to plot
        self.line = pg.PlotDataItem()
        self.plot_widget.addItem(self.line)

        # If multiple sensors selected via config.json, then add multi_sensor required items
        # TODO: In the future could be useful to not hard code these
        if self.multi_sensor:
            self.imux_queue = deque(maxlen=self.queue_length)
            self.imuy_queue = deque(maxlen=self.queue_length)
            self.line2 = pg.PlotDataItem()
            self.plot_widget.addItem(self.line2)

        # Define line & marker settings
        self.lineStyle = 'b'
        if settings["show_line"] is False:
            self.lineStyle = None
        self.markerStyle = 'o'
        if settings["show_marker"] is False:
            self.markerStyle = None

        # Set domain and range of graph
        self.plot_widget.setXRange(self.min_x, self.max_x)
        self.plot_widget.setYRange(self.min_y, self.max_y)

        # Add PlotWidget to layout
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Background color
        self.plot_widget.setBackground('white')

    # Append coordinate values to the corresponding deques
    def add_point(self, x, y, sensor_type:str):
        #with self.lock:
        if self.multi_sensor:
            if self.sensor_type != sensor_type:
                self.sensor_type = sensor_type

            if self.sensor_type == 'GoDirect':
                self.x_queue.append(x)
                self.y_queue.append(y)
            elif self.sensor_type == 'IMU':
                self.imux_queue.append(x)
                self.imuy_queue.append(y)
        else:
            self.x_queue.append(x)
            self.y_queue.append(y)
            

    # Repeatedly called to animate the curve produced by the coordinate values stored in the deques
    def update_line(self):

        # Initializing values queues depending on usage of multiple sensors
        #with self.lock:
        x_values = self.x_queue
        y_values = self.y_queue
        if self.multi_sensor:
            imux_values = self.imux_queue
            imuy_values = self.imuy_queue

	
        # Distributing points by class if using multiple sensors
        if self.multi_sensor:
            if self.sensor_type == 'GoDirect':
                self.line.setData(x_values, y_values, pen=self.lineStyle, symbol=self.markerStyle)
            elif self.sensor_type == 'IMU':
                self.line2.setData(imux_values, imuy_values, pen='r', symbol='+', symbolBrush='r')

        # Otherwise just use setData
        else:
            self.line.setData(x_values, y_values, pen=self.lineStyle, symbol=self.markerStyle)
        
        # if len(x_values)%13 == 0:
        #     self.line.setData([50], [50], pen=self.lineStyle, symbol='x')
        

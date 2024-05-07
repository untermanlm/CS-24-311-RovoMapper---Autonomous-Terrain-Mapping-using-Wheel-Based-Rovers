# The Sensor class of sensors.py holds state information and callback functions required to initialize a

from ctypes import c_void_p
from timeit import default_timer as timer
from time import sleep, time
from threading import Event
import json
from gdx import gdx
import math
import numpy as np

class Sensor:
    def __init__(self, device, cond, message, name:str, msg_handler, logger, speed:int):
        self.device = device
        self.callback = (self.data_handler)
        self.processor = None
        self.cond = cond
        self.message = message
        self.name = name
        self.msg_handler = msg_handler
        self.logger = logger
        self.speed = speed
        self.closed = False

    # Callback function that is executed for each packet of data that is produced
    def data_handler(self, data):
        # Time when each thread enters with new data
        # Get lock for data store, faster thread gets it - other thread forced to wait
        self.cond.acquire()

        #This is the data packet that is pushed to the moquito server with the values in the array from the calculations
        #for reading in values:
        t1 = time()
        self.message.update_sensor_data(self.name, data, t1)
        
        #Do we even need this anymore?
        # #If flag == 0 then this thread was the first to acquire lock
        if self.message.flag == 0:
            self.message.flag = 1
            self.message.payload['unix_timestamp'] = time()
            # Wake up 2nd thread and sleep until 2nd thread is finished
            self.cond.wait()
            self.cond.release()
        elif self.message.flag == 1:
            # Only 2nd thread can enter here
            self.message.flag = 0
            # Send paired data to msg broker
            self.msg_handler.publish(json.dumps(self.message.payload))
            # Check if there was a reset flag set
            if self.message.payload['reset'] == True:
                self.message.payload['reset'] = False
            # Wake up 1st thread and exit function
            self.cond.notifyAll()
            self.cond.release()
        
    #Setup the sensor with the specfic sensor we are looking for and the speed
    def setup(self):
        e = Event()

        # processor callback fn
        def processor_created(context, pointer):
            self.processor = pointer
            e.set()

        self.device.enable_sensors([5,6])
        # self.device.sensors[6].enabled = True
        self.device.start(self.speed) 

    #Initializes data stream
    def start(self):
        #An infinite loop for collecting data   
        #start = time()
        while self.closed is False:
            try:
                #Read now
                self.device.read()
                #end = time()
                #elapsed = end - start
                #start = end
                measurement = np.array(self.device.sensors[5].values)
                
                self.device.sensors[5].values.clear()

                diff = np.diff(measurement)
                elapsed = (self.speed) / 1000.0
                rps = diff / elapsed
                dps = rps * (180.0 / math.pi)

                for dp in dps:
                    value = dp#int(dp)
                    if self.name == 'LSensor':
                        self.callback(-1*value)
                    elif self.name == 'RSensor':
                        self.callback(value)
            except Exception:
                break
            

    def shutdown(self, event):
        self.logger.debug("Sensor debug disconnect")
        self.logger.debug("Disconnected")
        self.closed = True
        event.set()
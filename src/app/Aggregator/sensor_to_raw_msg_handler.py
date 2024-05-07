# Process that handles initializing connections to two GoDirect wireless rotary encoder sensors and a message broker. It starts 
# the data streams for the sensors and handles publishing to the Data/raw topic.

import app.lib.message_handler as message_handler
import app.lib.messages as messages
import app.Aggregator.sensors as sensors
from multiprocessing import Process
from timeit import default_timer as timer
from time import sleep
from sys import exit
from threading import Condition, Event, Thread
import logging, signal, json
from gdx import gdx

class SensorProcess(Process):
    def __init__(self, client_id:str, topic_sub:str, topic_pub:str, l_mac:str, r_mac:str, queue):
        Process.__init__(self)
        self.client_id = client_id
        self.topic_sub = topic_sub
        self.topic_pub = topic_pub
        self.l_mac = l_mac
        self.r_mac = r_mac
        self.queue = queue
        self.logger = logging.getLogger('app')
        self.godirect = None
        self.threads = []
        
    def run(self):
        try:
            # Setup interrupt signal handler
            signal.signal(signal.SIGTERM, self.interrupt_handler)
            
            self.logger.debug('Process Started')
            self.logger.info('Setting up Sensors...')
            
            sensor_type = 'GoDirect'
            self.cond = Condition()
            self.sensor_list = []
            self.message = messages.Message(self.l_mac, self.r_mac, sensor_type)
            
            # Create msg handler
            self.handler = message_handler.Handler(self.client_id, self.topic_sub, self.topic_pub)
            self.handler.client.message_callback_add(self.topic_sub, self.on_message)

            # Creating actual godirect object
            godirect = gdx.gdx()
            self.godirect = godirect

            # Opening left and right sensors
            try:
                godirect.open(connection='ble', device_to_open=f'{self.l_mac}, {self.r_mac}')
            except RuntimeError:
                print("Make sure sensors are close to RPI first and the BLE LED is blinking red.\nPress Ctrl-C to shutdown.")
                self.shutdown()
                exit(0)
            
            left_sensor = godirect.devices[0]
            right_sensor = godirect.devices[1]
            sensor_speed = 25  # Ms

            # Making each GoDirect sensor a Sensor object from sensors.py
            self.l_sensor = sensors.Sensor(left_sensor, self.cond, self.message, 'LSensor', self.handler, self.logger, sensor_speed)
            self.r_sensor = sensors.Sensor(right_sensor, self.cond, self.message, 'RSensor', self.handler, self.logger, sensor_speed)

            #If Successfully connected 
            self.logger.info("Connected to both sensors!")
            self.sensor_list.append(self.l_sensor)
            self.sensor_list.append(self.r_sensor)       

            # Setup sensors
            for s in self.sensor_list:
                s.setup()

            # Start polling and publishing
            self.handler.connect()
            self.message.payload['start_time'] = timer()

            # Tell parent process that setup is done and sensors are polling
            self.queue.put_nowait(True)

            #Make Threads
            for s in self.sensor_list:
                t = Thread(target = s.start)
                self.threads.append(t)

            #Tell each thread to start collecting data
            for t in self.threads:
                t.start()
            self.logger.info("DATA COLLECTION IN PROGRESS")
            
            #Start event loop for publishing data 
            self.handler.loop()
            
        except Exception as e:
            self.logger.error(e, exc_info=True)
            
    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        if data["reset"] == True:
            self.cond.acquire()
            self.message.payload['reset'] = True
            self.message.payload['start_time'] = timer()
            self.cond.release()
        
    def interrupt_handler(self, signum, frame):
        self.logger.debug(f'Handling signal {signum} ({signal.Signals(signum).name}).')
        self.handler.client.disconnect()
        self.shutdown()
        self.logger.debug('Process Ended')
        sleep(1)
        self.godirect.stop()
        self.godirect.close()
        exit(0)
        
    def shutdown(self):
        # Get lock
        self.cond.acquire()
        
        # Reset Sensors
        events = []
        for s in self.sensor_list:
            e = Event()
            events.append(e)
            self.logger.debug('Resetting board: %s', s.name)
            s.shutdown(e)

        # Ensure that all threads have finished with shutdown procedure before Main thread continues.
        for e in events:
            e.wait()

        self.cond.release()
    

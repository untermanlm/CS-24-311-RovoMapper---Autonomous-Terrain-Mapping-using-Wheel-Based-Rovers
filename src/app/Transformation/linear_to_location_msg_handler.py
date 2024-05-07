# Background process that handles subscribing to the linearData topic, passing data to an instance of 
# linear_to_location.Tracking class and then publishing to the locationData topic.

from sys import exit
from multiprocessing import Process
import app.lib.message_handler as message_handler
import app.Transformation.linear_to_location as linear_to_location
import json, logging, time, signal


class LinearProcess(Process):
    def __init__(self, client_id, topic_sub, topic_pub, axle_length, filter_version):
        Process.__init__(self)
        self.client_id = client_id
        self.topic_sub = topic_sub
        self.topic_pub = topic_pub
        self.axle_length = axle_length
        self.filter_version = filter_version
        self.logger = logging.getLogger('app')

    def run(self):
        try:
            # Setup interrupt signal handler
            signal.signal(signal.SIGTERM, self.interrupt_handler)
            
            self.logger.debug('Process Started')
        
            # Create transformer and msg handler 
            self.data_transformer = linear_to_location.Tracking(self.axle_length, self.filter_version)
            self.handler = message_handler.Handler(self.client_id, self.topic_sub, self.topic_pub)
            self.handler.client.message_callback_add(self.topic_sub, self.on_message)
        
            # Start event loop
            self.handler.connect()
            self.handler.loop()
        
        except Exception as e:
            self.logger.error(e, exc_info=True)
        
    def interrupt_handler(self, signum, frame):
        self.logger.debug(f'Handling signal {signum} ({signal.Signals(signum).name}).')
        self.handler.client.disconnect()
        self.logger.debug('Process Ended')
        time.sleep(1)
        exit(0)
        
    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        err = self.data_transformer.track(data)
        if err != 0:
            self.logger.error('linear_to_location.track returned with errno: ' + err)
        self.handler.publish(json.dumps(data))
        
    
The scripts and programs in the Aggregator folder handle configuring and initializing platform independent senors.  

They also handle collecting and pairing of the specific real time streaming sensor data as per the the requirements of the Transformation layer API.  
This paired data is then sent to a Message Broker for consumption by the Transformation layer.  

The Transformation Layer is responsible for transforming raw sensor data into linear distance traveled for each wheel. As the sensors and methodologies used to get this data may change, the API contract between the Aggregator and the Transformation Layer may be need to be updated.  

**Of most importance for the Aggregator Layer, is that regardless of methodology used, all the data from multiple sensors is accurately collected, paired and transmitted, for each epoch that is was collected.**

-----  

**The current Transformation API contract is as follows:**

- The API to the Transformation layer expects input in the form of a single JSON string:  
```
{
   "Start_time": float,
   "count": int,
   "sensor_type": str,
   "LW_Dis": float,
   "RW_Dis": float,
   "UTC": ?,
   "X": float,
   "Y": float,
   "LSensor": {
       "degPerSec": float,
       "timestamp": float,
       "mac": str
   }, 
   "RSensor": {
       "degPerSec": float,
       "timestamp": float,
       "mac": str
   }
 }
```
-----
* `sensor_to_raw_msg_handler.py`: Initialized by `initialize.py`, uses GDX library to open GoDirect sensors, spawns two Sensor processes (left and right) to initialize data collection period.

* `sensors.py`: Initialized by `sensor_to_raw_msg_handler.py`, infinitely collects data from GoDirect sensors until SIGINT received. Each sensor publishes message contents to MQTT message handler, natively synchronized. 

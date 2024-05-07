# messages.py's Message class is to be used by processes that are responsible for collecting raw sensor data.
# 
# The initial Message.payload dictionary structure defined here is serialized and deserialized
# as it is passed through the various layers of the application. 
# Layers may add key value pairs, but they should not remove any keys. As other layers may require them and 
# enables better logging of results.    

class Message():
    """
    Represents the state of a single paired data reading from a cohort of senors as well as various transformations
    to that data to turn it into location data.  
    """
    def __init__(self, l_mac:str, r_mac:str, sensor_type:str):
        self.flag = 0
        self.count = 0
        self.payload = {
            "start_time": 0.0,
            "count": 0,
            "sensor_type": sensor_type,
            "LW_dis": 0,
            "RW_dis": 0,
            "LW_total": 0,
            "RW_total": 0,
            "unix_timestamp": 0.0,
            "x_loc": 0,
            "y_loc": 0,
            "heading": 0.0,

            # Changing LSensor since new Sensors only have degPerSec data
            "LSensor": {
                "degPerSec": 0,
                "timestamp": 0.0,
                "mac": l_mac
            },
            # Changing RSensor since new Sensors only have degPerSec data
            "RSensor": {
                "degPerSec": 0,
                "timestamp": 0.0,
                "mac": r_mac
            },
            "reset": False
        }
        
    def update(self, key:str, value):
        self.payload[key] = value
        
    # Changing update data
    def update_sensor_data(self, sensor:str, data:int, timestamp:float):
        "Updates the specified sensor dictionary with live data"
        self.payload[sensor]["degPerSec"] = data
        self.payload[sensor]["timestamp"] = timestamp
        self.payload["count"] = self.count
        self.count += 1

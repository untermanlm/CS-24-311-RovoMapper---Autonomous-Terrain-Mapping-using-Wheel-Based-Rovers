from godirect import GoDirect
from time import sleep

godirect = GoDirect()
device = godirect.get_device()

if device != None and device.open(auto_start=True):
    sensors = device.get_enabled_sensors()
    while True:
        try:
            if device.read():
                for sensor in sensors:
                    print(sensor.value)
        except KeyboardInterrupt:
            break

    device.stop()
    device.close()
godirect.quit()
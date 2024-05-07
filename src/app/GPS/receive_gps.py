import socket
import json


write_name = '/home/server/Git-CS-24-311-RovoMapper/CS-24-311-RovoMapper---Autonomous-Terrain-Mapping-using-Wheel-Based-Rovers/src/app/GPS/gps_log_3.log'
gps_logs = {
    "header": [],
    "utc": [],
    "pos_status": [],
    "lat": [],
    "lat_dir": [],
    "lon": [],
    "lon_dir": [],
    "speed_kn": [],
    "track_true": [],
    "date": [],
    "mag_var": [],
    "var_dir": [],
    "check_sum": []
}

def read_GPRMC(data):
    cleaned_data = data.decode('utf-8')
    temp_arr = cleaned_data.split(',')
    gprmc_keys = gps_logs.keys()
    for i, (key, ele) in enumerate(zip(gprmc_keys, temp_arr)):
        if i == len(gprmc_keys) - 2:
            split = ele.split('*')
            var_dir = split[0]
            check_sum = split[1].strip('\r\n')
            gps_logs["var_dir"].append(var_dir)
            gps_logs["check_sum"].append(check_sum)
            break
        gps_logs[key].append(ele)

def convert_lat_lon(lat, lat_dir, lon, lon_dir):
    latitude = float(lat[:2]) + float(lat[2:]) / 60.0
    if lat_dir == 'S':
        latitude = -latitude
    longitude = float(lon[:3]) + float(lon[3:]) / 60.0
    if lon_dir == 'W':
        longitude = -longitude
    return latitude, longitude

def connect_to_server(ip, port, write_to = write_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((ip, port))
            print(f"Connected to {ip}:{port}")

            # Example of receiving data
            i = 0
            while True:
                data = client_socket.recv(1024)
                if not data:
                    with open(write_to, 'w') as file:
                        json.dump(gps_logs, file)
                    print(f"Writing to file: {write_to}")
                    break  # Connection closed
                read_GPRMC(data)
                print(f"Received: {data.decode('utf-8')}")
                latitude, longitude = convert_lat_lon(gps_logs["lat"][i], 
                                                        gps_logs["lat_dir"][i],
                                                        gps_logs["lon"][i],
                                                        gps_logs["lon_dir"][i]
                )
                print(f"Latitude: {latitude}, Longitude: {longitude}")
                i += 1

        except Exception as e:
            print(f"Failed to connect or error during communication: {e}")

if __name__ == "__main__":
    HOST_IP = '172.20.10.1'
    PORT = 11123
    connect_to_server(HOST_IP, PORT)

import json
import numpy as np
import os
import matplotlib.pyplot as plt


class LogReader:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.log_list = []
        self.ignored = []

        with open(file_name, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if i == 0:
                    continue
                try:
                    log_dict = json.loads(line)
                    self.log_list.append(log_dict)
                except json.decoder.JSONDecodeError:
                    self.ignored.append(i)
        
    def get_value_list(self, key_list: list[str], is_xy: bool = False):
        temp_dict = {}
        for key in key_list:
            temp_dict[key] = []

        if is_xy:
            breakpoints = []

        for i, log in enumerate(self.log_list):
            for key in key_list:
                if is_xy and key == 'reset':
                    if log[key]:
                        breakpoints.append(i)
                if key in log:
                    temp_dict[key].append(log[key])
            
        value_list = []
        for key in temp_dict.keys():
            value_list.append(temp_dict[key])

        # if is_xy:

        #     for vl, b in zip(value_list, breakpoints):
        #         split_point = self.__split(vl, b)
        #         split_lines = []
        #         split_lines.append(split_point[0])
        #         split_lines.append(split_poiq nt[1])
                          
        return value_list


    
# TODO
def break_list(lst, breakpoints):
    new_breakpoints = [0] + breakpoints + [len(lst)]
    newlist = []
    for i in range(len(breakpoints) - 1):
        split = lst[new_breakpoints[i]:new_breakpoints[i+1]]
        newlist.append(split)
    return newlist
    #return [lst[new_breakpoints[i]:new_breakpoints[i+1]] for i in range(len(new_breakpoints - 1))]          

def convert_lat_lon(lat, lat_dir, lon, lon_dir):
    latitude = float(lat[:2]) + float(lat[2:]) / 60.0
    if lat_dir == 'S':
        latitude = -latitude
    longitude = float(lon[:3]) + float(lon[3:]) / 60.0
    if lon_dir == 'W':
        longitude = -longitude
    return latitude, longitude

def read_gps_log(filename: str, write_name: str = 'output.csv'):
    with open(filename, 'r') as file:
        data = file.read()
        gps_dict = json.loads(data)

    clean_gps = [convert_lat_lon(lat, lat_dir, lon, lon_dir) for lat, lat_dir, lon, lon_dir in zip(gps_dict['lat'], gps_dict['lat_dir'], gps_dict['lon'], gps_dict['lon_dir'])]
    with open(write_name, 'w') as file:
        for tup in clean_gps:
            lat = tup[0]
            lon = tup[1]
            file.write(f'{lat}, {lon}\n')


def rotate(x, y, theta=np.pi / 4): 
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    points = np.array([[x_val, y_val] for x_val, y_val in zip(x, y)])
    rotated_points = np.dot(points, rotation_matrix)
    rotated_x = rotated_points[:, 0]
    rotated_y = rotated_points[:, 1]
    return rotated_x, rotated_y

def horizontal_flip(x):
    mean = np.mean(x)
    new_x = []
    for xval in x:
        flipped = 2 * mean - xval
        new_x.append(flipped)
    return np.array(new_x)


def main():
    filename = "courtyard_live_demo.log"

    keys = ["x_loc", "y_loc", "reset"]
    lr = LogReader(filename)

    # Need starting lat, lon values to build a proposed list of coordinate values solely from GoDirect output
    starting_lat, starting_lon = 37.54464612886165, -77.44830922741475

    values = lr.get_value_list(key_list=keys, is_xy=True)
    x = np.array(values[0]) / 10
    y = np.array(values[1]) / 10
    x_half = (np.array(x) / 100000)
    y_half = (np.array(y) / 100000)

    # plt.scatter(rotated_x, rotated_y)
    # plt.show()

    r_earth = 6378.137 # radius of the earth in km

    # Forming new_latitude, new_longitude values from x, y values
    new_latitude = starting_lat + (x_half / r_earth) * (180 / np.pi)
    new_longitude = starting_lon + (y_half / r_earth) * (180 / np.pi) / np.cos(starting_lat * np.pi / 180)
    
    print(new_latitude)
    print(new_longitude)
    outfile = 'gps_projected_original.csv'
    if not os.path.exists(outfile):
        with open(outfile, 'w') as file:
            for lat, lon in zip(new_latitude, new_longitude):
                file.write(f"{lat}, {lon}\n")
    



if __name__ == '__main__':
    main()
        

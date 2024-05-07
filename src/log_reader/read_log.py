import json
import numpy as np
import matplotlib.pyplot as plt


class LogReader:
    """
    LogReader class: utility to easily retrieve feature information from .log files
    generated by the system:
    Input: file_name: str - file name of the .log file you want to read.
    Output: None
    """
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
        """
        Input: key_list: list[str] - list of keys desired to retrieve from .log file
            * Optional: is_xy: bool - ignore, used to retrieve list of values associated with keys, 
                                      but split up by each time "RESET" button is pressed.
        Output: value_list: list[list[str]] - list of all values associated with each of the keys
        """
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
    """
    Ignore, WIP function with intended purpose of breaking column into smaller lists 
    for each of the "RESET" button usages.
    """
    new_breakpoints = [0] + breakpoints + [len(lst)]
    newlist = []
    for i in range(len(breakpoints) - 1):
        split = lst[new_breakpoints[i]:new_breakpoints[i+1]]
        newlist.append(split)
    return newlist
    #return [lst[new_breakpoints[i]:new_breakpoints[i+1]] for i in range(len(new_breakpoints - 1))]          


def main():
    filename = "gps_comparison_test.log" 

    keys = ["x_loc", "y_loc", "reset"]
    lr = LogReader(filename)

    values = lr.get_value_list(key_list=keys, is_xy=True)


    x = np.array(values[0]) / 10
    y = np.array(values[1]) / 10
    x_half = x[round(len(x)/ 2):]
    y_half = y[round(len(y)/ 2):]
    plt.scatter(x_half, y_half)
    plt.show()
    


if __name__ == '__main__':
    main()
        

# *RovoMapper - Autonomous Terrain Mapping using Wheel-Based Rovers*
## *Tamer Nadeem - University Affiliate*
## *Project Description*
In many crucial situations, such as mining operations, rescue missions in disaster-stricken areas, or exploration of hazardous environments, obtaining an accurate layout of the terrain or infrastructure is of paramount importance. Current methods for such tasks often involve deploying human personnel or large, expensive robotic systems, both of which may present significant risk or resource investment. As technology evolves, there is an increasing need for small, cost-effective, and intelligent systems capable of accurately mapping unfamiliar and potentially dangerous environments. By leveraging the advancements in sensor technology and algorithms for localization and mapping, this project provides a robust solution to such challenges, minimizing human risk and optimizing resource utilization.

### *Project Goals*
The goal of this project, we aim to develop an autonomous, smart mapping system utilizing a small, two-wheeled toy car equipped with optical rotational sensors. The system will autonomously traverse an unknown environment, creating a detailed map of the area, and delivering invaluable insights into potentially inaccessible or hazardous regions. This project will build upon our previous capstone project, where we developed a novel wheel-based asset localization framework for real-time tracking
of asset movement. This framework uses 9-degree inertial sensors (accelerometer, gyro, magnetometer) installed on the wheels of assets, interpreting rotational velocity readings to calculate distance traveled and relative location using trigonometric transformations and heading calculations.

### *Key Tasks*
Key tasks for this project will include:
* i) Replacing the original inertial sensors with more accurate optical rotational sensors and incorporating these into the current framework;
* ii) Adapting the framework to accommodate the new sensors, enhancing the precision of wheel rotations and distance computations;
* iii) Developing a SLAM-like layer to utilize sensor data for precise environmental mapping;
* iv) Creating a user interface for real-time visualization of the generated map and the toy car's location within it.

Through participation in this project, students will acquire a deep understanding of sensor technology and data integration, principles and applications of SLAM algorithms, and the development of autonomous systems. Furthermore, they'll gain experience in problem-solving and innovation, equipping them with essential skills for their future careers in technology and engineering.

---

## *GitHub repository contents*

| Folder | Description |
|---|---|
| Documentation |  all documentation the project team has created to describe the architecture, design, installation and configuratin of the peoject |
| Notes and Research | Relavent information useful to understand the tools and techniques used in the project. |
| Status Reports | Project management documentation - weekly reports, milestones, etc. |
| src | Source code - create as many subdirectories as needed |
| Simulation | Autonomous mapping of environment using only rotary optical encoder input. Boundary mapping via simulated collisions.

## Project Team
- *Tamer Nadeem*  - *University Affiliate* - Mentor
- *Tamer Nadeem* - *VCU College of Engineering* - Technical Advisor
- *Tamer Nadeem* - *Computer Science* - Faculty Advisor

- *Luke Unterman* - *Computer Science* - Student Team Member
- *Tahshon Holmes* - *Computer Science* - Student Team Member
- *Imanol Murillo* - *Computer Science* - Student Team Member
- *Mallika Lakshminarayan* - *Computer Science* - Project Team Leader

---

## Updated/Newly Created Files

- ``/src/app/Aggregator/sensor_to_raw_msg_handler.py``: Altered file to intitialize and handle GoDirect sensor processes. Spawned by initialize.py.
- ``/src/app/Aggregator/sensors.py``: Altered file, instead of using Metawear library to publish data from sensors, now using GoDirect library to retrieve data from optical rotary encoder sensors.
- ``/src/app/lib/messages.py``: Updated messages.py file to include additional payload information, including msg_count, sensor_type. Removed accX,Y,Z and gyroX,Y,Z fields.
- ``/src/app/Transformation/raw_to_linear_msg_handler.py``: Updated script to ignore messages with sensor_type IMU: used for visualization of multiple sensors
- ``/src/app/Transformation/raw_to_linear.py``: Updated to read from new 'degPerSec' field in Messages.py instead of 'gyroZ'
- ``/src/app/Transformation/linear_to_location.py``: Currently remains the same, although in previous commits updated logic (now commented) to prioritize straight lines instead of turning
- ``/src/app/log_reader/read_log.py``: Utility program, given keys of log file outputs associated values from log file. Accepts filename as input, outputs list of column values. 
- ``/Simulation/boundary_points(-2).py``:
- ``/Simulation/convex-hull-2.py``:
- ``/src/Sensor Drift Test logs/``: Contains extensive collection of test performed between GoDirect/IMU (videos on Google Drive RovoMapper folder)
- ``/src/app/GPS/read_log.py``: Updated version of log reader, given x, y values from .log file, output proposed lat/lon values to .csv
- ``/src/app/GPS/receive_gps.py``: Connects to GPS2IP app, saves lat/lon values from smartphone to csv file. Input: ip address, port number. Output: csv file of lat, lon values collected from phone.
- ``/src/app/GPS/plot_gps.py``: Using gmplot and oauth token from Google Maps, given input of real GPS csv and proposed GPS csv, outputs .html file showing each of the GPS paths.
- ``/src/app/Visualization/Components/plotter_gui.py``: Updated on_message function to add message_counts to print statements, also given messages contents, differentiates IMU vs GoDirect data points
- ``/src/app/Visualization/Components/graph.py``: Updated to be able to visualize two different types of data, IMU vs GoDirect. IMU data is red with '+' shape, GoDirect data is blue with 'o' shape.
- ``/src/analyze_drift.ipynb``: Given (IMU) .log file as input, outputs Allan deviation plot
- ``/src/config.json``: Updated sub/pub destinations to prevent IMU/GoDirect messages from being mixed up

-----

## Usage Instructions:
- Install dependencies from requirements.txt
- Install Mosquitto message broken on system, GDX library
- To plot GPS paths, install GPS2IP on smartphone, change values of receive_gps.py to allow for differences in IP_ADDR and PORT
  - Ensure that you have an oauth token from Google Maps to plot using gmplot
- How to Run:
  - Ensure GoDirect sensors are turned on, with blinking red LEDs for both
  - Ensure that sensors are in close proximity to Raspberry Pi
  - If desired, update config.json file to read log data instead or write messages to .log file
  - In /src/, to run project, do `python3 initialize.py`
  - To visualize output, in /src/, do `python3 visualization-PyQt.py`
  - To record output from both sensors, first finish visualization task using GoDirect. Once task is complete, use Ctrl C to stop initialize.py without reseting visualizer.
      - Then, you can connect to the other sensor via bluetooth (if IMU, this is done in CS-23-..) folder via initialize.py
      - Once connected, the IMU output will overlap on top of the GoDirect output collected previously!

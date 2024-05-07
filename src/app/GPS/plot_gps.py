import time
import gmplot
from datetime import datetime
import pandas as pd

api_key = "AIzaSyBSdYEwAqyC_xHnOQ5V4EMNdBYfQh9tpTU"

df = pd.read_csv('output.csv')
lat = df.iloc[:, 0].to_numpy()
lon = df.iloc[:, 1].to_numpy()

df_pred = pd.read_csv('gps_projected_original.csv')
pred_lat = df_pred.iloc[:, 0].to_numpy()
pred_lon = df_pred.iloc[:, 1].to_numpy()

richmond_lat = lat[0]
richmond_lon = lon[0]


gmap = gmplot.GoogleMapPlotter(richmond_lat, 
                                richmond_lon, 20, apikey=api_key) 

gmap.plot(lat, lon, color="#FF0000")
gmap.plot(pred_lat, pred_lon, color="#FFFFFF")
gmap.map_type = "hybrid"
gmap.draw('map_first_loop_original.html')
    
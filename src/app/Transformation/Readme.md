The Transformation Layer is responsible for transforming raw sensor data into x,y coordinates for an asset.  

This transformation happens in several stages:    
 - Raw sensor data to linear distance traveled over an interval for a left and right wheel.
 - Linear distance data to x,y coordinates.

 Along the way a message broker is utilized to handle sending data between the transformation stages.

 *TODO: layout the transformation layer architecture* 
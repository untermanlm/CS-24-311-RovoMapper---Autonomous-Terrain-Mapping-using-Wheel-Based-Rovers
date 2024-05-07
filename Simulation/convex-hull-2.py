from functools import cmp_to_key
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
import math

# A class used to store the x and y coordinates of points
class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

# A global point needed for sorting points with reference
# to the first point
p0 = Point(0, 0)

# A utility function to find next to top in a stack
def nextToTop(S):
    return S[-2]

# A utility function to return square of distance
# between p1 and p2
def distSq(p1, p2):
    return ((p1.x - p2.x) * (p1.x - p2.x) +
            (p1.y - p2.y) * (p1.y - p2.y))

# To find orientation of ordered triplet (p, q, r).
# The function returns following values
# 0 --> p, q and r are collinear
# 1 --> Clockwise
# 2 --> Counterclockwise
def orientation(p, q, r):
    val = ((q.y - p.y) * (r.x - q.x) -
           (q.x - p.x) * (r.y - q.y))
    if val == 0:
        return 0  # collinear
    elif val > 0:
        return 1  # clock wise
    else:
        return 2  # counterclock wise

# A function used by cmp_to_key function to sort an array of
# points with respect to the first point
def compare(p1, p2):
    # Find orientation
    o = orientation(p0, p1, p2)
    if o == 0:
        if distSq(p0, p2) >= distSq(p0, p1):
            return -1
        else:
            return 1
    else:
        if o == 2:
            return -1
        else:
            return 1

# Jarvis March algorithm to find the convex hull
def jarvisMarch(points):
    n = len(points)
    if n < 3:
        return []

    hull = []
    l = 0
    for i in range(1, n):
        if points[i].x < points[l].x:
            l = i

    p = l
    while True:
        hull.append(p)
        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i
        p = q
        if p == l:
            break

    return hull

# Read points from the file
points = []
with open("points.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line:
            x, y = map(float, line[1:-1].split(","))
            points.append(Point(x, -y))

# Find the convex hull using Jarvis March algorithm
hull_indices = jarvisMarch(points)
convex_hull_points = [points[i] for i in hull_indices]

# Threshold distance
threshold = 30  # Adjust this threshold value as needed

# Iterate over each line segment of the convex hull
for i in range(len(convex_hull_points)):
    p1 = convex_hull_points[i]
    p2 = convex_hull_points[(i + 1) % len(convex_hull_points)]
    
    # Calculate line equation parameters
    A = p2.y - p1.y
    B = p1.x - p2.x
    C = A * p1.x + B * p1.y
    
    # Calculate distance of each non-convex hull point to the line segment
    for point in points:
        if point not in convex_hull_points:
            distance = abs(A * point.x + B * point.y - C) / math.sqrt(A**2 + B**2)
            if distance <= threshold:
                points.remove(point)  # Remove points marked for deletion

# Extract x and y coordinates from the remaining points
x_coords = [point.x for point in points]
y_coords = [point.y for point in points]

# Apply DBSCAN clustering to the remaining points
X = np.array(list([x, y] for x, y in zip(x_coords, y_coords)))
# Calculate the average distance between points
average_distance = np.mean([np.linalg.norm(point1 - point2) for point1 in X for point2 in X])

# Set the threshold as a fraction of the average distance
threshold_fraction = 0.1  # Adjust as needed
threshold = threshold_fraction * average_distance

# Set epsilon as a fraction of the average distance
epsilon_fraction = 0.8  # Adjust as needed
epsilon = epsilon_fraction * average_distance

# Set minimum_samples based on the density of points
# Adjust as needed based on the desired density
min_samples = min(5, len(X) // 10)  

# Apply DBSCAN clustering with adjusted parameters
clustering = DBSCAN(eps=epsilon, min_samples=min_samples).fit(X)


# Generate colors for an unknown amount of clusters
groups = set(clustering.labels_)
colors = plt.cm.rainbow(np.linspace(0, 1, len(groups)))

# Plot clusters
for group, color in zip(groups, colors):
    cluster_points = X[clustering.labels_ == group]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], color=color, label=f'Cluster {group}')

# Extract x and y coordinates from the convex hull points
convex_hull_x = [point.x for point in convex_hull_points]
convex_hull_y = [point.y for point in convex_hull_points]

# Plot the convex hull
plt.plot(convex_hull_x + [convex_hull_x[0]], convex_hull_y + [convex_hull_y[0]], color='blue')


# Show the plot
plt.show()

# So the threshold, epsilon, and minimum_samples all seemingly need to be adjusted each run through of the program when it gets a new set of points

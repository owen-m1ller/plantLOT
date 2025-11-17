import sys
import os
import open3d as o3d
import numpy as np
from sklearn.cluster import KMeans

cloud = sys.argv[1] # input as ply file

cloud = o3d.io.read_point_cloud(cloud)
points = np.asarray(cloud.points)

k = int(sys.argv[2])

kmeans = KMeans(n_clusters=k).fit(points)

dwnsample_cloud = o3d.geometry.PointCloud()
dwnsample_cloud.points = o3d.utility.Vector3dVector(kmeans.cluster_centers_)

o3d.io.write_point_cloud("dwnsampled.ply", dwnsample_cloud)


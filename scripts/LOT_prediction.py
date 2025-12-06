import os
import sys
import ot
import numpy as np
import open3d as o3d
from utils import bary_proj, interpolate

cloud1_f = sys.argv[1]
cloud2_f = sys.argv[2]
reference_f = sys.argv[3] # at the moment, this must be one of the pcds.

cloud1 = o3d.io.read_point_cloud(cloud1_f)
cloud2 = o3d.io.read_point_cloud(cloud2_f)
reference = o3d.io.read_point_cloud(reference_f)

reference_points = np.asarray(reference.points)

T1 = np.asarray(bary_proj(reference, cloud1).points)
T2 = np.asarray(bary_proj(reference, cloud2).points)

print(T1.shape, T2.shape, reference_points.shape)

prediction = T2 + T2 - T1

dist=0
i=0
while dist <= 1:
    interpolated = interpolate(T2, prediction, dist)
    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(interpolated)
    o3d.io.write_point_cloud(f'../render/frame{i}.ply', cloud)
    dist += .01
    i += 1



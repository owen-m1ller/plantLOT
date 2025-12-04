import os
import sys
import ot
import numpy as np
import open3d as o3d
import shutil
from utils import bary_proj, interpolate

cloud1f = sys.argv[1]
cloud2f = sys.argv[2]

proj = bary_proj(cloud1f, cloud2f)

arr1 = np.asarray(o3d.io.read_point_cloud(cloud1f).points)
arr2 = np.asarray(proj.points)

l = float(sys.argv[3])

dist = 0
i = 0

while dist <= 1:
    interpolated = interpolate(arr1, arr2, dist)
    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(interpolated)
    o3d.io.write_point_cloud(f'../render/frame{i}.ply', cloud)
    dist += l
    i += 1


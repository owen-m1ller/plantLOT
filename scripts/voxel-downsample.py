import sys
import os
import open3d as o3d
import numpy as np
from sklearn.cluster import KMeans

cloud = sys.argv[1] # input as ply file

cloud = o3d.io.read_point_cloud(cloud)

voxel_size = float(sys.argv[2])
vxl_dwnsampled = cloud.voxel_down_sample(voxel_size)

o3d.io.write_point_cloud("vxl-dwnsampled.ply", vxl_dwnsampled)


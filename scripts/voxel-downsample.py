import sys
import os
import open3d as o3d
import numpy as np

cloud = sys.argv[1] # input as ply file

cloud = o3d.io.read_point_cloud(cloud)

voxel_size = float(sys.argv[2])
vxl_dwnsampled = cloud.voxel_down_sample(voxel_size)

new_name = sys.argv[1].replace('.ply', '_dwnsampled.ply')

o3d.io.write_point_cloud(f"{new_name}", vxl_dwnsampled)


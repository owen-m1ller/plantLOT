import numpy as np
import ot
import open3d as o3d
import sys
from utils import bary_proj

cloud_1_f = sys.argv[1] # input the file path of the first point cloud
cloud_2_f = sys.argv[2] # input the file path of the second point cloud

output = bary_proj(cloud_1_f, cloud_2_f)

folder = '/'.join(cloud_1_f.split('/')[:-1])
cloud_1_fname = cloud_1_f.split('/')[-1].replace('.ply', '')
cloud_2_fname = cloud_2_f.split('/')[-1].replace('.ply', '')

outputf = f'{folder}/{cloud_1_fname}-{cloud_2_fname}-bary.ply'

o3d.io.write_point_cloud(outputf, output)


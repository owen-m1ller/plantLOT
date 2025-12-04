import open3d as o3d
import numpy as np
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / '.env')

DATA_DIR = (REPO_ROOT / os.getenv("DATA_DIR")).resolve()

cloud = np.loadtxt(DATA_DIR /sys.argv[1])
cloud = cloud[:, :3]

o3_cloud = o3d.geometry.PointCloud()
o3_cloud.points = o3d.utility.Vector3dVector(cloud)

new_name = sys.argv[1].replace('_a.txt', '.ply')
new_name = new_name.replace('.txt', '.ply')

o3d.io.write_point_cloud(DATA_DIR / f"{new_name}", o3_cloud)


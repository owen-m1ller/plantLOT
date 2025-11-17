import open3d as o3d
import numpy as np
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / '.env')

DATA_DIR = (REPO_ROOT / os.getenv("DATA_DIR")).resolve()

pcd_xyz = np.loadtxt(DATA_DIR / sys.argv[1], delimiter=" ")
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(pcd_xyz)
o3d.visualization.draw_geometries([pcd])

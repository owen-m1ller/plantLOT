import numpy as np
import torch
import open3d as o3d
import re
import argparse

from model import MotionNet
from utils import fps, normalize_cloud

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_txt_pc(path):
    """Load x y z from Pheno4D TXT file."""
    return np.loadtxt(path)[:, :3]


def to_o3d(pc, color):
    """Convert Nx3 array into an Open3D point cloud with RGB color."""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pc)
    pcd.colors = o3d.utility.Vector3dVector(np.tile(color, (pc.shape[0], 1)))
    return pcd


def visualize(P_t, P_t_pred, P_t1):
    """Display original, predicted, and ground truth."""
    pcd_t = to_o3d(P_t,  [0.2, 0.8, 0.2])   # green
    pcd_pred = to_o3d(P_t_pred, [0.1, 0.1, 0.9])  # blue
    pcd_t1 = to_o3d(P_t1, [0.9, 0.1, 0.1])  # red

    o3d.visualization.draw_geometries([pcd_t, pcd_pred, pcd_t1])


def main(args):
    # Paths
    # --plant (Maize01)
    # then --t0 (0313)
    # then --t1 (0314)
    plant_folder = args.plant
    plant_prefix = re.sub(r"\d+", "", args.plant).lower()
    path_t0 = f"data/{plant_folder}/{plant_folder[0]}{plant_folder[-2:]}_{args.t0}.txt"
    path_t1 = f"data/{plant_folder}/{plant_folder[0]}{plant_folder[-2:]}_{args.t1}.txt"

    # ---- Load point clouds ----
    P_t0 = load_txt_pc(path_t0)
    P_t1 = load_txt_pc(path_t1)

    # ---- Normalize + FPS ----
    P_t0 = normalize_cloud(P_t0)
    P_t1 = normalize_cloud(P_t1)

    P_t_ds = fps(P_t0, num=4096)
    P_t1_ds = fps(P_t1, num=4096)

    # ---- Load model ----
    model = MotionNet().to(device)
    model.load_state_dict(torch.load("motionnet_pheno4d_mac.pth", map_location=device))
    model.eval()

    # ---- Predict flow ----
    with torch.no_grad():
        P_t_tensor = torch.tensor(P_t_ds, dtype=torch.float32).unsqueeze(0).to(device)
        pred_flow = model(P_t_tensor)[0].cpu().numpy()

    # ---- Generate predicted next frame ----
    P_t_pred = P_t_ds + pred_flow

    # ---- Visualize ----
    visualize(P_t_ds, P_t_pred, P_t1_ds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--plant", type=str, required=True,
                        help="Plant ID, e.g. M01, T02, etc.")
    parser.add_argument("--t0", type=str, required=True,
                        help="Timestamp for first scan, e.g. 0313")
    parser.add_argument("--t1", type=str, required=True,
                        help="Timestamp for second scan, e.g. 0314")
    args = parser.parse_args()
    main(args)   # ✅ pass args here!

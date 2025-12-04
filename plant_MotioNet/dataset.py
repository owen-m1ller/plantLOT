import os
import numpy as np
from glob import glob
from torch.utils.data import Dataset
from scipy.spatial import cKDTree
import torch
from utils import fps, normalize_cloud


class Pheno4DDataset(Dataset):
    def __init__(self, root, num_points=4096):
        """
        root: directory containing plant subfolders
        """
        self.num_points = num_points
        self.pairs = []  # (path_t, path_t1)

        plants = sorted([d for d in glob(os.path.join(root, "*")) if os.path.isdir(d)])

        for plant in plants:
            scans = sorted(glob(os.path.join(plant, "*.txt")))
            for i in range(len(scans) - 1):
                self.pairs.append((scans[i], scans[i+1]))

    def load_txt_pc(self, path):
        pc = np.loadtxt(path)[:, :3]  # keep x,y,z only
        return pc

    def compute_flow(self, P_t, P_t1):
        tree = cKDTree(P_t1)
        _, idx = tree.query(P_t)
        return P_t1[idx] - P_t

    def __getitem__(self, idx):
        path_t, path_t1 = self.pairs[idx]

        P_t = self.load_txt_pc(path_t)
        P_t1 = self.load_txt_pc(path_t1)

        # Normalize
        P_t = normalize_cloud(P_t)
        P_t1 = normalize_cloud(P_t1)

        # FPS downsample
        P_t = fps(P_t, self.num_points)
        P_t1 = fps(P_t1, self.num_points)

        # GT flow
        flow = self.compute_flow(P_t, P_t1)

        return (
            torch.tensor(P_t, dtype=torch.float32),
            torch.tensor(P_t1, dtype=torch.float32),
            torch.tensor(flow, dtype=torch.float32)
        )

    def __len__(self):
        return len(self.pairs)

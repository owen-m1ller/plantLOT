import numpy as np
import torch

def normalize_cloud(pc):
    pc = pc - pc.mean(axis=0, keepdims=True)
    scale = np.max(np.linalg.norm(pc, axis=1))
    return pc / scale

def fps(pc, num=4096):
    """
    Pure NumPy Farthest Point Sampling.
    pc: (N,3)
    """
    N = pc.shape[0]
    cent = np.mean(pc, axis=0)
    dist = np.linalg.norm(pc - cent, axis=1)

    farthest = np.argmax(dist)
    sample_inds = [farthest]
    distances = np.linalg.norm(pc - pc[farthest], axis=1)

    for _ in range(num - 1):
        farthest = np.argmax(distances)
        sample_inds.append(farthest)
        distances = np.minimum(distances,
                               np.linalg.norm(pc - pc[farthest], axis=1))
    return pc[sample_inds]
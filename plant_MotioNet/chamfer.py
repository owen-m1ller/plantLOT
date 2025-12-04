import torch

def chamfer_distance(pc1, pc2):
    """
    pc1, pc2: (B, N, 3)
    """
    pc1_expanded = pc1.unsqueeze(2)        # (B, N, 1, 3)
    pc2_expanded = pc2.unsqueeze(1)        # (B, 1, M, 3)

    dist = torch.sum((pc1_expanded - pc2_expanded)**2, dim=-1)  # (B, N, M)

    min1 = torch.min(dist, dim=2)[0]  # (B, N)
    min2 = torch.min(dist, dim=1)[0]  # (B, M)

    return min1.mean() + min2.mean()
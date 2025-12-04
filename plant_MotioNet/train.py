from chamfer import chamfer_distance
from dataset import Pheno4DDataset
from model import MotionNet
from torch.utils.data import DataLoader
import torch

def train():
    dataset = Pheno4DDataset(root="data/", num_points=4096)
    loader = DataLoader(dataset, batch_size=1, shuffle=True)

    model = MotionNet()
    model.train()

    opt = torch.optim.Adam(model.parameters(), lr=1e-4)

    for epoch in range(10):
        for P_t, P_t1, flow_gt in loader:
            pred_flow = model(P_t)

            P_pred = P_t + pred_flow

            loss_cd = chamfer_distance(P_pred, P_t1)
            loss_flow = ((pred_flow - flow_gt)**2).mean()

            loss = loss_cd + 0.1 * loss_flow

            opt.zero_grad()
            loss.backward()
            opt.step()

        print(f"Epoch {epoch} - Loss: {loss.item():.4f}")

    torch.save(model.state_dict(), "motionnet_pheno4d_mac.pth")

if __name__ == '__main__':
    train()

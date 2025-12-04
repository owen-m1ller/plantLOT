import torch
import torch.nn as nn


class PointNetEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(3, 64), nn.ReLU(),
            nn.Linear(64, 128), nn.ReLU(),
            nn.Linear(128, 256), nn.ReLU(),
        )

    def forward(self, x):
        # x: (B, N, 3)
        feat = self.mlp(x)
        global_feat = torch.max(feat, dim=1, keepdim=True)[0]
        global_feat = global_feat.expand_as(feat)
        return torch.cat([feat, global_feat], dim=-1)  # (B, N, 512)


class FlowDecoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(512, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, 3)
        )

    def forward(self, x):
        return self.mlp(x)


class MotionNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = PointNetEncoder()
        self.decoder = FlowDecoder()

    def forward(self, x):
        feat = self.encoder(x)
        flow = self.decoder(feat)
        return flow

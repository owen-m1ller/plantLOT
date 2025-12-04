import numpy as np
import ot
import time

day2 = np.loadtxt("../data/Tomato01/T01_0306.txt")[::100] # downsample
day4 = np.loadtxt("../data/Tomato01/T01_0308.txt")[::100]

print(day4.shape)
print(day2.shape)
xt_list = [day2, day4]
xr = np.random.normal(0.0, 1.0, size=(2000, 3))
start_lot = time.time()
def lot_embed_point_clouds(
    xr,
    xt_list,
    r_mass=None,
    xt_masses=None,
    sinkhorn=False,
    lambd=1.0,
    normalize_T=False,
    eps=1e-8,
):
    
    xr = np.asarray(xr)
    m, d = xr.shape

    if r_mass is None:
        a = np.ones(m, dtype=float) / m
    else:
        r_mass = np.asarray(r_mass, dtype=float)
        a = r_mass / r_mass.sum()  

    if xt_masses is None:
        xt_masses = [None] * len(xt_list)

    embeddings = []

    for X, b in zip(xt_list, xt_masses):
        X = np.asarray(X)
        n = X.shape[0]

        if b is None:
            b = np.ones(n, dtype=float) / n
        else:
            b = np.asarray(b, dtype=float)
            b = b / b.sum()

        M = ot.dist(xr, X) 

        if sinkhorn:
            G = ot.sinkhorn(a, b, M, reg=lambd)
        else:
            G = ot.emd(a, b, M)

        G1 = G @ np.ones(n)
        G_stochastic = G / (G1[:, None] + eps) 

        T = G_stochastic @ X  # shape (m, d)

        if normalize_T:
            T = T / np.sqrt(m)

        V = T - xr 

        embeddings.append(V)

    T_embeddings = np.stack(embeddings, axis=0)
    return T_embeddings

start_lot = time.time()
T_embeddings = lot_embed_point_clouds(
    xr,
    xt_list,
    xt_masses=None,
    sinkhorn=False,   
    lambd=1,
    normalize_T=False
)
end_lot = time.time()

T_day2 = T_embeddings[0]
T_day4 = T_embeddings[1]

w2_lot = np.linalg.norm(T_day2 - T_day4)

print("LOT-approximation W2(day2, day4):", w2_lot)
print("LOT embedding + distance time: {:.4f} seconds".format(end_lot - start_lot))


start_ot = time.time()

a = np.ones(day2.shape[0]) / day2.shape[0]
b = np.ones(day4.shape[0]) / day4.shape[0]

M = ot.dist(day2, day4) ** 2

w2_sq_true = ot.emd2(a, b, M)
w2_true = np.sqrt(w2_sq_true)

end_ot = time.time()

print("True W2(day2, day4) from OT:", w2_true)
print("True OT time: {:.4f} seconds".format(end_ot - start_ot))




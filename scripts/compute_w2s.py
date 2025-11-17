import numpy as np
import ot

day2 = np.loadtxt("../data/Tomato01/T01_0306.txt")[::100] # downsample
day4 = np.loadtxt("../data/Tomato01/T01_0308.txt")[::100]

print(day4.shape)
print(day2.shape)

unif_day2 = np.ones(day2.shape[0]) / day2.shape[0]
unif_day4 = np.ones(day4.shape[0]) / day4.shape[0]

cost = ot.dist(day2, day4, metric='euclidean') ** 2

w2_sinkhorn = np.sqrt(ot.emd2(unif_day2, unif_day4, cost))

print(w2_sinkhorn)

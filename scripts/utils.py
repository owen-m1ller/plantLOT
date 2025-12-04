import open3d as o3d
import numpy as np
import ot


def bary_proj(cloud_1_f, cloud_2_f):
    '''
    Compute the barycenteric projection from point cloud 1 to point cloud
    2. Finds an exact optimal transport solution.
    '''
    cloud_1 = o3d.io.read_point_cloud(cloud_1_f)
    cloud_2 = o3d.io.read_point_cloud(cloud_2_f)

    cloud_1_pts = np.asarray(cloud_1.points)
    cloud_2_pts = np.asarray(cloud_2.points)

    unif_cloud_1 = np.ones(cloud_1_pts.shape[0]) / cloud_1_pts.shape[0]
    unif_cloud_2 = np.ones(cloud_2_pts.shape[0]) / cloud_2_pts.shape[0]

    cost = ot.dist(cloud_1_pts, cloud_2_pts, metric='sqeuclidean')
    cost = cost / cost.max()

    coupling = ot.emd(unif_cloud_1, unif_cloud_2, M=cost)
    bary_proj = cloud_1_pts.shape[0] * coupling @ cloud_2_pts

    output = o3d.geometry.PointCloud()
    output.points = o3d.utility.Vector3dVector(bary_proj)

    return output


def interpolate(arr1, arr2, l):
    '''
    Interpolate between arrays representing two point clouds. 
    l is a scalar in [0, 1]
    '''
    return (1 - l) * arr1 + l * arr2


import numpy as np
from sklearn.cluster import DBSCAN
import copy
import gc
from pathlib import Path
import pandas as pd
import os

# These imports may not work, may need additional things installed

import open3d as o3d
import sys
from dotenv import load_dotenv

import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Takes in the Pheno4d folder (or whatever its named) that contains the smaller folders with the plant data
# Creates a big dictionary with subdictionaries: Maize/Tomato0x -> file_name of different days -> points and labels

def load_in_plants(folder_name):
    root_dir = Path(folder_name)
    species = ["Maize", "Tomato"]
    indices = range(1, 8)  
    
    def load_plant(file_path):
        data = np.loadtxt(file_path)
        if data.shape[1] > 3:
            pts = data[:, :3]
            labels = data[:, 3:]
            return pts, labels
        else:
            return data, None
    
    all_plants = {}
    
    for s in species:
        for i in indices:
            folder_name = f"{s}0{i}"
            folder_path = root_dir / folder_name
            
            if not folder_path.exists():
                print(f"Folder missing: {folder_path}")
                continue
            
            all_plants[folder_name] = {}

            for file_path in sorted(folder_path.glob("*.txt")):
                pts, labels = load_plant(file_path)
                all_plants[folder_name][file_path.stem] = {
                    "points": pts,
                    "labels": labels
                }

    return all_plants

# Finds the minimum z-coordinate of any point in the data and moves it up to 0 along with every other point in accordance. Takes in a single point cloud

def shift_up(plant):
    z_coordinate_min = pd.DataFrame(plant)[2].min()

    if z_coordinate_min >= 0:
        shift = np.repeat(-z_coordinate_min, plant.shape[0]).reshape(-1,1)
        padded = np.concatenate((np.zeros((plant.shape[0], 2)), shift), axis = 1)
        return plant + padded
    else:
        shift = np.repeat(abs(z_coordinate_min), plant.shape[0]).reshape(-1,1)
        padded = np.concatenate((np.zeros((plant.shape[0], 2)), shift), axis = 1)
        return plant + padded
    
#truncates the plant below some certain z-value. Takes in a single point cloud.

def truncate(plant, value, labels=None):
    plant_df = pd.DataFrame(plant)
    labels_df = None

    indices = plant_df[plant_df[2] > value].index

    if labels is not None:
        labels_df = pd.DataFrame(labels).iloc[indices].to_numpy()

    truncated_points = plant_df.iloc[indices].to_numpy()

    del indices
    gc.collect()
    
    return [truncated_points, labels_df]

#takes the truncated points and runs a dbscan to remove any outliers hanging around the sides
    
def clean_outliers(truncated_points, epsilon, cluster_size, plant_labels=None):
    DBSCAN_cluster = DBSCAN(eps=epsilon, min_samples=cluster_size).fit(truncated_points)

    labels = DBSCAN_cluster.labels_

    unique, counts = np.unique(labels[labels != -1], return_counts=True)
    largest_label = unique[np.argmax(counts)]

    indices = labels == largest_label

    cleaned_points = truncated_points[indices]
    
    final_plant_labels = None
    if plant_labels is not None:
        final_plant_labels = plant_labels[indices]

    del DBSCAN_cluster
    del labels
    del unique, counts
    del largest_label
    del indices
    gc.collect()

    return [cleaned_points, final_plant_labels]

# probably dont use this function. It runs the data processing (the above three functions in succession) on all the point clouds. This will likely cause a memory allocation failure.

def process_data(all_plants):
    
    for plant_evolution in all_plants:
        for plant in all_plants[plant_evolution]:
            shifted_up = shift_up(all_plants[plant_evolution][plant]['points'])
            truncated = truncate(shifted_up, 10, all_plants[plant_evolution][plant]['labels'])
            cleaned = clean_outliers(truncated[0], 1, 10, truncated[1])

            all_plants[plant_evolution][plant]['points'] = cleaned[0]
            all_plants[plant_evolution][plant]['labels'] = cleaned[1]

            del shifted_up
            del truncated
            gc.collect()

    return all_plants

#This is useless too, just a loop that creates pop up visualizations. Better to use blender or something.


for plant_evolution in all_plants:
    for plant in all_plants[plant_evolution]:
        points = all_plants[plant_evolution][plant]['points']

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        o3d.visualization.draw_geometries([pcd]);
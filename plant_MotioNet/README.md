# Instructions for Training the Model

Assuming you are in the `plant_MotioNet` directory, run `train.py`. This will create a file in the directory called 
`motionnet_pheno4d_mac.pth`, which contains the temporary parameters that PyTorch got when training the model. Feel free to tune 
the learning rate and number of epochs in `train.py` to compare performances.

After, in the same directory, run `python visualize_prediction.py` but with three arguments:
- `--plant`: The plant number of which you want to look at, e.g. `Maize01`
- `--t0`: First time frame as a 4 digit date
- `--t1`: Second time frams as a 4 digit date

An example of running the script after the model has been trained would be
```
python visualize_prediction.py --plant Maize05 --t0 0314 --t1 0315
```
Then open3d will display an interactable model of the point cloud for the plant.

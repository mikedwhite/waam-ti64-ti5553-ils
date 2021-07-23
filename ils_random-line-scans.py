"""Determine inter-lamellar spacing and volume fraction for batch of binary images.
"""


import csv
from glob import glob
import os

import numpy as np
from skimage import io, img_as_bool
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 14})
plt.rcParams['figure.dpi'] = 100

from measurements import vol_frac, chord_length
from misc import determine_scaling


# Define paths
input_path = 'binary_tiles/5553on64/TileSet/Line3/'
output_path = f'measurements/{input_path[13:]}'

# ILS parameters
bar_length_um = 10
bar_frac = 1.2/3.8
n_scans = 200
min_length = 20

# Create list of files to be analysed
filenames = sorted(glob(f'{input_path}*.jpg'))
# filenames = [f'{input_path}Tile_128-001-000_0.jpg']

# Create output directory
if not os.path.isdir(output_path):
    os.makedirs(output_path)

# Initialise counter
counter = 0

# Count files
n_files = len(filenames)

# Create storage for intersection count means
cl_mean = []

# Create storage for volume fractions
vf = []

# Create storage for filenames
FILENAME = []

for filename in filenames:

    # Extract filename from full path excluding file extension
    if '/' in filename:
        FILENAME += [filename.split('/')[-1][:-4]]
    else:
        FILENAME += [filename[:-4]]

    # Update counter and print progress
    counter += 1
    print(f'Processing image {counter}/{n_files}: {FILENAME[counter-1]}')

    # Import image
    image = io.imread(filename)

    # Convert image to boolean
    image = img_as_bool(image)

    # Define scale conversion
    um_per_px = determine_scaling(image, bar_length_um, bar_frac)

    # Perform intersection count
    cl = chord_length(image, um_per_px, n_scans, min_length)
    # cl = grain_size.chord_length_uniform(image, um_per_px, n_scans)

    # Determine mean intersection count and store
    cl_mean_temp = np.mean(cl)
    print(f'ILS: {cl_mean_temp}')
    cl_mean += [cl_mean_temp]

    # # Determine volume fraction and store
    vf_temp = vol_frac(image)
    print(f'VF: {vf_temp}')
    vf += [vf_temp]

    # Write results to file
    with open(f'{output_path}{FILENAME[counter-1]}_ils_distribution.txt', 'w') as f:
        for measurement in cl:
            f.write(f'{measurement}' + '\n')

plt.plot(cl_mean)
plt.savefig(f'{output_path}/chord_length_plot.jpg')
plt.show()

plt.plot(vf)
plt.savefig(f'{output_path}/vol_frac_plot.jpg')
plt.show()

# Write results to csv
rows = zip(FILENAME, cl_mean, vf)
with open(f'{output_path}measurements.csv', "w") as f:
    writer = csv.writer(f)
    writer.writerow(['filename', 'chord_length', 'vol_frac'])
    for row in rows:
        writer.writerow(row)

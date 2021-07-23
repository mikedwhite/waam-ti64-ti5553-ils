"""Binarise a batch of micrographs and save results to file for analysis.
"""


from glob import glob
import os

import numpy as np
from skimage import io, color, morphology, img_as_ubyte, filters

from preprocessing import hmf_gauss, otsu


# Define input and output paths
input_path = 'raw_data/5553on64/TileSet/Line3/'
output_path = f'binary_tiles/{input_path[9:]}'
input_filetype = 'tif'
output_filetype = 'jpg'

# Create list of image files to be analysed
filenames = sorted(glob(f'{input_path}*.{input_filetype}'))

# Create output directory
if not os.path.isdir(output_path):
    os.makedirs(output_path)

# initialise counter
counter = 0

for filename in filenames:

    # Extract filename from full path
    if '/' in filename:
        filename = filename.split('/')[-1][:-4]
    else:
        filename = filename[:-4]

    counter += 1
    print(f'Segmenting image {counter}/{len(filenames)}: {filename}')

    # Import micrograph
    image = io.imread(f'{input_path}{filename}.{input_filetype}')

    # Convert to grayscale
    image = color.rgb2gray(image)

    # Define filter parameters
    sigma = 10.
    alpha = 0.5
    beta = 1.5
    pass_type = 'high'

    # Apply filter
    image_hmf = hmf_gauss(image, sigma, alpha, beta, pass_type)

    # Binarise image
    image_binary = otsu(image_hmf)
    # image_binary = niblack(image_hmf, window_size=99)

    # Convert to uint8
    image_binary = img_as_ubyte(image_binary)

    # Invert binary image
    image_binary = np.max(image_binary) - image_binary

    # Perform area closing and opening
    image_binary = morphology.area_closing(image_binary, area_threshold=500)
    image_binary = morphology.area_opening(image_binary, area_threshold=20)

    # Smooth grain boundaries
    image_binary = filters.gaussian(image_binary, sigma=2)

    # Sharpen image
    image_binary = filters.unsharp_mask(image_binary, radius=2, amount=5)

    # Convert to uint8
    image_binary = img_as_ubyte(image_binary)

    # Save binary image
    io.imsave(f'{output_path}{filename}.{output_filetype}', image_binary)

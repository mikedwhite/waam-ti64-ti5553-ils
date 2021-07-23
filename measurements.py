"""Inter-lamellar spacing and volume fraction metrics.
"""


import numpy as np
from mct.misc import remove_outliers
from skimage import measure


def vol_frac(image: np.ndarray) -> np.ndarray:
    """Calculate volume fraction of white space in binary image.

    Parameters
    ----------
    image : ndarray
        Binary image.

    Returns
    -------
    vf : float
        Percentage white space in image.
    """

    vf = 100 * (np.sum(image) / image.size)

    return vf


def chord_length(image: np.ndarray, um_per_px: float, n_scans: int,
                 min_length: float) -> list:
    """Perform intercept (chord) length method with randomly orientated scan
    lines.

    Parameters
    ----------
    image : ndarray
        Binary image.
    um_per_px : float
        Scaling (um per pixel).
    n_scans : int
        Number of randomly orientated line scans to perform.
    min_length : float
        Minimum scan line length to include in measurements (um).

    Returns
    -------
    cl : list of float
        List of chord lengths.

    References
    ----------
    .. [1] ASTM E1382−97 (2015) Standard Test Methods for Determining Average
           Grain Size Using Semiautomatic and Automatic Image Analysis
    """

    # Exclude grains intersecting edge of image field
    # image = clear_border(image)

    # Create storage for returns
    cl = []

    # Initialise counter
    counter = 0

    while counter < n_scans:

        # Create storage for scan line start and end coordinates
        x = []

        # Generate two random integers from 0 to 3 without replacement. Defines
        # side selections for scan line start and end coordinates
        sides = np.random.choice(4, 2, replace=False)

        # Generate random coordinates for a point which lies on each side
        for side in sides:
            if side == 0:
                x.append(int(np.random.uniform(0, image.shape[0])))
                x.append(0)
            elif side == 1:
                x.append(0)
                x.append(int(np.random.uniform(0, image.shape[1])))
            elif side == 2:
                x.append(int(np.random.uniform(0, image.shape[0])))
                x.append(image.shape[1])
            else:
                x.append(image.shape[0])
                x.append(int(np.random.uniform(0, image.shape[1])))

        # Compute intensity profile of scan line
        line_profile = measure.profile_line(image, (x[0], x[1]), (x[2], x[3]))

        # Calculate length of scan line
        line_length = np.sqrt((x[0] - x[2]) ** 2 + (x[1] - x[3]) ** 2) * um_per_px

        # Skip measurement if scan line length is below min_length
        if line_length < min_length:
            continue

        # Determine grain initial and end indices along scan line
        line_profile_dx = np.diff(line_profile)
        idx_init = np.argwhere(line_profile_dx > 0)
        idx_end = np.argwhere(line_profile_dx < 0)

        # Remove excess indices
        if idx_init.size > idx_end.size:
            idx_init = idx_init[:idx_end.size]
        elif idx_init.size < idx_end.size:
            idx_end = idx_end[:idx_init.size]

        # Ensure first index corresponds to an initial index
        try:
            while idx_init[0] > idx_end[0]:
                idx_end = idx_end[1:]
                idx_init = idx_init[:-1]

            # Calculate difference between index vectors
            idx_diff = np.abs(idx_init - idx_end)

            # Convert differences to distance in um and store mean chord length
            cl_temp = idx_diff / line_profile.size * line_length

            # Remove outliers
            try:
                cl_temp = remove_outliers(cl_temp, n_std=1)
            except:
                continue

            # Store mean chord length
            # cl += [np.mean(cl_temp)]
            cl.extend(cl_temp)

            # Update counter
            counter += 1

        except IndexError:
            continue

    return cl

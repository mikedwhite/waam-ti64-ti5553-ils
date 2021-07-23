"""Miscellaneous functions.
"""


import numpy as np


def remove_outliers(x: np.ndarray, n_std: int = 2):
    """Remove outliers, i.e. values, x_i, which lie outside the range
    x_i +- std(x) * n_std.

    Parameters
    ----------
    x : ndarray
        Input data.
    n_std : int
        Number of standard deviations to retain data within (2, by default).

    Returns
    -------
    ndarray
        Data with outliers removed. Returned as 1d array regardless of input
        shape.
    """

    if x.ndim > 1:
        x = x.reshape(-1)

    return x[abs(x - np.mean(x)) < n_std * np.std(x)]


def determine_scaling(image: np.ndarray, bar_length_um: float,
                      bar_frac: float) -> float:
    """Determine um per pixels scaling for an image provided the bar length in
    um and the fraction of the image for which it occupies.

    Parameters
    ----------
    image : ndarray
        Input image. Must be grayscale.
    bar_length_um : float
        Length of scale bar (um).
    bar_frac : float
        Fraction of the image width occupied by the scale bar.

    Returns
    -------
    um_per_px : float
        Scaling (um per px).
    """

    # Convert bar length from um to pixels
    bar_length_px = bar_frac * image.shape[1]

    # Determine conversion
    um_per_px = bar_length_um/bar_length_px

    return um_per_px

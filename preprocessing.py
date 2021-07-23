"""Homomorphic Gaussian filter and Otsu thresholding for data preprocessing.
"""


import numpy as np
from skimage import img_as_float
from skimage.filters import threshold_otsu


def hmf_gauss(image: np.ndarray, sigma: float = 1., alpha: float = 0.,
              beta: float = 1., pass_type: str = 'low') -> np.ndarray:
    """Apply emphasised Gaussian homomorphic filter of the form
        H_emphasis = alpha + beta * H,
    where H is a Gaussian filter with standard deviation sigma.

    Parameters
    ----------
    image : ndarray
        Input image. Must be grayscale.
    sigma : float, optional
        Gaussian filter standard deviation (1.0, by default).
    alpha : float, optional
        Gaussian filter offset (0.0, by default).
    beta : float, optional
        Gaussian filter scaling (1.0, by default).
    pass_type : str, optional
        'low' (default)
            Applies a low-pass filter.
        'high'
            Applies a high-pass filter.

    Returns
    -------
    image : ndarray
        Grayscale filtered image normalised to the range [0,1].
    """

    # Define original image size
    m, n = image.shape[0], image.shape[1]

    # Convert to float
    image = img_as_float(image)

    # Take log
    image = np.log(1 + image)

    # Pad image with replicated image edges
    image = np.pad(image, ((np.int(m/2),), (np.int(n/2),)), mode='edge')

    # Construct Gaussian filter
    M, N = 2*m, 2*n
    X, Y = np.meshgrid(np.linspace(0, N, N+1), np.linspace(0, M, M+1))
    X_centre, Y_centre = np.ceil((N+1)/2), np.ceil((M+1)/2)
    hmf = np.exp(-((X-X_centre)**2+(Y-Y_centre)**2)/(2*sigma**2))
    if pass_type == 'high':
        hmf = 1 - hmf

    # Rearrange filter
    hmf = np.fft.fftshift(hmf)

    # Offset and scale filter
    hmf = alpha + beta*hmf

    # Apply Fourier transform to image
    image = np.fft.fft2(image, s=(M + 1, N + 1))

    # Apply filter and inverse fourier transform
    image = np.real(np.fft.ifft2(hmf * image))

    # Crop filtered image to original size
    image = image[int(np.ceil(M/2)-m/2):int(np.ceil(M/2)+m/2),
                  int(np.ceil(N/2)-n/2):int(np.ceil(N/2)+n/2)]

    # Take exponential
    image = np.exp(image) - 1

    # Normalise image to lie in range 0 to 1
    image -= np.amin(image)
    image /= np.amax(image)

    return image


def otsu(image, n_bins=256, T_shift=0) -> np.ndarray:
    """Return binary image image > T for T determined globally by Otsu's method.

    Parameters
    ----------
    image : ndarray
        Input image. Must be grayscale.
    n_bins : int, optional
        Number of histogram bins for computing global threshold (256, by
        default).
    T_shift : float
        Alteration to make to detected threshold, T (0, by default).

    Returns
    -------
    image_binary : ndarray
        Binarised image. Pixels (x,y) where image(x,y) > T are assumed to be
        foreground.
    """

    # Determine Otsu threshold
    T = threshold_otsu(image, n_bins)

    # Apply Otsu threshold
    image_binary = image > T + T_shift

    return image_binary

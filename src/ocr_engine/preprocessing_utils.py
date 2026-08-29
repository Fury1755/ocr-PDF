"""
Utility module that contains generic helper functions for preprocessing.
"""

import cv2
import numpy as np
import pymupdf
from deskew import determine_skew


def page_to_numpy(page: pymupdf.Page, dpi: int = 300) -> np.ndarray:
    """
    Args:
        page(pymupdf.Page): The individual page of pymupdf's Document object
        dpi(int): The dpi of the numpy array. Set to 300 because that's the office
                    printer's dpi.

    Returns:
        The page's numpy array.
    """

    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY)
    nparray = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)  # pylint: disable=E0602
    return nparray


def deskew_image(img_grey: np.ndarray) -> np.ndarray:
    """
    Uses the deskew library to determine skew angles in a greyscale image.
    Returns a new deskewed numpy array. Skips the deskew if angle is suspicious (>45 degrees)

    Args:
        img_grey(np.ndarray): greyscale image as numpy array
    Returns:
        A new deskewed numpy array
    """

    angle = determine_skew(img_grey)

    if angle is None:
        return img_grey

    if abs(angle) >= 20:
        return img_grey

    h, w = img_grey.shape[:2]
    centre = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(centre, angle, 1.0)

    rotated = cv2.warpAffine(
        img_grey,
        rotation_matrix,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=255,
    )

    return rotated

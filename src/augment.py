# Functions that make barcode images look like bad real-world photos.
# Every function takes an image and a severity between 0 (no change) and 1 (very strong).

import numpy as np
import cv2


def low_light(img, severity):
    # make the image darker and add some camera noise (dark photos are noisy)
    factor = 1 - 0.95 * severity
    dark = img.astype(np.float32) * factor
    noise = np.random.default_rng(0).normal(0, 25 * severity, img.shape)
    return np.clip(dark + noise, 0, 255).astype(np.uint8)


def motion_blur(img, severity):
    # horizontal blur, like when the camera moves
    size = int(1 + severity * 8)
    if size < 2:
        return img.copy()
    kernel = np.zeros((size, size), np.float32)
    kernel[size // 2, :] = 1.0 / size
    return cv2.filter2D(img, -1, kernel)

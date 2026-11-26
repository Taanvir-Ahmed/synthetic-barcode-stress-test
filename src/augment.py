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


def glare(img, severity, seed=None):
    # add a bright white spot, like light reflecting on the label
    rng = np.random.default_rng(seed)
    h, w = img.shape[:2]
    cx, cy = rng.integers(0, w), rng.integers(0, h)
    radius = int(min(h, w) * (0.2 + 0.6 * severity))

    spot = np.zeros((h, w), np.float32)
    cv2.circle(spot, (int(cx), int(cy)), radius, 1.0, -1)
    spot = cv2.GaussianBlur(spot, (0, 0), radius / 2 + 1)

    if img.ndim == 3:
        spot = spot[..., None]
    out = img.astype(np.float32) + spot * 255 * 2 * severity
    return np.clip(out, 0, 255).astype(np.uint8)


def damage(img, severity, seed=None):
    # draw random scratches over the barcode
    rng = np.random.default_rng(seed)
    out = img.copy()
    h, w = img.shape[:2]
    n_lines = int(severity * 15)
    for _ in range(n_lines):
        x1, x2 = rng.integers(0, w, 2)
        y1, y2 = rng.integers(0, h, 2)
        color = int(rng.choice([0, 255]))
        thickness = int(1 + severity * 4)
        cv2.line(out, (int(x1), int(y1)), (int(x2), int(y2)), (color, color, color), thickness)
    return out


EFFECTS = {
    "low_light": low_light,
    "motion_blur": motion_blur,
    "glare": glare,
    "damage": damage,
}

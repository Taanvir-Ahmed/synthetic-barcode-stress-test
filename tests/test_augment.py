import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from augment import EFFECTS, low_light


def make_test_image():
    img = np.full((100, 200, 3), 255, np.uint8)
    img[:, 50:60] = 0
    return img


def test_shape_and_type_stay_same():
    img = make_test_image()
    for name, func in EFFECTS.items():
        out = func(img, 0.5)
        assert out.shape == img.shape, name
        assert out.dtype == np.uint8, name


def test_low_light_makes_image_darker():
    img = make_test_image()
    assert low_light(img, 0.8).mean() < img.mean()


def test_severity_zero_changes_nothing():
    img = make_test_image()
    assert np.array_equal(low_light(img, 0.0), img)

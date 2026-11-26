# Step 3: check image quality and test if the barcode can still be read

import os
import cv2
import pandas as pd
from pyzbar.pyzbar import decode

DATA_DIR = "data/synthetic"
RESULTS_FILE = "results/quality_results.csv"


def sharpness(gray):
    # variance of the Laplacian, lower value = more blurry
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def try_decode(gray):
    found = decode(gray)
    if len(found) > 0:
        return found[0].data.decode("utf-8")
    return ""


def main():
    labels = pd.read_csv(os.path.join(DATA_DIR, "labels.csv"), dtype={"true_value": str})

    brightness, sharp, decoded = [], [], []
    for file in labels["file"]:
        img = cv2.imread(os.path.join(DATA_DIR, file))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness.append(gray.mean())
        sharp.append(sharpness(gray))
        decoded.append(try_decode(gray))

    labels["brightness"] = brightness
    labels["sharpness"] = sharp
    labels["decoded_value"] = decoded
    labels["correct"] = labels["decoded_value"] == labels["true_value"]

    os.makedirs("results", exist_ok=True)
    labels.to_csv(RESULTS_FILE, index=False)

    print("Overall decode rate:", round(labels["correct"].mean(), 3))
    print(labels.groupby(["effect", "severity"])["correct"].mean().unstack().round(2))


if __name__ == "__main__":
    main()

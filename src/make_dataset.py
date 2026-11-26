# Step 2: apply each effect at different severities and save the labels

import os
import csv
import cv2
from augment import EFFECTS

CLEAN_DIR = "data/clean"
OUT_DIR = "data/synthetic"
SEVERITIES = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(os.path.join(CLEAN_DIR, "clean_labels.csv")) as f:
        clean = list(csv.DictReader(f))

    rows = []
    for i, item in enumerate(clean):
        img = cv2.imread(os.path.join(CLEAN_DIR, item["file"]))

        for effect_name, func in EFFECTS.items():
            for sev in SEVERITIES:
                if effect_name in ("glare", "damage"):
                    new_img = func(img, sev, seed=i)
                else:
                    new_img = func(img, sev)

                name = f"{item['file'][:-4]}_{effect_name}_{sev:.1f}.png"
                cv2.imwrite(os.path.join(OUT_DIR, name), new_img)
                rows.append([name, item["true_value"], effect_name, sev])

    with open(os.path.join(OUT_DIR, "labels.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "true_value", "effect", "severity"])
        writer.writerows(rows)

    print(f"Saved {len(rows)} images to {OUT_DIR}")


if __name__ == "__main__":
    main()

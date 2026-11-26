# Step 1: make clean EAN-13 barcode images

import os
import random
import csv
import barcode
from barcode.writer import ImageWriter

OUT_DIR = "data/clean"
N_BARCODES = 100


def random_ean13():
    # EAN-13 needs 12 digits, the library adds the check digit
    return "".join(str(random.randint(0, 9)) for _ in range(12))


def main():
    random.seed(42)
    os.makedirs(OUT_DIR, exist_ok=True)

    rows = []
    for i in range(N_BARCODES):
        code = barcode.get("ean13", random_ean13(), writer=ImageWriter())
        file_name = f"barcode_{i:03d}"
        path = code.save(os.path.join(OUT_DIR, file_name))
        rows.append([os.path.basename(path), code.get_fullcode()])

    with open(os.path.join(OUT_DIR, "clean_labels.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "true_value"])
        writer.writerows(rows)

    print(f"Saved {len(rows)} barcodes to {OUT_DIR}")


if __name__ == "__main__":
    main()

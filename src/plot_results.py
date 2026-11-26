# Step 4: plot decode rate vs severity and save a few example images

import cv2
import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv("results/quality_results.csv")

# decode rate chart
rate = results.groupby(["effect", "severity"])["correct"].mean().unstack(0)
# different line styles because some lines overlap
ax = rate.plot(style=["o-", "s--", "^-", "d:"], figsize=(7, 4.5))
ax.set_xlabel("Severity")
ax.set_ylabel("Decode success rate")
ax.set_title("How often the barcode can still be read")
ax.set_ylim(-0.05, 1.05)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("results/decode_rate.png", dpi=120)
print("saved results/decode_rate.png")

# example grid for barcode 000
effects = ["low_light", "motion_blur", "glare", "damage"]
severities = [0.2, 0.6, 1.0]
fig, axes = plt.subplots(len(effects), len(severities), figsize=(9, 8))
for r, eff in enumerate(effects):
    for c, sev in enumerate(severities):
        img = cv2.imread(f"data/synthetic/barcode_000_{eff}_{sev:.1f}.png")
        axes[r, c].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axes[r, c].set_title(f"{eff}, {sev}", fontsize=9)
        axes[r, c].axis("off")
plt.tight_layout()
plt.savefig("results/sample_grid.png", dpi=100)
print("saved results/sample_grid.png")

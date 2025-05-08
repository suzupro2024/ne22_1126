import os
from main import LABELS, DATA_DIR

for label in LABELS:
    count = len([f for f in os.listdir(DATA_DIR) if f.startswith(label)])
    print(f"{label}: {count} samples")

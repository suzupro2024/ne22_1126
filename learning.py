from main import LABELS, DATA_DIR

from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical


import glob
import numpy as np
import os

X, y = [], []

label_map = {label: idx for idx, label in enumerate(LABELS)}

for file in glob.glob(os.path.join(DATA_DIR, '*.npy')):
    sequence = np.load(file)
    label_name = file.split('/')[-1].split('_')[0]
    X.append(sequence)
    y.append(label_map[label_name])

X = np.array(X)
y = to_categorical(y).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

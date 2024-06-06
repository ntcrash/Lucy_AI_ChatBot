import os
import numpy as np
import cv2
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
# from tensorflow.keras.preprocessing.image import ImageDataGenerator

# pip install opencv-python-headless tensorflow

# Define paths
data_dir = 'path_to_your_dataset'
categories = ['category1', 'category2']  # Update this with your categories

# Load data
data = []
labels = []

for category in categories:
    path = os.path.join(data_dir, category)
    class_num = categories.index(category)
    for img in os.listdir(path):
        try:
            img_array = cv2.imread(os.path.join(path, img))
            resized_array = cv2.resize(img_array, (128, 128))  # Resize to your required dimensions
            data.append(resized_array)
            labels.append(class_num)
        except Exception as e:
            pass

# Convert lists to numpy arrays
data = np.array(data)
labels = np.array(labels)

# Normalize data
data = data / 255.0

# Convert labels to categorical
labels = to_categorical(labels, num_classes=len(categories))

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

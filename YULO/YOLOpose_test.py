from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy

# Load a model
model = YOLO('yolov8n-pose.pt')  # load an official model  # load a custom model

# Predict with the model
results = model.predict('./data/perspective_transform.png',conf=0.1)  # predict on an image

res_plot = results[0].plot()
plt.imshow(res_plot)
plt.show()

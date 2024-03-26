import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n-pose.pt')  # load an official model  # load a custom model

# Predict with the model
image = cv2.imread('./data/perspective_transform.png')
# 이미지를 3x3 그리드로 등분
rows = 3
cols = 3
# 이미지를 위아래로 3등분하여 저장하는 코드
height, width, _ = image.shape

# 3x3 그리드로 이미지를 등분
images = []
for r in range(rows):
    for c in range(cols):
        # 이미지를 3x3 그리드로 등분
        image_part = image[r * height // rows:(r + 1) * height // rows, c * width // cols:(c + 1) * width // cols, :]
        # 이미지 확대
        image_part = cv2.resize(image_part, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        images.append(image_part)

# 각 이미지에 대해 모델 예측 수행
results = [model.predict(img) for img in images]

# 출력 창 크기 조절
plt.figure(figsize=(12, 12))

# 각 부분에 대한 출력 표시
for i, result in enumerate(results):
    plt.subplot(rows, cols, i + 1)
    plt.imshow(result[0].plot())
    plt.title(f'Part {i+1}')
    plt.axis('off')

plt.show()

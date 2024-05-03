from ultralytics import YOLO

model = YOLO('yolov8n-pose.pt')  # 사용자 지정 훈련 모델을 불러오기

# 모델을 내보내기
model.export(format='onnx')
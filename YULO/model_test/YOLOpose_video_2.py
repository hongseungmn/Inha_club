#라이브러리 import 
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
from ultralytics import YOLO


from fastapi.middleware.cors import CORSMiddleware

# FastAPI 앱 인스턴스 생성
app = FastAPI()
model = YOLO('yolov8n.pt')
model.classes = [0]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 허용
    allow_methods=["GET", "POST", "OPTIONS"],  # 허용할 메서드 지정
    allow_headers=["*"],  # 허용할 헤더 지정
)

def get_stream_video():
    # camera 정의
    cam = cv2.VideoCapture(0)

    while True:
        # 카메라 값 불러오기
        success, frame = cam.read()

        if not success:
            break
        else:
            results = model(frame,verbose=False, classes=[0])
            names = model.names
            count = 0
            for r in results:
                for c in r.boxes.cls:
                    count+= 1
                    print(names[int(c)])
                    
            print(count)
            ret, buffer = cv2.imencode('.jpg', results[0].plot())
            if ret:
              frame = buffer.tobytes()
              yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' +
                  frame + b'\r\n')
            else:
            # yield로 하나씩 넘겨준다.
              frame = buffer.tobytes()
              yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(frame) + b'\r\n')
        




@app.get('/get_url')
def get_url():
  return {
    "url":"http://127.0.0.1:8000/video"
  }
  
  
def video_streaming():
  return get_stream_video()
  
@app.get('/video')
def main():
    #StringResponse 함수를 return하고,
    #인자로 OpenCV에서 가져온 "바이트"이미지와 type을 명시
    return StreamingResponse(video_streaming(), media_type="multipart/x-mixed-replace; boundary=frame")
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from cv2 import get_stream_video

app = FastAPI()

def video_streaming():
  return get_stream_video()

@app.get("/video")
def main():
  return StreamingResponse(video_streaming(), media_type="multipart/x-mixed-replace; boundary=frame")
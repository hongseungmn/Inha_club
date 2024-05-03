
from av import VideoFrame
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription

class VideoTransformTrack(MediaStreamTrack):
  kind = "video"
  
  def __init__(self, track, transform):
    super().__init__()
    self.track = track;
    self.transform = transform
    
  async def recv(self):
    frame = await self.track.recv()
    if self.transform == "smoke":
      img = frame.to_ndarray(format="bgr24")
      new_frame = VideoFrame.from_ndarray(img, format="bgr24")
      return new_frame


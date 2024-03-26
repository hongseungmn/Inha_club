import cv2

cap = cv2.VideoCapture(0)

if cap.isOpened():
  fps = cap.get(cv2.CAP_PROP_FPS)
  f_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
  f_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
  f_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
  
  print('Frames per second : ', fps, 'FPS')
  print('Frame count : ', f_count)
  print('Frame width : ', f_width)
  print('Frame height : ',f_height)
  
  while cap.isOpened():
    ret, frame = cap.read()
    re_frame = cv2.resize(frame, (round(f_width/4), round(f_height/4)))
    cv2.imshow('Car_Video', re_frame)
    key = cv2.waitKey(30)
    if key == ord('q'):
      break;

cap.release()
cv2.destroyAllWindows()

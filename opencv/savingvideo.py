import cv2
import numpy as np

cap = cv2.VideoCapture(0)

fmt = cv2.VideoWriter_fourcc('m','p','4','v') # MPEG-4
fps = 20.0 # 20이 적당한 fps인듯
size = (640, 360)
writer = cv2.VideoWriter('test.m4v', fmt, # mp4v 
                        fps, size)

while True:
    _, frame = cap.read() # 이미지 읽어들이기
    
    frame = cv2.resize( frame, size ) # 이미지를 축소
    writer.write(frame) # 이미지 출력
    print(frame)
    cv2.imshow( 'frame', frame ) # 화면출력

    if cv2.waitKey(1) == 13: break
writer.release()
cap.release() # 카메라 해제
cv2.destroyAllWindows() # 윈도우 제거
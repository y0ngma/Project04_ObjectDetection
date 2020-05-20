# cd repository/project04_objectdetection/opencv
import numpy as np
import cv2

cap = cv2.VideoCapture(0) # 웹 카메라로부터 입력받기
while True:
    _, frame = cap.read() # 이미지 읽어 들이기
    
    frame = cv2.resize(frame, (480,360)) # 이미지를 축소
    frame[:,:,0] = 0 # BGR에서 파란색을 0으로
    frame[:,:,1] = 0 # 녹색을 0으로
    
    cv2.imshow('openCV Web Camera', frame) # 위도우에 이미지 출력
    k = cv2.waitKey(1)
    if k ==27 or k == 13:break # ESC(27)/ENTER(13)가 입력되면 반복종료

cap.release() # 카메라 해제
cv2.destroyAllWindows() # 윈도우 제거
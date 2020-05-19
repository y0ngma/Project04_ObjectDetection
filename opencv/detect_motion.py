import cv2
import numpy as np
# import imutils
# contours = contours[1] if imutils.is_cv3() else contours[0]

cap = cv2.VideoCapture(0) # 웹 카메라로부터 입력받기
img_last = None # 이전 프레임을 저장해 둘 변수(초기화)
green = (0,255,0)

while True:
    _, frame = cap.read() # 이미지 읽어들이기
    
    frame = cv2.resize( frame, (500,300) ) # 이미지를 축소
    gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY ) # 흑백으로 변화
    gray = cv2.GaussianBlur( gray, (9,9), 0 ) # 블러처리
    img_b = cv2.threshold( gray, 100, 255, cv2.THRESH_BINARY )[1]# 이진화

    if img_last is None: # 차이확인하기
        img_last = img_b
        continue
    frame_diff = cv2.absdiff( img_last, img_b )

    # find the contours (continuous blobs of pixels) the image
    contours = cv2.findContours( frame_diff,
                    cv2.RETR_EXTERNAL, # 윤곽추출
                    cv2.CHAIN_APPROX_SIMPLE)[1]
    # contours = contours[0]

    for contour in contours: # 차이있는부분 출력
        (x,y,w,h) = cv2.boundingRect(contour)
        if w < 30: continue # 작은변경은 무시하기
        cv2.rectangle( frame, (x, y), (x+w, y+h), green, 2 ) # 녹색사각 렌더링
    
    img_last = img_b # 프레임을 변수에 저장해두기
    cv2.imshow( 'Diff Camera', frame      ) # 화면출력
    cv2.imshow( 'diff data',   frame_diff )

    if cv2.waitKey(1) == 13: break
cap.release() # 카메라 해제
cv2.destroyAllWindows() # 윈도우 제거
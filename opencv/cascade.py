# https://github.com/opencv/opencv/tree/master/data/haarcascades
# 정면얼굴검출용 haarcascade_frontalface_alt.xml
###################################
# 얼굴검출과정 확인하기
#%%
import matplotlib.pyplot as plt
import cv2
# %%
path = '../data/'
# 케스케이드 파일 지정해서 검출기 생성하기
cascade_file = path+'haarcascade_frontalface_alt.xml'
cascade = cv2.CascadeClassifier(cascade_file)
cascade
# 이미지 읽어 들이고 흑백변환
# img = cv2.imread(path+'jennie_eye.jpg')
img = cv2.imread('..\data\jennie_eye.jpg')
type(img)
#%%
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# %%
# 얼굴인식하기
face_list = cascade.detectMultiScale(img_gray, minSize=(150,150))
# 결과 확인하기
if len(face_list)==0:
    print('failed')
    quit()

# %%
# 인식한 부분표시하기
for (x,y,w,h) in face_list:
    print('얼굴의좌표=', x,y,w,h)
    red = (0,0,255)
    cv2.rectangle(img, (x,y), (x+w, y+h), red, thickness=20)

# %%
# 이미지 출력하기
cv2.imwrite('face-detect.png', img)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
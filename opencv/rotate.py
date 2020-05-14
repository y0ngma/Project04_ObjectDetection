#%%
import matplotlib.pyplot as plt
import cv2

base_path = 'C:/Repository/Project04_ObjectDetection/data/'
img = cv2.imread(base_path + 'hong.png')
print(type(img))

# %%
# 원래이미지를 왼쪽에 출력하기
plt.subplot(1,2,1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# 좌우 반전
plt.subplot(1,2,2)
img_flip = cv2.flip(img, 1)
plt.imshow(cv2.cvtColor(img_flip, cv2.COLOR_BGR2RGB))
plt.show()
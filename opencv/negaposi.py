#%%
import matplotlib.pyplot as plt
import cv2
import os

base_path = 'C:/Repository/Project04_ObjectDetection/data/'
img = cv2.imread(base_path + 'hong.png')
print(type(img))

# %%
plt.imshow(img)
plt.show()
# %%
# 네거티브-포지티브 반전
img_nega = 255-img
plt.imshow(cv2.cvtColor(img_nega, cv2.COLOR_BGR2RGB))
plt.show

# %%
# 흑백 색공간 변환
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.imshow(img, cmap='gray')
plt.axis('off')
plt.show()

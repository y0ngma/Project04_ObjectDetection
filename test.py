# from keras.applications.vgg16 import VGG16
# model = VGG16()
# print(model.summary())

from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
import cv2, numpy as np

from keras.applications.mobilenet import MobileNet, decode_predictions

import cv2
import time 
from matplotlib import pyplot as plt

mobile = MobileNet()
# mobile.summary()

img = cv2.imread('bird1.jpg', -1)
img = cv2.resize(img, (224, 224))

start = time.time() 
yhat = mobile.predict(img.reshape(-1, 224, 224, 3))
time = time.time() - start
# label_key = np.argmax(yhat)
label = decode_predictions(yhat)
label = label[0][0]

print("테스트 시 소요 시간 : {}".format(time))
print('%s (%.2f%%)' % (label[1], label[2]*100))
img = img[:,:,::-1]
plt.figure(figsize=(11,11))
plt.imshow(img)
plt.axis("off")
plt.show()

# from keras.applications.mobilenetv2 import MobileNetV2, decode_predictions

# mobilev2 = MobileNetV2()
# mobilev2.sumary()
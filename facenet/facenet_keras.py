# 케라스 FaceNet 모델 로드 예시
from keras.models import load_model


# 모델 불러오기
model = load_model('facenet_keras.h5')
# 입력과 출력 배열 형태 요약
print(model.inputs)
print(model.outputs)
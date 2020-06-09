# Project04_ObjectDetection

## FaceNet
- MTCNN
- ResNet
    - Residual block에 Batch Normalization(BN) 사용
    - Conv-BN-ReLU 순으로 배치(순서에따라 성능 차이 유의)
- VGG_Face
    - pre-train model
## 환경구축
- Docker django
    - 가상화 머신 보다 좀더 경량화된 방식
    - 게스트 OS를 설치하지 않아도 됨
    - 서버운영에 필요한 프로그램과 라이브러리만 격리해서 설치할 수 있고, os 자원은 호스트와 공유. 
    - 이미지 용량이 적음
    - 가상화 레이어가 없기 때문에 파일시스템, 네트워크 속도도 가상머신에 비해 월등히 빠름. 호스트와 거의 동일
    - 가상머신과 달리 이미지 생성과 배포에 특화된 기능제공(버전관리 포함)
    - 제공되는 다양한 API 으로 원하는 만큼 자동화가능. 개발과 서버운영에 융용.

- CUDA
- PostgreSQL
- 
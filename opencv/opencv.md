# 도커 우분투에서 opencv 사용하기
## import cv2 안될때
- 다음과 같은 문구가 뜬다면
    - `ImportError: libSM.so.6: cannot open shared object file: No such file or directory`
    ```py
    # 필요시, 먼저 설치를 원하는 가상환경으로 진입해야 한다
    # conda activate 가상환경명
    apt-get update
    apt-get install -y libsm6 libxext6 libxrender-dev
    pip install opencv-python
    ```
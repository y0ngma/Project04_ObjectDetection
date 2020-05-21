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

## 설치
1. 우분투 16.04
1. CUDA, CUDNN 설치
1. openCV

    ```py
    # 소프트웨어 및 라이브러리 갱신
    sudo apt-get update
    
    # 운영체제 업그레이드
    sudo apt-get upgrade
    
    # 소프트웨어 컴파일
    sudo apt-get install build-essential
    
    # CV 선행요건 파일설치
    sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
    
    # CV 선행요건 파일설치
    sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
    
    # directory
    sudo mkdir ~/opencv
    cd ~/opencv
    
    # git clone
    sudo git clone https://github.com/opencv/opencv.git
    sudo git clone https://github.com/opencv/opencv_contrib.git
    
    # dir
    sudo mkdir ~/opencv/build
    cd ~/opencv/build
    
    # 빌드 폴더위치에 있으면 이 명령을 실행하라. 약간의 시간이 걸릴 수 있다. 오류 없이 이 명령이 실행되면 다음 단계로 진행하라
    sudo cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D INSTALL_C_EXAMPLES=ON \
        -D INSTALL_PYTHON_EXAMPLES=ON \
        -D WITH_TBB=ON \
        -D WITH_V4L=ON \
        -D WITH_QT=on \
        -D WITH_OPENGL=ON \
        -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
        -D BULID_EXAMPLES=ON /home/team/opencv/opencv
        #-D BULID_EXAMPLES=ON ..
    
    # 다음 명령으로 CPU 코어갯수 확인
    nproc
    
    # 코어갯수를 알면 멀티 스레딩을 처리하는데 사용가능. 4개로 설정하면 4개의 스레드가 실행되고 있음을 의미. 이 명령은 다음과 같고, 명령을 내리면 openCV용 C로 작성된 모든 클래스가 컴파일된다
    make -j4
    
    # 이제 OpenCV를 실제로 설치하려면 다음 명령을 실행하라
    sudo make install
    
    # 구성파일에 경로를 추가하라
    sudo sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf'
    
    # 다음 명령을 사용해 올바른 구성을 확인하라
    sudo ldconfig
    
    # 성공적으로 설치하면 이 라이브러리를 사용해 실시간 비디오를 스트리밍할 수 있다. 이제 기준모델을 구축하기 시작해보자.
    ```
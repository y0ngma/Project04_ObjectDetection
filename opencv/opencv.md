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


# 전처리부터 분류까지
## Labeled Faces in the Wild
1. LFW 경로 맞추기
    - 다음과 같은 경로에 모델압축을 푼다
        ```py
        models
        L facenet
            L 20180402-114759.zip
            L 20180402-114759
                L 20180402-114759.pb
                L model-20180402-114759.ckpt-275.data-00000-of-00001
                L model-20180402-114759.ckpt-275.index
                L model-20180402-114759.meta

        mkdir -p /root/models/facenet
        # 도커컨테이너밖 터미널에서 윈도우로컬의 파일을
        # 도커컨테이너안 우분투 목표경로에 압축파일 옮겨놓기
        docker cp C:/Users/admin/Downloads/20180402-114759.zip \
                    ubuntu1:/root/models/facenet
        # 목표경로에 이동하여 압축풀기
        cd /root/models/facenet
        apt-get update
        apt-get install zip unzi
        unzip 20180402-114759.zip
        ```

1. LFW 전처리 하기
    - 로우데이터를 전처리하여 lfw_mtcnnpy_160 폴더에 넣기
        ```py
        python src/align/align_dataset_mtcnn.py \ 
        /root/datasets/lfw/raw \
        ~/datasets/lfw/lfw_mtcnnpy_160 \
        --image_size 160 \
        --margin 32 \
        --random_order \
        --gpu_memory_fraction 0.25 \
        ```

1. LFW 분류기 생성
    - 전처리 된걸로 분류기 피클생성 
        ```py
        # 경로이동
        cd /root/repository/facenet0
        # 실행
        python src/classifier.py TRAIN \
        ~/datasets/lfw/lfw_mtcnnpy_160 \
        ~/models/facenet/20180402-114759/model-20180402-114759.pb \
        ~/models/facenet/my_classifier.pkl \
        --batch_size 1000 --min_nrof_images_per_class 40 \ 
        --nrof_train_images_per_class 35 --use_split_dataset
        ```

## 개인데이터로
1. my_datasets 경로 맞히기
    - 다음과 같은 경로를 생성한다
        ```
        datasets
            L my_datasets
                L star
                    L raw
                    L star_mtcnnpy_160

        mkdir -p /root/datasets/my_datasets/star/raw \
                 /root/datasets/my_datasets/star/star_mtcnn_160

        docker cp C:/Users/admin/Downloads/img_test.zip \
                    ubuntu1:/root/datasets/my_datasets/star/raw
        ```

1. 모델훈련용 데이터 전처리
    - ~raw/Train 전처리하여 star_mtcnnpy_160/Train 폴더에 넣기
        ```py
        # 경로이동
        cd /root/repository/facenet0
        conda activate facenet0

        # 인풋~/Train에 담긴 이름별 폴더의 데이터셋을 전처리해서
        # 아웃풋~/Train에 이름별로 담기
        python src/align/align_dataset_mtcnn.py /root/datasets/my_datasets/star/raw/Train ~/datasets/my_datasets/star/star_mtcnnpy_160/Train \
        --image_size 160 \
        --margin 32 \
        --random_order \
        --gpu_memory_fraction 0.25
        ```
1. 분류용 검증데이터 전처리하기
    - ~raw/Test 전처리하여 star_mtcnnpy_160/Test 폴더에 넣기
        ```py
        python src/align/align_dataset_mtcnn.py /root/datasets/my_datasets/star/raw/Test ~/datasets/my_datasets/star/star_mtcnnpy_160/Test \
        --image_size 160 \
        --margin 32 \
        --random_order \
        --gpu_memory_fraction 0.25
        ```
1. 전처리된 훈련데이터로 분류기 생성하기
    - 전처리 된걸로 분류기 피클생성 
        ```py
        python src/classifier.py TRAIN \
        ~/datasets/my_datasets/star/star_mtcnnpy_160/Train \
        ~/models/facenet/20180402-114759/20180402-114759.pb \
        ~/models/facenet/my_classifier20p.pkl
        --batch_size 1000 
        
        --min_nrof_images_per_class 40 \ 
        --nrof_train_images_per_class 35 --use_split_dataset
        ```

1. 전처리된 검증데이터를 분류하기
    - 분류
        ```py
        # 경로이동
        cd /root/repository/facenet0

        python src/classifier.py CLASSIFY \
        ~/datasets/my_datasets/star/star_mtcnnpy_160/Test \
        ~/models/facenet/20180402-114759/20180402-114759.pb \
        ~/models/facenet/my_classifier20p.pkl --batch_size 1000

        # 분류기 넣는 폴더에 미리 생성된 분류기 붙여넣기법은 다음과 같다
        docker cp C:/Users/admin/Downloads/my_classifier20p.pkl \
                    ubuntu1:/root/models/facenet
        ```

## 정리
- 정확도 acc = float(tp+tn) / dist.size
    ```py
    def calculate_accuracy(threshold, dist, actual_issame):
        predict_issame = np.less(dist, threshold)
        tp = np.sum(np.logical_and(predict_issame, actual_issame))
        fp = np.sum(np.logical_and(predict_issame, np.logical_not(actual_issame)))
        tn = np.sum(np.logical_and(np.logical_not(predict_issame), np.logical_not(actual_issame)))
        fn = np.sum(np.logical_and(np.logical_not(predict_issame), actual_issame))
    
        tpr = 0 if (tp+fn==0) else float(tp) / float(tp+fn)
        fpr = 0 if (fp+tn==0) else float(fp) / float(fp+tn)
        acc = float(tp+tn)/dist.size
        return tpr, fpr, acc
    ```
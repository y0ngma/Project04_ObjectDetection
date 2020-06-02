# 2020-05-27 Unknown과 Accuracy 영상에 출력되도록 수정
# 2020-06-01 DB에 적재중
import align.detect_face
import argparse
import sys
import time
import cv2
import face # Original
# import contributed.face # Modified
import psycopg2
import random
import estimate, UI
from functions import *
import os


base_path = '/'.join((os.getcwd()).split('/')[:4])+'/' #/home/team/facenet_master/ 
upload_path = 'project04_objectdetection/data/'
download_path = 'data/images/'
print( '='*80,'\n',"기본경로-> ",base_path," 적재할 파일의 경로 :",upload_path," 다운받을 로컬 경로 :",download_path )

input_path  = base_path + upload_path
output_path = base_path + download_path


# main 함수 내에서 영상 출력 중에 Bounding Box, name, Accuracy 등을 출력하는 함수
def add_overlays(frame, faces, frame_rate):
    if faces:
        # Detecting된 얼굴들 정보가 Class 객체로 담겨 있는 리스트를 for iterator로 출력한다
        for i, face in enumerate(faces):
            # 정확도가 0.8 이상인 경우에 color 정의
            color = ( 255, 0, 0 ) # Modified
            face_bb = face.bounding_box.astype(int)
            # Bounding Box를 출력
            cv2.rectangle(frame,
                        (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                        (0, 255, 0), 2)
            # 얼굴의 정확도가 0.8 이하인 경우 아래와 같이 정의한다
            if face.accuracy < 0.8 :  
                face.name = "Unknown" # Modified
                color = ( 0, 0, 255 ) # Modified

            # 얼굴 이름, 정확도를 Text로 영상에 출력하는 함수
            cv2.putText(frame, face.name, (face_bb[0], face_bb[3]),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                        thickness=2, lineType=2)
            cv2.putText(frame, str(round(face.accuracy,2)*100)+"%", (face_bb[0], face_bb[3]-30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                        thickness=2, lineType=4) # Modified
    # 프레임 수를 출력하는 함수
    cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)

# main 함수
def main(args):
    # face detection이 실행될 때 프레임의 수 정의
    frame_interval = 5  # Number of frames after which to run face detection 
    # fps가 출력되는 interval
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0
    
    # Opencv함수로 영상 정의
    video_capture = cv2.VideoCapture(0)
    # face.Recognition() 클래스 정의
    face_recognition = face.Recognition()
    # 시작시간 정의
    start_time = time.time()
    if args.debug:
        print("Debug enabled")
        face.debug = True

    # 영상이 돌기 시작
    while True:
        # Capture frame-by-frame
        # 영상을 읽은 프레임 별로 ret, frame에 정의
        ret, frame = video_capture.read()
    
        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)
            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0
        print( 'number of face', len(faces) ) # Modified
        # frame, faces, frame_rate를 overlay하기 위해 변수를 담아준다
        add_overlays(frame, faces, frame_rate)
        frame_count += 1
        # frame 출력
        cv2.imshow('Video', frame)
        ## 키 입력하거나 구매를 완료시 break한다
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #######################################################
    ###### 조작패널 : 결제대용으로 키보드나 웹버튼 이용 ######
    #######################################################
        """ to do list :
        1. DB에 실시간 예측값 customers 테이블에 적재( 옵션 : 임베딩얼굴값을 키값으로 )
        2. items의 구매내역을 적재 및 구매한 회원과 연결 ( 1 customer vs 다수 item 연결 )
        3. 두 작업을 버튼하나로 통합 및 items 테이블에 타임스탬프 생성
            3.1 시간형식 설정 https://www.postgresqltutorial.com/postgresql-time/
            3.2 타임스탬프 자동생성 https://x-team.com/blog/automatic-timestamps-with-postgresql/
        4. main()실행시 세션연결 autocommit으로 자동 DB커밋 구현 및 close(구매완료시) 
        5. DB에 회원정보 수정 update_customer()
            5.1 회원가입(약관동의 버튼)누르면 사진 캡쳐 및 업로드
            5.2 저장된 예측값 대신 직접입력 할 수 있는 칸이나 팝업창구현
            5.3 그 입력값으로 DB에 insert/update_customer()
            5.4 단, 이름이나 폰번호로 회원을 구분하는게 아니라 얼굴피쳐맵으로
        6. 상기 실시간 DB연동 구축되면 더미데이터 대량적재 copy()이용
            https://hakibenita.com/fast-load-data-python-postgresql#copy
        7. 분석
        """
        ## 회원입력
        if cv2.waitKey(1) & 0xFF == ord('i'):
            customer_age, customer_gender = estimate.age_gender()
            insert_customer(customer_age, customer_gender)
        ## 결제 : customer_id와 item_id를 연결
        if cv2.waitKey(1) & 0xFF == ord('a'):
            item_name, item_producer, item_group, item_price = UI.purchase()
            add_item(item_name, item_producer, item_group, item_price, customer_list)
        ## DB예측된 값을 사용자가 수정
        # 웹상에서 팝업창 띄우거나 예측된값 옆에 수정버튼 구비
        if cv2.waitKey(1) & 0xFF == ord('u'):
            customer_age, customer_gender, customer_id = UI.register(customer_id)
            update_customer(customer_id, customer_age, customer_gender)
        ## 이미지 캡쳐하고 (로컬저장후) DB적재
        # 이미지 캡쳐하는것 추가필요
        if cv2.waitKey(1) & 0xFF == ord('d'):
            write_blob(1, input_path+'hong.jpeg', 'jpeg')
            write_blob(2, input_path+'jennie_makeup.jpg', 'jpg')

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true',
                        help='Enable some debug outputs.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    # main(parse_arguments(sys.argv[1:]))

# 열결된 db 정보
    connect()
# DB
    create_tables()

## 회원입력
    customer_age, customer_gender = estimate.age_gender()
    for i in range(10):
        insert_customer(customer_age+int(i), customer_gender)
## customer_id와 item_id를 연결
    item_name, item_producer, item_group, item_price = UI.purchase()
    customer_list = (1, 2)
    add_item(item_name, item_producer, item_group, item_price, customer_list)
## DB예측된 값을 사용자가 수정
# 웹상에서 팝업창 띄우거나 예측된값 옆에 수정버튼 구비
    # customer_age, customer_gender, customer_id = UI.register()
    # update_customer(customer_id, customer_age, customer_gender)
## 이미지 캡쳐하고 (로컬저장후) DB적재
# 이미지 캡쳐하는것 추가필요
    # write_blob(1, input_path+'hong.jpeg', 'jpeg')
    # write_blob(2, input_path+'jennie_makeup.jpg', 'jpg')


# # 나이 성별 예측목록 통째 입력
#     insert_customer_list([ (29,1), (35,0) ])

# https://hakibenita.com/django-group-by-sql
# # customer_id 가 1인 사람의 item를 가져오기
#     get_items(1)

# # id인덱스 리셋시 참고할 시퀸스명
#     sequences()

# # 적재된 이미지 불러와 로컬에 저장 
#     read_blob( 1, output_path )
            

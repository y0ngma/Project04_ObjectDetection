# 장고 모듈 import
from django.shortcuts import render, redirect
from django.http import HttpResponse,StreamingHttpResponse
from django.views.decorators import gzip
from django.views.decorators.csrf import csrf_exempt
# 얼굴인식 모듈 import
import cv2
import time
import numpy as np
# from . import face
# Database 모듈 import 및 접속 설정
import psycopg2
import estimate, UI
from functions import *

# conn_string = "host='192.168.0.59' dbname ='postgres' user='user' password='password'"
# conn = psycopg2.connect(conn_string)
# cur = conn.cursor()
face_lists = list()

# 카메라 인식 Class - fps 부분은 삭제
class VideoCamera(object):
    def __init__(self):
        # 얼굴인식 관련 멤버변수 설정
        self.frame_interval = 5  # Number of frames after which to run face detection 
        self.fps_display_interval = 20  # seconds
        self.frame_count = 0
        self.face_recognition = face.Recognition()
        self.start_time = time.time()
        # self.face_lists
        self.trigger = 0

        # 라즈베리 파이 카메라 모듈로 촬영된 스트리밍(mjpg-streamer)을 가져온다.
        self.video = cv2.VideoCapture('http://192.168.0.101:8091/?action=stream')


    def __del__(self):
        self.video.release()

    # 바인딩 박스 추가하는 메소드
    def add_overlays(self, frame, faces, trigger=0):
        if faces is not None:
            for i, face in enumerate(faces):
                face_bb = face.bounding_box.astype(int) # 사각형 좌표 리스트
                cv2.rectangle(frame, # 이미지
                            (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]), # 시작좌표, 종료좌표
                            (63, 28, 1), 2) # 색상(B, G, R), 두께 pixel

                if face.name is not None:
                    cv2.putText(frame, face.name, (face_bb[0], face_bb[3]),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (165, 123, 18),
                                thickness=2, lineType=2)

                    ## 정확도 막대 구현
                    # x1,y1,x2,y2 = face_bb[0], face_bb[1], face_bb[2], face_bb[3]
                    bar_height_origin = face_bb[3] - face_bb[1]
                    acc = round(face.accuracy,2)
                    bar_height = int(bar_height_origin * acc)
                    # print("bar_height_origin : ", bar_height_origin)
                    # print("acc : ", acc)
                    # print("bar_height : ", bar_height)
                    # print("pt1=(face_bb[2], face_bb[3]+bar_height)", (face_bb[2], face_bb[3]+bar_height) )
                    # print("pt2=(face_bb[2]+10, face_bb[3])", (face_bb[2]+10, face_bb[3]) )
                    cv2.rectangle(img=frame, pt1=(face_bb[2], face_bb[3]-bar_height), pt2=(face_bb[2]+7, face_bb[3]), color=(63, 28, 1), thickness=7) 

                    cv2.putText(frame, str(round(face.accuracy,2)*100)+"%", (face_bb[0], face_bb[3]-30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (38, 165, 101),
                                thickness=2, lineType=4)

    # 프레임을 가져오는 메소드
    def get_frame(self, trigger=0):
        ret,frame = self.video.read()
        frame = cv2.flip(frame,0) # 상하반전
        global face_lists
        # 가져온 프레임에서 얼굴 id 인식 - 설정된 interval 마다 수행
        if (self.frame_count % self.frame_interval) == 0:
            face_lists = self.face_recognition.identify(frame)

        #
        self.add_overlays(frame, face_lists)
        self.frame_count += 1
        ######
        ret,jpeg = cv2.imencode('.jpg',frame)
        return jpeg.tobytes(), 0
    
    def capture(self, faces):
        if faces is not None:
            for i, face in enumerate(faces):
                # ### 이미지 캡쳐 시작
                print(face.name)
                time_st = time.strftime("%Y%m%d_%H%M%S")
                cap_name = './capture/{}_{}.png'.format(face.name, time_st)
                cv2.imwrite(cap_name, face.image)                
        return face.name


def gen(camera):
    while True:
        frame = camera.get_frame()[0]
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        yield camera.get_frame()[1]


@gzip.gzip_page
def stream(request): 
    try:
        return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")

@csrf_exempt
def caps(request):
    if request.method == 'POST':
        if face_lists == []:
            pass
        else:
            print(face_lists)
            print(face_lists[0])
            print(face_lists[0].name)

    return HttpResponse(face_lists[0].name)


def service(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    # elif request.method == 'POST':
    #     return redirect('/face/capture')
    # name='Jang Won1'
    # age=36
    # gender=0
    # image=1 
    if request.method == 'POST':
        print(face_lists)
        # print(face_lists[0].name)


    # return render(request, 'index.html', context={'name':name, 'age':age, 'gender':gender, 'image' : image })


@csrf_exempt
def join1():
    # if request.method == "GET":
        # return render(request, 'index.html')
    # elif request.method == "POST":
    # connect()
    # create_tables()
    customer_age, customer_gender = estimate.age_gender()
    if cv2.waitKey(1) & 0xFF == ord('i'):
        insert_customer(customer_age, customer_gender)
        # sql = """INSERT INTO customers(customer_age, customer_gender)
        #      VALUES(%s,%s) RETURNING customer_id;"""
        # cur.execute(sql, (customer_age, customer_gender))
        # # customer_id = cur.fetchone()[0]
        # # print('추가', customer_id)
        # conn.commit()
        # cur.close()
        # return customer_id

    # # return render(request, 'index.html', context={'name':name, 'age':age, 'gender':gender, 'image' : image })


def test():
    cap = cv2.VideoCapture(0) # 웹 카메라로부터 입력받기
    while True:
        _, frame = cap.read() # 이미지 읽어 들이기
        frame = cv2.resize(frame, (480,360)) # 이미지를 축소
        frame[:,:,0] = 0 # BGR에서 파란색을 0으로
        frame[:,:,1] = 0 # 녹색을 0으로
        cv2.imshow('openCV Web Camera', frame) # 위도우에 이미지 출력
        k = cv2.waitKey(1)        

            #######################################################
            ###### 조작패널 : 결제대용으로 키보드나 웹버튼 이용 ######
            #######################################################
            # """ to do list :
            # 1. DB에 실시간 예측값 customers 테이블에 적재( 옵션 : 임베딩얼굴값을 키값으로 )
            # 2. items의 구매내역을 적재 및 구매한 회원과 연결 ( 1 customer vs 다수 item 연결 )
            # 3. 두 작업을 버튼하나로 통합 및 items 테이블에 타임스탬프 생성
            #     3.1 시간형식 설정        https://www.postgresqltutorial.com/postgresql-time/
            #     3.2 타임스탬프 자동생성  https://x-team.com/blog/automatic-timestamps-with-postgresql/
            # 4. main()실행시 세션연결 autocommit으로 자동 DB커밋 구현 및 close(구매완료시) 
            # 5. DB에 회원정보 수정 update_customer()
            #     5.1 회원가입(약관동의 버튼)누르면 사진 캡쳐 및 업로드
            #     5.2 저장된 예측값 대신 직접입력 할 수 있는 칸이나 팝업창구현
            #     5.3 그 입력값으로 DB에 insert/update_customer()
            #     5.4 단, 이름이나 폰번호로 회원을 구분하는게 아니라 얼굴피쳐맵으로
            # 6. 상기 실시간 DB연동 구축되면 더미데이터.txt 대량적재 copy()이용
            #         https://hakibenita.com/fast-load-data-python-postgresql#copy
            # 7. 분석
            # """
        
        customer_age, customer_gender = estimate.age_gender()
    # 회원입력
        if cv2.waitKey(1) & 0xFF == ord('i'):
            insert_customer(customer_age, customer_gender)
    # 물품 입력
        if cv2.waitKey(1) & 0xFF == ord('o'):
            insert_item = """INSERT INTO items(item_name, item_producer, item_group, item_price) 
                    VALUES(%s,%s,%s,%s) RETURNING item_id;"""
            cur.execute(insert_item, (item_name, item_producer, item_group, item_price))
            item_id = cur.fetchone()[0]
            cur.execute(assign_customer, (customer_id, item_id))
            conn.commit()

    ## 결제 : customer_id와 item_id를 연결
        if cv2.waitKey(1) & 0xFF == ord('a'):
            item_name, item_producer, item_group, item_price = UI.purchase()
            add_item(item_name, item_producer, item_group, item_price, customer_id)
    ## 이미지 캡쳐하고 (로컬저장후) DB적재
        # 이미지 캡쳐하는것 추가필요
        if cv2.waitKey(1) & 0xFF == ord('d'):
            write_blob(1, input_path+'hong.jpeg', 'jpeg')
            write_blob(2, input_path+'jennie_makeup.jpg', 'jpg')

    ## DB예측된 값을 사용자가 수정
        # # 웹상에서 팝업창 띄우거나 예측된값 옆에 수정버튼 구비
        # if cv2.waitKey(1) & 0xFF == ord('u'):
        #     customer_id = 수정할 사람
        #     customer_age, customer_gender, customer_id = UI.register(customer_id)
        #     update_customer(customer_id, customer_age, customer_gender)
       
        if k ==27 or k == 13:break # ESC(27)/ENTER(13)가 입력되면 반복종료

    cap.release() # 카메라 해제
    cv2.destroyAllWindows() # 윈도우 제거


test()
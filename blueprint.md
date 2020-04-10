
# 


## 1.Planning

비즈니스문제|분석문제
--|--
고객이탈증대|이탈에 영향미치는 요인식별, 이탈가능성 예측
예상치 않은 설비장애로 인한 판매량 감소| 설비의 장애를 이끄는 신호를 감지하여<br> 설비장애요인으로 식별하고,<br> 장애발생시점 및 가능성 예측
기존 판매정보 기반 영업사원의<br> 판단시 재고관리 및 적정가격 판매어려움|내부판매 정보외의 수요예측을 수행할 수 있는<br> 인자의 추출 및 모델링을 통한 수요예측 
### 비즈니스 도메인 이해하기
### 프로젝트 목표정의 하기
### 데이터 이해하기
### 평가 기준정의
### 위험관리 계획
### 프로젝트 계획수립

## 2.Data preparing
- Data Acquirement

-|보험사기자 예측|MyProject
--|--|--
Structured/Unstructured Data|데이터 재구조화, 데이터 병합|
Data Item Definition|테이블 및 변수 정의서 참고|
Legacy ERD/Meta Data/Process|무관|
Data Life Cycle|2016년 데이터|
Data Storing Design(RDB, HDFS)|csv 파일 형식|
Understanding Missing/Outlier|NA, NULL 결측치 처리|
EDA|기본 통계량 확인, 데이터 탐색|
Consistent Data Quality|무관|
### 데이터 탐색
자료|남게되는량
--|--
Unstructured Data|75%
Semi-structured Data|55
Analystic|20
### 데이터 시각화

## 3.Data analyzing

-|보험사기자예측|MYROJECT
--|--|--
Understanding Missing&Outlier Data|결측치, 이상치 처리|
Selection Variables, Derived Data|변수선택(PCA, SVMRFE 등)|
Advanced Analytics Results|NNet, SVM, XGBoost 등을 이용한 분류|
Model Evaluation|F-measure를 이용한 모델 검증|
Considering Overfitting||
Model Algorithm Description|NNet, SVM, XGBoost|
Model Assessing Criteria|F-measure가 얼마인가|
Training/Test/Validation Data|Train/Test set 70%/30%|

- F-measure
    - 가중치를 가진 조화평균
    - Precision과 Recall 통합하여 정확성을 한번에 나타내는 지표

### 가설수립 및 검증
- 개인 특성에 따른 가설
    - 고객의 성별, 나이에 따라 사기자 비율이 달라지지 않을까?
    - 지역, 주거타입, 고객소득에 따라 달라지지 않을까?
        - 오피스텔 및 상가 등은 사기자 비율이 높은반면 아파트 등은 낮다. 추가적으로 오피스텔 거주자는 박스플롯 결과 소득분포가 달랐다. 
    - FP경력에 따라 사기자 비율이 달라지지 않을까 ?
        - 보험설계자 3명과 인터뷰 결과, 보험을 잘 아는 사람이 보험사기를 칠 것 같다라는 의견을 들었다. 이러한 현업지식을 데이터를 통해 확인해보았다

- 고객 로그정보에 따른 가설
    - 사기자들은 보험클레임을 많이 걸지 않을까
    - 특정병원 종류를 선호하지 않을까
    - 금감원 유의 병원에 갔으면 사기자로 의심해야 할까
    - 사기자들은 자기부담금 비율이 낮지 않을까
    - 사기자들이 선호하는 청구사유가 잇지 않을까?
    - 입원일수가 증가할수록 사기자비율이 증가하지 않을까?
        - 히스토그램으로 확인결과 실제 입원일이 증가할 수록 사기자의 비율이 증가함을 확인
    - 사기자들이 선호하는 보험상품종류가 잇지 않을까

### 변수 선택
- 세워진 가설 및 가설검증으로 변수를 선택가능
### 정형데이터 분석
### 모델선택
### 모델구축
### 모델평가

## 4.System developing(웹 어플리캐이션 개발)
### 운영데이터 준비
### 시스템 설계 및 개발
### 모델확인

## 5.Deploying
### 배포계획 수립
### 모니터링 및 유지보수모델 및 시스템
### 재건축모델 및 시스템계획
### 모델 유효성 검사
### 프로젝트마무리

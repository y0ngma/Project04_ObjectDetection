## Table of Content
- 명령어 종류
    ```SQL
    DDL
    테이블 정의어
        CREATE      -- 생성
        ALTER       -- 타입을 변경
        ALTER TABLE 테이블명 RENAME COLUMN 기존컬럼명 TO 바꿀컬럼명;
        DROP        -- 삭제
        RENAME      -- 이름
        TRUNCATE    -- 비우기

    DML
    데이터 조작어
        INSERT 
            INTO MEMBER(ID, NAME, AGE) VALUEs('a', 'b', 34) --value S 철자주의
        UPDATE
            MEMBER SET NAME='B1', AGE=44 WHERE ID='a' 
        DELETE
            FROM MEMBER WHERE ID='a'
        SELECT
            * FROM MEMBER WHERE ID LIKE 'a%'    -- LIKE 는 정규식
            ORDER BY NO DESC | ACS              -- 내림 | 오름차순
        "%" || "가" ||"%"   -> "가" 포함
        "가"|| "%"          -> "가" 시작
        "%" || "가"         -> "가" 끝남

    DCL 
    데이터 제어어
        GRANT       -- 권한 부여
        REVOKE      -- 권한 삭제

    TCL
    트랜잭션 제어어
        COMMIT      -- 적용
        ROLLBACK    -- 포인트로 돌아가기
        SAVEPOINT
    ```
---

## Basic commands
- Oracle SQL Developer. 192.168.99.100_admin의 테이블에서
- 워크시트에 다음과 같이 입력하고 원하는 행을 드레그해서 개별실행 가능
- 실행결과는 중간의 '질의 결과'텝이나 상단의 BOARD_TABLE1의 데이터탭에서 확인 가능
    ```SQL
    1. 추가
        INSERT INTO BOARD_TABLE1(TITLE, CONTENT, WRITER, HIT, REGDATE)
        VALUES('sql에서 추가', '내용임', '작성자임', 34, SYSDATE);
        COMMIT;
        -- 예시        
        INSERT INTO ITEM1 (NAME, CONTENT, PRICE, REGDATE)
        VALUES('패딩', '파타고니아 남성 겨울신상', 1080000, SYSDATE);
        COMMIT;

    1. 삭제
        delete from board_table1 where no = 47;
        commit;
        
    1. 수정
        update board_table1 set title='변경1', content='변경2' where no = 52;
        update board_table1 set no=53 where no = 52;
        
    1. 조회;
        -- 데이터 많을시 가장 빠른 조건문:NO 이용
        SELECT * FROM BOARD_TABLE1 WHERE NO IN (3, 4, 5, 6, 7);
        
        --ORDER BY [정렬할 내용][ASC/DESC]이다 ORDER NO BY DESC 아니고    
        SELECT * FROM BOARD_TABLE1 ORDER BY NO DESC; 
        SELECT NO FROM BOARD_TABLE1 WHERE HIT >= 5;
        SELECT * FROM BOARD_TABLE1 UNION ALL;
    ```

## SELECT
-     
    ```SQL
    - mysql 기준 1부터
        SELECT * FROM MEMBER_TABLE2 LIMIT 1,10;

    - oracle 에서 하는방법
        SELECT * FROM (
            SELECT 
                NO, TITLE, CONTENT, 
                ROW_NUMBER() OVER (ORDER BY NO DESC) ROWN
            FROM
                BOARD_TABLE1)
        WHERE ROWN BETWEEN 1 AND 10

    - 한글이 포함된 항목조회
        SELECT * FROM BOARD_TABLE1
        WHERE NAME LIKE '%'||'홍길동'||'%'
        WHERE TITLE LIKE '%'||'제목'||'%'
    ```
- 집계함수:SUM,MAX,MIN,COUNT개수, AVG
    ```SQL
    SELECT
        'MEMBER_TABLE2'.'CLASSROOM', -- [테이블]의 [클래스룸이라 저장된 데이터]랑
        SUM('MEMBER_TABLE2'.'KOR') AS 'SUM1', -- kor행 데이터합 별칭을 SUM1로
        SUM('MEMBER_TABLE2'.'ENG') AS 'SUM2',
        SUM('MEMBER_TABLE2'.'MATH') AS 'SUM3'
    FROM 'MEMBER_TABLE2'
    ```
        
    ```sql
    -- 검색어 최초검색된 날짜, 최종일
    SELECT YEAR, MONTH, DAY, TIME FROM BOARD_BOARD1
    WHERE NO IN (SELECT NO FROM BOARD_BOARD1 WHERE NO <= 1000)AND
        WORD LIKE %s
    ORDER BY YEAR, MONTH, DAY, TIME ASC
    ```

## Mongo DB -> Oracle DB
- 크롤링해온 데이터를 서비스 하기 위해 오라클로 옮겨야 한다
- 배포하고자 하는 정보만 옮기고 정렬 등 한다

- 순차적 번호를 매기기
    ```sql
    -- 자동 증가 시퀸스 생성
    -- SEQ_TABLE1_NO = SEQ_TABLE1_NO+1 번호증가
    CREATE SEQUENCE SEQ_TABLE1_NO
    START WITH 1
    INCREMENT BY 1
    NOMAXVALUE
    NOCACHE;
    COMMIT;

    -- 테이블 편집-자동 


    -- TABLE1의 데이터가 번호증가 하는지 확인
    INSERT INTO TABLE1 (NO, ID, NAME, AGE)
    VALUES(SEQ_TABLE1_NO.nextval, 'a', 'name', 34);
    COMMIT;

    -- SEQ_TABLE1_NO.nextval을 테이블편집-기본값에 입력
    -- 위sql문과 동일한 실행문이 된다.
    INSERT INTO TABLE1 (ID, NAME, AGE)
    VALUES('a', 'name', 34);
    COMMIT;
    ```

## Advanced Commands
- distinct / group by
    ```sql
    SELECT * 
    FROM BOARD_BOARD1
    WHERE 
    GROUP BY --집계하고자 하는 컬럼(들)

    -- 집계하기
    COUNT(*) null값포함 테이블 전체건수
    COUNT(컬럼명) null 제외한 해당컬럼 건수
    COUNT(DISTINCT 원하는 컬럼) 데이터 종류수
    ORDER BY COUNT(*) DESC

    -- 집계된 값 기준으로 정렬
    SELECT  T1.REGION_CD
            ,COUNT(*) STORE_CNT
    FROM    SQL_TEST.MA_STORE T1
    GROUP BY T1.REGION_CD
    ORDER BY COUNT(*) DESC 
    ```

- Multiple-Row Subquery
    - 괄호로 묶어서 활용
    ```sql
    -- IN  하나의 컬럼이 하나이상의 "=" 조건 가질때
    -- 부서별 최저 임금받는 사원의 정보 
    SELECT NAME, SAL, DEPTNO FROM EMPLOYEES
    WHERE SAL IN (
        SELECT MIN(SAL) FROM EMPLOYEES GROUP BY DEPTNO)
    
    -- ANY 하나이상 맞으면 참 (>MIN 또는 OR와 비슷)
    -- ALL 모두 맞아야 (>MAX 또는 AND와 비슷)
    -- 10000이상 받는 모든사원의 나이보다 낮은연령의 사원정보
    SELECT DEPTNO, NAME, SAL FROM EMPLOYEES
    WHERE AGE < ALL (
        SELECT AGE FROM EMPLOYEES WHERE SAL > 10000 )

    -- Bruce와  동일직책, 동일부서인 사원 검색 
    select employee_id, first_name, job_id, salary
    from employees
    where (manager_id, job_id) in (
        select manager_id, job_id
        from employees
        where first_name = 'Bruce')
        and first_name <> 'Bruce' 
        -- <>는 != 이랑 같음 
    ```

- COUNT와 GROUP BY
    ```sql
    -- 인덱스<1000 중 검색어 1순위, 입력한시간에 해당하는 검색어
    SELECT COUNT(*) FROM (
    SELECT WORD FROM BOARD_BOARD1
    WHERE NO IN (
        SELECT NO FROM BOARD_BOARD1 WHERE NO <= 1000) 
    AND RANK = 1   
    )
    ```
    | Option | Description |
    | ------ | ----------- |
    |1행|30|

    ```sql
    SELECT WORD,COUNT(*) FROM (
        SELECT WORD FROM BOARD_BOARD1
        WHERE NO IN (
            SELECT NO FROM BOARD_BOARD1 WHERE NO <= 1000) 
        AND RANK = 1   
        )
    GROUP BY WORD
    ```
    | Option | Description |
    | ------ | ----------- |
    |유한양행	     | 10|
    |버스도착정보    |	5|
    |아리따움대란    |	15|

- 컬럼 합쳐서 비교 (To_CHAR, TO_DATE, TO_NUMBER)
- 
```sql
SELECT WORD,TO_NUMBER(YEAR||MONTH||DAY||TIME) 
FROM BOARD_BOARD1 
WHERE 
    GENE LIKE '%10대%' AND
    TO_NUMBER(YEAR||MONTH||DAY||TIME) >= 2019721 AND
    TO_NUMBER(YEAR||MONTH||DAY||TIME) < 2019742 AND
    RANK >= 1 AND RANK <=3

-- 아래는 2020년 1월 2일 ~ 2월 1일 검색시 월은 만족,일은 불만족으로 에러.. 합칠필요   
SELECT WORD FROM BOARD_BOARD1
WHERE 
    GENE LIKE %s AND 
    (YEAR  >= %s AND YEAR  <= %s) AND
    (MONTH >= %s AND MONTH <= %s) AND
    (DAY   >= %s AND DAY   <= %s) AND 
    (TIME  >= %s AND TIME  <= %s) AND 
    (RANK  >= %s AND RANK  <= %s)
```    

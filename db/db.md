
## 명령어정리
- https://kb.objectrocket.com/postgresql/how-to-show-databases-in-postgresql-848
```bash
# postgresql 설치 확인
service postgresql status
# command-line postgresql 인터페이스 설치확인
psql -V

# 명령에 대한 설명보기
man createuser

# 사용자계정으로 db 접속
sudo -u dejavu psql -d dejavu
# psql 접속후 접속정보 보기
\conninfo
# 데이터테이블 리스트
\list
# 테이블 확인
\d
# 데이블 데이터타입 확인
\dt
# 접속후 나가기
\q
exit

```
### 데이터베이스



## 우분투에 포스트그레 설치하기
- 
```ini
# database.int
# 외부에서 서버 접속시 ~/connect.py 및 ~/config.py 등 에서 참조할 파일 
[postgresql]
host=192.168.0.59
database=dejavu
user=postgres
password=password
```

### 설치하려는 우분투에서
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

### root user 비번설정
```bash
# 접속
sudo -u postgres psql postgres
\password postgres
```

### sudo 계정으로 접속해서 아이디 만들기
```
sudo -i -u postgres
createuser --interactive

Enter name of role to add: dejavu
Shall the new role be a superuser? (y/n) y
```

### db 만들기
```bash
sudo -i -u postgres
createdb dejavu
sudo adduser dejavu
sudo -u dejavu psql -d dejavu
# 접속정보 확인
\conninfo
```

---

### sql 문
```sql
-- 데이블 만들기
CREATE TABLE words (
    equipId serial PRIMARY KEY,
    word varchar (50) NOT NULL,
    means varchar (250) NOT NULL,
    example varchar (1000) NULL,
    location varchar (250) check (location in ('north', 'south', 'west', 'east', 'northeast', 'southeast', 'southwest', 'northwest')),
    updateDate date
);

-- 데이터 입력
INSERT INTO words (word, means, example, location, updateDate) VALUES ('simple', '간단한', 'see also simply', 'east', '2017-09-14');
INSERT INTO words (word, means, example, location, updateDate) VALUES ('difficult', '어려운', 'an unreasonable and unhelpful way.', 'west', '2017-09-14');

-- 데이터 확인
select * from words;
select * from words where word = 'simple';

-- 데이터 업데이트
update words set means = '[^디퍼런스]\n어려운' where word = 'difficult';
select * from words where word = 'difficult'; -- 확인
-- 삭제
delete from words where word = 'simple';
select * from words; -- 확인

-- 테이블 변경
-- 컬럼 lastdate 추가
alter table words add lastdate date;
select * from words; -- 확인

-- 컬럼 삭제
alter table words drop lastdate;
```

---


## 외부에서 접속가능하게 하기
- 포트확인 및 수정
    - /찾는단어 + 엔터 해서 찾고, 'a' 눌러서 수정 후
    - esc 후 :wq(수정후나감) 또는 :wq!(저장없이)
```bash
netstat -ntlp 
sudo vim /etc/postgresql/9.5/main/postgresql.conf
```
- 주석제거 및 ' * ' 으로 변경
    - /listen 입력으로 검색
```bash
#------------------------------------------------------------------------------
# CONNECTIONS AND AUTHENTICATION
#------------------------------------------------------------------------------

# - Connection Settings -
# 기본으로 localhost로 설정되어 있을 것이다.
listen_addresses = '*'                  # what IP address(es) to listen on;
                                        # comma-separated list of addresses;
                                        # defaults to 'localhost'; use '*' for all
```
- 재시작 및 확인
```bash
sudo /etc/init.d/postgresql restart
netstat -ntlp
# 127.0.0.1:5432가 0.0.0.0:5432으로 변경됨
```
- 수정 
```bash
sudo vim /etc/postgresql/9.5/main/pg_hba.conf
```
- IPv4 local connections
    - @ pg_hba.conf 
    - /IPv4 local connections으로 검색 후
    - 내용 모두 all 으로 변경
```bash
local   all             postgres                                peer

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             0.0.0.0/0               md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
# Allow replication connections from localhost, by a user with the
# replication privilege.
#local   replication     postgres                                peer
#host    replication     postgres        127.0.0.1/32            md5
#host    replication     postgres        ::1/128                 md5
```
- 재시작 및 외부접속 되는지 확인해본다
```
sudo /etc/init.d/postgresql restart
```
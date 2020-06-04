from django.db import models
from django.contrib.auth.models import User
# python manage.py check
# python manage.py makemigrations member
# python manage.py migrate member

class Member1(models.Model):
    objects = models.Manager() # vs code 오류제거용
    id      = models.IntegerField(primary_key=True)
    group   = models.ForeignKey(
                    User,
                    on_delete=models.Cascade, # 연결된 테이블의 기록 같이 삭제
                    blank=True, null=True # 빈칸이나 group필드 Null값 허용
                    )
    name    = models.CharField(max_length=30)
    gender  = models.CharField(max_length=10)
    age     = models.IntegerField(max_length=30)
    img     = models.BinaryField(null=True) # 바이너리 필수
    upload  = models.ImageField(upload_to ='uploads/% Y/% m/% d/')
    # file will be saved to MEDIA_ROOT / uploads / 2015 / 01 / 30 
    intime  = models.DateTimeField(auto_now_add=True)
    outtime = models.DateTimeField(auto_now_add=True)
    regdate = models.DateTimeField(auto_now_add=True) # 자동

# class Table1(models.Model):
#     objects = models.Manager() # vs code 오류 제거용

#     no      = models.AutoField(primary_key=True) # 자동 번호매기기
#         # 자동의 이점 : 개발자가 번호 중복 매기지 않을 수 있음
# # 사용자로부터 받을 내용-----------------------------
#     title   = models.CharField(max_length=200) 
#     content = models.TextField() 
#     writer  = models.CharField(max_length=50)
# # -------------------------------------------------
#     hit     = models.IntegerField() # 조회수
#     img     = models.BinaryField(null=True) # 바이너리 필수
#     regdate = models.DateTimeField(auto_now_add=True) # 자동

    
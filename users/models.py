from django.db import models

# Create your models here.
class User(models.Model):
    #unique=True : 고유한 값이어야함 즉, email,mobile_number,username은 
    # 로그인할때 id로 사용할 수 있기에 중복한 값이 없어야한다
    email=models.CharField(max_length=100, unique=True, null=True)
    full_name=models.CharField(max_length=100)
    username=models.CharField(max_length=100, unique=True)
    password=models.CharField(max_length=300)
    mobile_number=models.CharField(max_length=100, unique=True, null=True )
    #회원가입을 관리할때는 시간관리가 중요함
    #auto_now_add : 처음 생성된 시점을 자동으로 기록해줌
    #auto_now : 필드가 업데이트 될때마다 그 시점을 기록해줌
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='users'


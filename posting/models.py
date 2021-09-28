from django.db import models
from users.models  import User

# posting - 인스타그램의 게시물 생성하는 app
# 게시물에는 작성자,이미지,내용, 생성시간이 필요하다
# 게시물의 사진은 여러개 등록할 수 있다.
# 게시물의 작성자는 이미 서비스에 가입된 유저여야 한다.
 
class Posting(models.Model):
    #content는 공백 허용, 내용을 작성하지 않아도 됨
    content = models.CharField(max_length=2000, null=True)
    #auto_now_add : 생성일자, django model이 최초 저장(insert)시에만 
    # 현재날짜를 적용한다. 
    created_at = models.DateTimeField(auto_now_add=True)
    
    #users.User -> 외부의 클래스를 가져오려면 경로를 명확히 해주어야한다. 
    #               User라고 하면 에러발생함
    user= models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table='postings'
        
class Image(models.Model):
    image_url = models.URLField(max_length=2000)
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE)
    
    class Meta:
        db_table='images'


class Comment(models.Model):
    content    = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    #한명의 유저는 여러개의 댓글을 달 수 있음 ( User와 Comment테이블은 1대다관계)
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    #하나의 게시물에 댓글이 여러개 달릴수있음 (posting과 comment테이블은 1대다관계)
    posting    = models.ForeignKey('Posting', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'comments'
        
    
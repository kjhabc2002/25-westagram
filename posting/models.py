from django.db import models
from users.models import User

# posting - 인스타그램의 게시물 생성하는 app
# 게시물에는 작성자,이미지,내용, 생성시간이 필요하다
# 게시물의 사진은 여러개 등록할 수 있다.
# 게시물의 작성자는 이미 서비스에 가입된 유저여야 한다.
 
class Posting(models.Model):
    content = models.CharField(max_length=2000, null=True)
    created_at = models.CharField(auto_now_add=True)
    user= models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table='postings'
        
class Image(models.Model):
    image_url = models.URLField()
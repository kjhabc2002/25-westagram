
import json
from json.decoder import JSONDecodeError

from django.shortcuts import render
from django.views     import View

from posting.models   import Posting, Image, Comment
from users.models    import User
from django.http      import JsonResponse
from users.utils      import login_decorator  

class PostingView(View):
    #post함수를 실행하기 전에 로그인 토큰을 확인하도록 데코레이터 추가
    @login_decorator
    def post(self, request):
        try:
            data=json.loads(request.body)
            #user = User.objects.get(username=data.get('user',None))
            user=request.user
            
            content = data.get('content', None)
            image_url_list = data.get('image_url', None)
            # key error 처리하기
            # content는 없어도 되는 정보이므로 user와 image_url_list에만 값이 잘 담겨져있는지 확인
            
            # if문에 user가 빠진이유는 
            # user에는 데코레이터를 통과했다면 반드시 값이 담기므로 keyerror를 처리할 필요가 없다.
            if not image_url_list:
                return JsonResponse({'image':'KEY_ERROR'}, status=400)

            # create()메서드를 이용한 데이터 생성하기
            posting= Posting.objects.create(
                user = user,
                content = content
            )
            #image_url_list는 이미지가 담긴 리스트로 for문을 사용하여 리스트 값을 하나씩
            # 가져와야 됨
            # foreign key인 posting도 생성해야함
            for image_url in image_url_list:
                Image.objects.create(
                    image_url = image_url,
                    posting = posting
                )
                return JsonResponse({'message':'SUCCESS'}, status=200)
            
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        #모든 게시물을 get()메서드를 이용하여 조회하기
        
    def get(self, request):
            #위에서 정의했던 posting을 이용해서 게시물의 속성을 가져올 수 있음
            #posing_list를 딕셔너리 형태로 담긴 리스트로 정의해라
            posting_list = [{
                "username" : User.objects.get(id=posting.user.id).username,
                "content" : posting.content,
                "image_url" : [i.image_url for i in Image.objects.filter(posting_id=posting.id)],
                "create_at" : posting.created_at
                } for posting in Posting.objects.all()]
            
            return JsonResponse({'data':posting_list}, status=200)

#특정 유저의 게시물 표출 기능
#user_id로 조회해서 특정유저의 게시물만 표출하는 로직구현
class PostingSearchView(View):
    def get(self, request, user_id):
        #user_id에 해당하는 유저가 없을 경우 에러코드 응답
        if not User.objects.filter(id=user_id).exists():
            return JsonResponse({'message':'USER_DOES_NOT_EXIST'}, status=404)
        #filter로 해당유저의 정보만 가져옴
        posting_list = [{
            "username" : User.objects.get(id=user_id).username,
            "content" : posting.content,
            "image_url" : [i.image_url for i in Image.objects.filter(posting_id = posting.id)],
            } for posting in Posting.objects.filter(user_id=user_id)]
        return JsonResponse({'data':posting_list}, status=200)

class CommentView(View):
    @login_decorator
    def post(self,request):
        try:
            data=json.loads(request.body)
            user=request.user
            
            content    = data.get('content', None)
            posting_id = data.get('posting_id', None)
            
            if not (content and posting_id):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
            
            # 요청받은 posting_id에 매칭되는 게시물이 있는지 확인한다.
            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({'message':'POSTING_DOES_NOT_EXIST'}, status=404)
            
            posting = Posting.objects.get(id=posting_id)
            
            Comment.objects.create(
                content = content,
                user    = user,
                posting = posting
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

#댓글 표출 기능
#특정 게시물에 대한 댓글만 표출
class CommentSearchView(View):
    #url로 posting_id를 전달받아 해당 게시물에 대한 댓글을 보여줌
    def get(self, request, posting_id):
        if not Posting.objects.filter(id=posting_id).exists():
            return JsonResponse({'message':'POSTING_DOES_NOT_EXIST'}, status=404)

        comment_list = [{
            "username"  : User.objects.get(id=comment.user.id).username,
            "content"   : comment.content,
            "create_at" : comment.created_at
            } for comment in Comment.objects.filter(posting_id=posting_id)
        ]

        return JsonResponse({'data':comment_list}, status=200)

        
        
                
            
                

import json
from json.decoder import JSONDecodeError

from django.shortcuts import render
from django.views     import View

from posting.models   import Posting, Image
from users.models    import User
from django.http      import JsonResponse

class PostingView(View):
    def post(self, request):
        try:
            data=json.loads(request.body)
            user = User.objects.get(username=data.get('user',None))
            content = data.get('content', None)
            image_url_list = data.get('image_url', None)
            # key error 처리하기
            # content는 없어도 되는 정보이므로 user와 image_url_list에만 값이 잘 담겨져있는지 확인
            if not (user and image_url_list):
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

        
    
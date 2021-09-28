import jwt
import json

from django.http import JsonResponse
from my_settings import SECRET, ALGORITHM
from users.models import User

# 장고에서는 보통 데코레이터를 utils.py라는 파일에 별도로 저장한다.
def login_decorator(func): 		
    # wrapper함수에는 self(instance자신), request(http request)를 매개변수로 받음
    # 매개변수가 고정되어있지 않을때 wrapper함수를 가변인수함수로 만든다.
    def wrapper(self, request, *args, **kwargs): 		
        try:
            # HTTP Request의 헤더인 Authorization의 값을 가져오고 없으면 None으로 남김
            access_token = request.headers.get('Authorization', None) 		
            # payload는 토큰을 디코딩하면 나오게 될 사용자에 대한 정보이다.
            # 디코딩에 들어가는 secret과 algorithms은 토큰 발생 시 넣었던 정보와 같아야한다.
            payload = jwt.decode(access_token, SECRET, algorithms=ALGORITHM)    
            # dbd에서 토큰의 사용자 정보와 매칭되는 사용자 정보를 불러오고, user라는 변수에
            # 저장한다. 
            user = User.objects.get(id=payload['id']) 				
            # 토큰발행시 id라는 키로 사용자 정보를 저장했으므로 불러올때도 동일하게 id라는 키를 사용
            request.user = user 						
            #request는 가변객체로 다른 객체 또는 변수할당이 가능하다
        except jwt.exceptions.DecodeError: 				
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)

        # 토큰에서 디코드된 사용자가 존재하지 않을 때 DoesNotExist발생
        except User.DoesNotExist: 						
            return JsonResponse({'message':'INVALID_USER'}, status=400)
        return func(self, request, *args, **kwargs)

    return wrapper
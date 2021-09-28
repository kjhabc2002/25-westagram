import json
import re
import bcrypt
import jwt
from json.decoder import JSONDecodeError

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from users.models     import User
from my_settings      import SECRET, ALGORITHM


PASSWORD_MINIMUM_LENGTH = 8

#회원가입 기능구현
class SignUpView(View):
    def post(self, request):
        try:
            #회원가입에 필요한 정보는 json형식으로 request의 body에 담겨서 옵니다.
            data= json.loads(request.body)
            
            # 딕셔너리 get메소드
            # 딕셔너리.get(키, 기본값) : 해당 키값이 없는 경우 기본값을 대신 가져옴
            
            email=data.get('email', None)
            mobile_number=data.get('mobile_number',None)
            username=data.get('username',None)
            password=data.get('password',None)
            full_name=data.get('full_name',None)
            
            #정규표현식 validation 구현
            email_pattern=re.compile('[a-zA-Z0-9._+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]')
            mobile_number_pattern=re.compile('^[0-9]{1,15}$')
            username_pattern=re.compile('^(?=.*[a-z])[a-z0-9_.]+$')
            
            
            if not (
                (email or mobile_number)
                and full_name
                and username
                and password
            ):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
            #if문으로 VaildationError가 발생하였음을 알려야한다.
            if email:
                if not re.match(email_pattern, email):
                    return JsonResponse({'message':'EMAIL_VALIDATION_ERROR'}, status=400)

            if mobile_number:
                if not re.match(mobile_number_pattern, mobile_number):
                    return JsonResponse({'message':'MOBILE_NUMBER_VALIDATION_ERROR'}, status=400)

            if not re.match(username_pattern, username):
                return JsonResponse({'message':'USERNAME_VALIDATION_ERROR'}, status=400)

            if len(data['password']) < PASSWORD_MINIMUM_LENGTH:
                return JsonResponse({'message':'PASSWORD_VALIDATION_ERROR'}, status=400)
            # q객체를 통해 or조건 사용
            # 전달된 정보가 없다면 1반환
            # 왜 None이 아니라 1로 했는가하면 email에는 null값이 존재할 수 있기 때문이다.
            # 만약 email이None이라면 기존 db에 등록되어 있던 null이 같은 값이라고 취급되어 중복값이 
            # 존재하는 것처럼 처리됨
            if User.objects.filter(
                Q(email         = data.get('email', 1)) |
                Q(mobile_number = data.get('mobile_number', 1)) |
                Q(username      = data['username'])
            ).exists():
                return JsonResponse({'message':'ALREADY_EXISTS'}, status=409)
            
            User.objects.create(
                email         = email,
                mobile_number = mobile_number,
                full_name     = full_name,
                username      = username,
                password      = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        # JSONDecodeError : 아무런 정보도 전달되지 않았을때 발생하는 에러
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

#로그인기능 구현
class LoginView(View):
    def post(self, request):
        try:
            data= json.loads(request.body)
            
            login_id=data.get('id',None)
            password=data.get('password',None)
            #password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            if not(login_id and password):
               return JsonResponse({'message':'KEY_ERROR'},status=401)
           
           #exists() : db에서 filter를 통해 조건의 데이터가 유무에 따라
           # true,false를 반환하는 메소드
           # 어떤 특정 조건 에 대해서 이벤트나 로직을 처리할 때 많이 쓰임
            if not User.objects.filter(
                #get() 메소드 : queryset이 아닌 모델 객체를 반환하는 함수
                Q(email=data.get('login_id')) |
                Q(mobile_number=data.get('login_id')) |
                Q(username = data.get('login_id'))
            #409 error code : 서버에 있는 파일보다 오래된 파일을 업로드하면 버전 제어 충돌발생
            ).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=409)     
            
            user = User.objects.get(
                Q(email=login_id) |
                Q(mobile_number=login_id) |
                Q(username=login_id)
            )
            #사용자 비밀번호를 가져와서 입력된 비밀번호와 비교
            # if user.password != password:
            #     return JsonResponse({'message':'INVALID_PASSWORD'},status=401)
            # return JsonResponse({'message':'SUCESS',}, stauts=201)
            
            # checkpw() 메소드로 입력된 비밀번호가 맞는지 확인
            # 사용자가 입력한 패스워드와 db에 str타입으로 저장되어있는 패스워드를 각각 인자로 받는데
            # 둘다 str타입으로 encode해줘야 함
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=401)
            
            #비밀번호가 일치하면 access_token을 발급하고 jsonresponse에 담아서 보낸다
            access_token =jwt.encode({"id":user.id}, SECRET, algorithm=ALGORITHM)
            
            return JsonResponse({'message':'SUCCESS', 'Authorization':access_token}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
            
            
                
                 
            
            
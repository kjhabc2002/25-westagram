import json
import re
from json.decoder import JSONDecodeError

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from users.models          import User


PASSWORD_MINIMUM_LENGTH = 8

class SignUpView(View):
    def post(self, request):
        try:
            #회원가입에 필요한 정보는 json형식으로 request의 body에 담겨서 옵니다.
            data= json.load(request.body)
            
            # 딕셔너리 get메소드
            # 딕셔너리.get(키, 기본값) : 해당 키값이 없는 경우 기본값을 대신 가져옴
            
            email=data.get('email', None)
            mobile_number=data.get('mobile_number',None)
            username=data.get('useraname',None)
            password=data.get('password',None)
            full_name=data.get('full_name',None)
            
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
                password      = password
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        # JSONDecodeError : 아무런 정보도 전달되지 않았을때 발생하는 에러
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

class 
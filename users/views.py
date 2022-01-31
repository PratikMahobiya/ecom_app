import email
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import User
from . import serializers
import users

# Create your views here.
# FOR NEW USER REGISTRATION ---------
class RegisterUser(APIView):
  def post(self, request):
    serializer = serializers.UserSerializer(data=request.data)
    if not serializer.is_valid():
      return JsonResponse({'status':403, 'errors': serializer.errors})
    serializer.save()
    user          = User.objects.get(email = serializer.data['email'])
    token_obj, _  = Token.objects.get_or_create(user = user)
    return JsonResponse({'status':200, 'data': serializer.data, 'token':str(token_obj)})

# FOR LOGIN -------------
class Login(APIView):
  def post(self, request):
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    try:
      Account = User.objects.get(email=email)
    except BaseException as e:
      return JsonResponse({'status':400, 'message':'Email not found.'})

    token = Token.objects.get_or_create(user=Account)[0].key
    if not User.check_password(Account,raw_password=password):
        return JsonResponse({'status':400, 'message':'Invalid Credential.'})

    if Account:
      if Account.is_active:
        serializer = serializers.UserSerializer(User.objects.filter(email = Account),many=True)
        return JsonResponse({'status':200, 'data':serializer.data, 'token': token})
      else:
          return JsonResponse({'status':400, 'message':'Account not active.'})
    else:
        return JsonResponse({'status':400, 'message': 'Account doesnt exist'})

# FOR LOGOUT ------------
class Logout(APIView):
  def post(self, request):
    request.user.auth_token.delete()
    return JsonResponse({'status':200, 'message': 'User Logout Successfully.'})

# FOR AUTHEN ------------
class Auth_User(APIView):
  def post(self, request):
    token = request.data['token']
    if token is None:
      return JsonResponse({'status':200, 'success': False,'message':'Please SignIn.'})
    elif len(Token.objects.filter(key=token)) == 0:
      return JsonResponse({'status':200, 'success': False, 'message':'Session Expired.'})
    else:
      email = Token.objects.get(key=token).user
      serializer = serializers.UserSerializer(User.objects.filter(email = email),many=True)
      return JsonResponse({'status':200,'success': True, 'data':serializer.data, 'token': token,'message':'Already Login.'})

class test_v(APIView):
  authentication_classes = [TokenAuthentication,]
  permission_classes = [IsAuthenticated]
  def get(self, request):
    return JsonResponse({'status':200,'data':'TESTED POSITIVE'})
    
from api.user.models import Organization
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import status, mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import sso_api, get_faculty_info
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from ..user.serializers import UserDetailSerializer
from django.contrib.auth.models import User, Group

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginSSOViewSets(mixins.CreateModelMixin, viewsets.GenericViewSet):    
    def create(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        sso_data = sso_api(username=username, password=password).json()

        if sso_data['state'] == 0:
            return Response({"success": False, "message": 'Username atau password SSO tidak sesuai. Silahkan coba lagi.'}, status=status.HTTP_400_BAD_REQUEST)

        count_users = User.objects.filter(username=username).count()

        if count_users == 0:
            email = f'{username}@ui.ac.id'
            user = User.objects.create_user(username=username, password=password, email=email)
            if sso_data['nama_role'] == 'mahasiswa':
                print(sso_data)
                prodi  = sso_data['kode_org'].split(":")[0]
                full_name =  sso_data['nama']
                id_code =  sso_data['kodeidentitas']
                organization_class = Organization.objects.get(id = prodi)
                
                user_detail = {
                    'email': email,
                    'role' : 'STU',
                    'is_external': False,
                    'full_name': full_name,
                    'id_code': id_code
                }

                serializer = UserDetailSerializer(data=user_detail)

                if serializer.is_valid():
                    group = Group.objects.get(name='Student')

                    user.groups.add(group)
                    serializer.save(user=user, organization=organization_class)

                    serializer = MyTokenObtainPairSerializer(data={'username': username, 'password': password})
                    serializer.is_valid(raise_exception=True)
                    token_data = serializer.validated_data
                    refresh_token = RefreshToken.for_user(user)
                    access_token = token_data['access']

                    return Response({'access_token': str(access_token), 'refresh_token': str(refresh_token)})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif sso_data['nama_role'] == 'dosen':
                full_name =  sso_data['nama']
                id_code =  sso_data['kodeidentitas']

                user_detail = {
                    'email': email,
                    'role' : 'LEC',
                    'is_external': False,
                    'full_name': full_name,
                    'id_code': id_code
                }
                serializer = UserDetailSerializer(data=user_detail)
                if serializer.is_valid():
                    group = Group.objects.get(name='Lecturer')

                    user.groups.add(group)
                    serializer.save(user=user)

                    serializer = MyTokenObtainPairSerializer(data={'username': username, 'password': password})
                    serializer.is_valid(raise_exception=True)
                    token_data = serializer.validated_data
                    refresh_token = RefreshToken.for_user(user)
                    access_token = token_data['access']

                    return Response({'access_token': str(access_token), 'refresh_token': str(refresh_token)})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                full_name =  sso_data['nama']
                id_code =  sso_data['kodeidentitas']
                
                user_detail = {
                    'email': email,
                    'role' : 'SEC',
                    'is_external': False,
                    'full_name': full_name,
                    'id_code': id_code
                }
                serializer = UserDetailSerializer(data=user_detail)
                if serializer.is_valid():
                    group = Group.objects.get(name='Secretary')

                    user.groups.add(group)
                    serializer.save(user=user)

                    serializer = MyTokenObtainPairSerializer(data={'username': username, 'password': password})
                    serializer.is_valid(raise_exception=True)
                    token_data = serializer.validated_data
                    refresh_token = RefreshToken.for_user(user)
                    access_token = token_data['access']

                    return Response({'access_token': str(access_token), 'refresh_token': str(refresh_token)})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif count_users == 1:
            user = authenticate(request, username=username, password=password)

            login(request, user)

            serializer = MyTokenObtainPairSerializer(data={'username': username, 'password': password})
            serializer.is_valid(raise_exception=True)
            token_data = serializer.validated_data
            refresh_token = RefreshToken.for_user(user)
            access_token = token_data['access']

            return Response({'access_token': str(access_token), 'refresh_token': str(refresh_token)})

        elif count_users > 1:
            messages.error(request, 'Terdapat lebih dari 1 akun dengan username sama. Silakan hubungi Admin')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
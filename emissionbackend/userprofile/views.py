from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ProjectSerializer
from .utils import NoServerAvailableException, NoUserEmailException
from .models import User
from .serializers import UserSerializer, LoginSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing User.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if not request.data.get('project', None):
            return Response(
                'Project ID is required',
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            resp = super().create(request, *args, **kwargs)
        except NoServerAvailableException:
            return Response(
                "No server available",
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except NoUserEmailException:
            return Response(
                "Email is required",
                status=status.HTTP_400_BAD_REQUEST
            )
        if resp.status_code == 201:
            # login user
            user = User.objects.get(email=request.data['email'])
            user_project = ProjectSerializer(user.project)
            return Response(
                {
                    **user.refresh_token(),
                    'user_token': user.token,
                    'date_joined': user.date_joined,
                    'server_url': user.active_server,
                    **user_project.data,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(resp.data, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # Hash password but passwords are not required
        if 'password' in self.request.data:
            password = make_password(self.request.data.get('password'))
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        # Hash password but passwords are not required
        if 'password' in self.request.data:
            password = make_password(self.request.data.get('password'))
            serializer.save(password=password)
        else:
            serializer.save()


class LoginView(GenericAPIView):
    """[MOBILE] Resident Login (email and password)"""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.data.get('username', None)
        if username:
            try:
                user = User.objects.get(
                    username=username,
                )
            except User.DoesNotExist:
                return Response(
                    f'User with email={email} and username={username} does not exist',
                    status=status.HTTP_404_NOT_FOUND
                )
            # authenticate user
            user = authenticate(
                request,
                username=username,
                password=serializer.data.get('password', None)
            )
            if not user:
                return Response(
                    'User email or password is incorrect',
                    status=status.HTTP_401_UNAUTHORIZED
                )
            if not serializer.data.get('project', None):
                return Response(
                    'Project ID is required',
                    status=status.HTTP_400_BAD_REQUEST
                )
            if user.project is not None:
                if user.project.id != serializer.data.get('project'):
                    return Response(
                        'Project ID is incorrect',
                        status=status.HTTP_400_BAD_REQUEST
                    )

            user_project = ProjectSerializer(user.project)

            return Response(
                {
                    **user.refresh_token(),
                    'user_token': user.token,
                    'date_joined': user.date_joined,
                    'user_server': user.active_server,
                    **user_project.data,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            'User email does not exist',
            status=status.HTTP_404_NOT_FOUND
        )


class LogoutView(APIView):
    """[MOBILE] Log user out and expire token"""

    def get(self, request, *args, **kwargs):
        request.user.expire_token()
        logout(request)
        return Response('User logout successfully', status.HTTP_200_OK)

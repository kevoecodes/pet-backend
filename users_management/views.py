from django.contrib.auth import authenticate
from rest_framework import status, generics, filters
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from pet_backend.utils.common import StandardResultsSetPagination
from users_management.models import User
from users_management.serializers import UserListSerializer, LoginSerializer, RegisterUserSerializer, \
    ResetPasswordSerializer


class LoginUser(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            cleaned_data = serializer.validated_data
            _user = authenticate(
                email=cleaned_data['email'],
                password=cleaned_data['password']
            )
            if _user is not None:
                token = Token.objects.get_or_create(user=_user)
                serializer = UserListSerializer(_user, many=False)
                return Response({
                    "token": str(token[0]),
                    "user": serializer.data
                })

            return Response(False, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsers(generics.ListAPIView):
    search_fields = ['fist_name', 'last_name', 'cellphone']
    filter_backends = (filters.SearchFilter,)
    serializer_class = UserListSerializer
    queryset = User.objects.filter(is_superuser=False, role__isnull=False).order_by('-date_joined')
    pagination_class = StandardResultsSetPagination


class RegisterUser(APIView):

    @staticmethod
    def post(request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save(created_by=request.user)
            obj.set_password(serializer.validated_data['cellphone'])
            obj.save()
            return Response({
                "status": True,
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    @staticmethod
    def get(request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        return Response(UserListSerializer(instance=user, many=False).data)

    @staticmethod
    def put(request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        serializer = RegisterUserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response({
                "status": True,
                "data": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetUserPassword(APIView):

    @staticmethod
    def post(request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.password_changed = True
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({
                "status": True,
                "message": "Password reset successfully"
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



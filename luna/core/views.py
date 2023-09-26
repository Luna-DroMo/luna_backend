from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer, StudentUserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import User, StudentUser

from django.shortcuts import get_object_or_404


# Create your views here.
@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, email=request.data["email"])
    if not user.check_password(request.data["password"]):
        return Response(
            {"detail": "Not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})
    # return Response({})


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(
            email=request.data["email"],
            user_type=request.data["user_type"],
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
        )
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )
    # return Response({})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")
    # return Response({})


@api_view(["GET"])
def get_studentusers(request):
    if request.method == "GET":
        queryset = StudentUser.objects.all()
        serializer = StudentUserSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def get_users(request):
    if request.method == "GET":
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


# Retrieve a specific student user by ID:
@api_view(["GET"])
def get_studentuser(request, pk):
    try:
        studentuser = StudentUser.objects.get(pk=pk)
    except StudentUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = StudentUserSerializer(studentuser)
        return Response(serializer.data)


# Update the information of a student user
@api_view(["PATCH"])
def update_studentuser(request, pk):
    try:
        studentuser = StudentUser.objects.get(pk=pk)
    except StudentUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        serializer = StudentUserSerializer(
            studentuser,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            print(request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete a student user
@api_view(["DELETE"])
def delete_studentuser(request, pk):
    try:
        studentuser = StudentUser.objects.get(pk=pk)
    except StudentUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        studentuser.delete()
        return Response({"status": "Deleted"}, status=status.HTTP_200_OK)

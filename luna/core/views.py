from rest_framework.decorators import (
    api_view,
)
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import User, StudentUser
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema

def landing(request):
    return render(request, "core/index.html")

@swagger_auto_schema(tags=['Login'], method='post')
@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, email=request.data["email"])
    if not user.check_password(request.data["password"]):
        return Response(
            {"detail": "Not found."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    token, _ = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    response_data = {
        "token": token.key,
        "user": serializer.data,
    }

    try:
        student_user = StudentUser.objects.get(user=user)
        response_data["student_id"] = student_user.pk
    except StudentUser.DoesNotExist:
        pass

    return Response(response_data)

@swagger_auto_schema(tags=['Sign-Up'], method='post')
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
            university=request.data["university"],  # Comment out if cause any problem.
        )
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response(
            {
                "token": token.key,
                "user": serializer.data,
            }
        )
    print(serializer.errors)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )

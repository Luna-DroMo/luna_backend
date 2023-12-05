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
from .email import send_otp_via_email
from django.shortcuts import get_object_or_404


# Create your views here.


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
    return Response(
        {
            "token": token.key,
            "user": serializer.data,
        }
    )


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
        return Response(
            {
                "token": token.key,
                "user": serializer.data,
                # "otp": send_otp_via_email(email=request.data["email"]),
            }
        )
    print(serializer.errors)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


# def resend_email(request):
#     return Response(
#         {
#             "otp": send_otp_via_email(email=request.data["email"]),
#         }
#     )


# @api_view(["GET"])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     return Response("passed!")

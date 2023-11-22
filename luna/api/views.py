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

from core.serializers import UserSerializer, StudentUserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from core.models import StudentUser, Module
from django.shortcuts import get_object_or_404
from .serializers import ModuleSerializer
import json
from django.http import JsonResponse

# Update the information of a student user


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello"})


@api_view(['POST'])
def handle_post(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse({"status": "success", "data_received": data})


@api_view(["PATCH"])
def update_studentuser_with_id(request, pk):
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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_student_modules(request, id):
    try:
        student_user = StudentUser.objects.get(pk=id)
    except StudentUser.DoesNotExist:
        return Response({"message": "There is no user with this id"}, status=404)

    # If the StudentUser exists, then retrieve their modules
    modules = Module.objects.filter(student_user=student_user)
    serializer = ModuleSerializer(modules, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_studentusers(request):
    if request.method == "GET":
        queryset = StudentUser.objects.all()
        serializer = StudentUserSerializer(queryset, many=True)
        return Response(serializer.data)


# @api_view(["GET"])
# def get_users(request):
#     if request.method == "GET":
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)


# # Retrieve a specific student user by ID:
# @api_view(["GET"])
# def get_studentuser_with_pk(request, pk):
#     try:
#         studentuser = StudentUser.objects.get(pk=pk)
#     except StudentUser.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         serializer = StudentUserSerializer(studentuser)
#         return Response(serializer.data)


# @api_view(["GET"])
# def get_studentuser_with_email(request, email):
    try:
        studentuser = StudentUser.objects.get(email=email)
    except StudentUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = StudentUserSerializer(studentuser)
        return Response(serializer.data)


# Update the information of a student user
@api_view(["PATCH"])
def update_studentuser_with_email(request, email):
    try:
        studentuser = StudentUser.objects.get(email=email)
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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Delete a student user
# @api_view(["DELETE"])
# def delete_studentuser_with_pk(request, pk):
#     try:
#         studentuser = StudentUser.objects.get(pk=pk)
#     except StudentUser.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "DELETE":
#         studentuser.delete()
#         return Response({"status": "Deleted"}, status=status.HTTP_200_OK)


# # Delete a student user
# @api_view(["DELETE"])
# def delete_studentuser_with_email(request, email):
#     try:
#         studentuser = StudentUser.objects.get(email=email)
#     except StudentUser.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "DELETE":
#         studentuser.delete()
#         return Response({"status": "Deleted"}, status=status.HTTP_200_OK)


# # Update the information of a user
# @api_view(["PATCH"])
# def update_user_with_email(request, email):
#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "PATCH":
#         serializer = UserSerializer(
#             user,
#             data=request.data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# def get_user_with_email(request, email):
    # try:
    #     user = User.objects.get(email=email)
    # except User.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    # if request.method == "GET":
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

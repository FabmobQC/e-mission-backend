from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from projects.models import Project

from api.serializers import ProjectSerializer
from api.serializers import UserProfileSerializer

@api_view(['GET'])
def getProjects(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getProject(request, id):
    if request.method == 'GET':
        project = Project.objects.filter(id=id)
        serializer = ProjectSerializer(project[0], many=False)
        return Response(serializer.data)

@api_view(['POST'])
def UserProfileAPI(request):
    if request.method == 'POST':
        user_serializer = UserProfileSerializer(data=request.data)

        if user_serializer.is_valid(raise_exception=True):
                
            user_serializer.save()

            return Response({'status':'Success'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status':'Error'}, status=status.HTTP_401_UNAUTHORIZED)
    
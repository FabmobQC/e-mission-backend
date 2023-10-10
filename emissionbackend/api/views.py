from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from projects.models import Project
from userprofile.models import User

from api.serializers import ProjectMinimalSerializer, ProjectSerializer
from userprofile.serializers import UserSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectMinimalSerializer


class ConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProjectUsersAPI(request, id):

    if request.method == 'GET':
        user_profiles = User.objects.filter(project=id)
        serializer = UserSerializer(user_profiles, many=True)
        return Response(serializer.data)

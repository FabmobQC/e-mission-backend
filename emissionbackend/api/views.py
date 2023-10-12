from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from projects.models import Project
from userprofile.factories import UserFactory
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
    """ Return full configuration for project with user_email_mandatory false """
    if request.method == 'GET':
        try:
            project = Project.objects.get(id=id)
            serializer = ProjectSerializer(project)
            if not project.user_email_mandatory:
                user = UserFactory.build(project=project)
                user.save()
                return Response(
                    {
                        **user.refresh_token(),
                        'user_token': user.token,
                        'date_joined': user.date_joined,
                        'user_server': user.active_server,
                        **serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProjectUsersAPI(request, id):

    if request.method == 'GET':
        user_profiles = User.objects.filter(project=id)
        serializer = UserSerializer(user_profiles, many=True)
        return Response(serializer.data)

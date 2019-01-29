from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import mixins

from modelchimp.serializers.profile import ProfileSerializer
from modelchimp.models.profile import Profile
from modelchimp.models.user import User
from modelchimp.serializers.user import UserSerializer

from modelchimp.api_permissions import HasProjectMembership
from rest_framework.permissions import IsAuthenticated


class UserAPI(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)

    def retrieve(self, *args, **kwargs):
        instance = self.get_queryset().get(user=self.request.user.id )
        serializer = self.get_serializer(instance)
        #serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, *args, **kwargs):
        user_profile = self.get_queryset().get(user=self.request.user.id )
        serializer = self.get_serializer(user_profile, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        serializer.save()
        return Response(serializer.data)


class RegisterAPI(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)


    def create(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = user.auth_token.key

        return Response({'token': token})

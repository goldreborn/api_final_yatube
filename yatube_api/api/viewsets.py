from rest_framework.serializers import Serializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class FolowCustom(CreateModelMixin, ListModelMixin, GenericViewSet):

    def perform_create(self, serializer: Serializer) -> Response:
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.following.all()

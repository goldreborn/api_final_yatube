from rest_framework.serializers import Serializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from posts.models import Follow


class FolowCustom(CreateModelMixin, ListModelMixin, GenericViewSet):

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user=self.request.user)

    def get_queryset(self) -> list[Follow]:
        return self.request.user.following.all()

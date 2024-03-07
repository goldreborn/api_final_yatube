from typing import List

from rest_framework.serializers import Serializer
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.viewsets import (
    ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from posts.models import Follow, Post, Group, Comment
from .permissions import OwnershipPermission
from .serializers import (
    FollowSerializer, PostSerializer, GroupSerializer, CommentSerializer
)


User = get_user_model()


class FollowViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    filter_backends = [SearchFilter]
    search_fields = ('user__username', 'following__username')

    def perform_create(self, serializer: Serializer) -> Response:

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        follow = serializer.save(user=self.request.user)

        return Response(
            FollowSerializer(follow).data, status=status.HTTP_201_CREATED
        )

    def get_queryset(self) -> List[Follow]:
        return Follow.objects.all().filter(
            user=get_object_or_404(
                User, username=self.request.user.username
            )
        )


class GroupViewSet(ReadOnlyModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostViewSet(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, OwnershipPermission]
    filter_backends = [SearchFilter]
    filterset_fields = ['group']
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, OwnershipPermission]

    def get_queryset(self) -> List[Comment]:
        return get_object_or_404(
            Post, pk=self.kwargs.get('post_id')
        ).comments.all()

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(
            author=self.request.user, post=get_object_or_404(
                Post, pk=self.kwargs.get('post_id')
            )
        )

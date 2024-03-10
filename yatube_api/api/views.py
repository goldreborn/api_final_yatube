from rest_framework.serializers import Serializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.viewsets import (
    ModelViewSet, ReadOnlyModelViewSet
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet

from posts.models import Post, Group
from .permissions import IsOwnershipPermission
from .serializers import (
    FollowSerializer, PostSerializer, GroupSerializer, CommentSerializer
)
from .viewsets import CreateListViewSet


User = get_user_model()


class FollowViewSet(CreateListViewSet):

    serializer_class = FollowSerializer
    filter_backends = [SearchFilter]
    search_fields = ('user__username', 'following__username')

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(user=self.request.user)

    def get_queryset(self) -> QuerySet:
        return self.request.user.following.all()


class GroupViewSet(ReadOnlyModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]


class PostViewSet(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnershipPermission]
    filter_backends = [SearchFilter]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnershipPermission]

    def create_post(self) -> Post:
        return get_object_or_404(
            Post, pk=self.kwargs.get('post_id')
        )

    def get_queryset(self) -> QuerySet:
        return self.create_post().comments.all()

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(
            author=self.request.user,
            post=self.create_post()
        )

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

from posts.models import Post, Group, Follow
from .permissions import IsOwnershipPermission
from .serializers import (
    FollowSerializer, PostSerializer, GroupSerializer, CommentSerializer
)
from .viewsets import FolowCustom


User = get_user_model()


def create_post(serializer: Serializer, *args, **kwargs) -> None:
    serializer.save(**kwargs)


class FollowViewSet(FolowCustom):

    serializer_class = FollowSerializer
    filter_backends = [SearchFilter]
    search_fields = ('user__username', 'following__username')


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
        create_post(serializer=serializer, author=self.request.user)


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnershipPermission]

    def get_queryset(self) -> QuerySet:
        return get_object_or_404(
            Post, pk=self.kwargs.get('post_id')
        ).comments.all()

    def perform_create(self, serializer: Serializer) -> None:
        create_post(
            serializer=serializer,
            author=self.request.user,
            post=get_object_or_404(
                Post, pk=self.kwargs.get('post_id')
            )
        )

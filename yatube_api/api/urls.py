from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet, GroupViewSet, PostViewSet, CommentViewSet

router_v1 = DefaultRouter()
router_v1.register('follow', FollowViewSet, basename='follow')
router_v1.register('groups', GroupViewSet, basename='group')
router_v1.register('posts', PostViewSet, basename='post')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments(/(?P<comment_id>\d+)/)?',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
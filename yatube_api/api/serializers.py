from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import ForeignKey, CASCADE
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Follow, Group


User = get_user_model()


class FollowSerializer(ModelSerializer):

    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ['user', 'following']
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Вы уже подписаны на этого пользователя',
            )
        ]


class CommentSerializer(ModelSerializer):

    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:

        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)


class PostSerializer(ModelSerializer):

    author = SlugRelatedField(slug_field='username', read_only=True)
    group = ForeignKey(Group, on_delete=CASCADE)

    class Meta:

        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')


class GroupSerializer(ModelSerializer):

    class Meta:

        model = Group
        fields = ('id', 'title', 'slug', 'description')

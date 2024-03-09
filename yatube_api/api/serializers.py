from rest_framework.serializers import (
    ModelSerializer, SlugRelatedField,
    CurrentUserDefault, ReadOnlyField,
    ValidationError, UniqueTogetherValidator
)

from posts.models import Follow, Post, Comment, Group, User


class FollowSerializer(ModelSerializer):

    user = SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=CurrentUserDefault(),
    )
    following = SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:

        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Вы уже подписаны на этого пользователя'
            )
        ]

    def validate_following(self, value):

        if value == self.context["request"].user:
            raise ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return value


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:

        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)


class GroupSerializer(ModelSerializer):

    class Meta:

        model = Group
        fields = ('id', 'title', 'slug', 'description')

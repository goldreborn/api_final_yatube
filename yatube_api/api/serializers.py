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

    def validate_following(self, value):

        if value == self.context["request"].user:
            raise ValidationError()

        return value

    class Meta:

        model = Follow
        fields = ('id', 'user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Вы уже подписаны на этого пользователя'
            )
        ]


class PostSerializer(ModelSerializer):
    author = ReadOnlyField(source="author.username")

    class Meta:

        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')


class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source="author.username")
    post = ReadOnlyField(source="post_id")

    class Meta:

        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class GroupSerializer(ModelSerializer):

    class Meta:

        model = Group
        fields = ('id', 'title', 'slug', 'description')

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подписок.
    """

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Состовная уникальность полей user и following'
            )
        ]

    def validate_following(self, value):
        if value == self.context.get('request').user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return value


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализация группы.
    """

    class Meta:
        model = Group
        fields = (
            '__all__'
        )


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализация поста.
    """

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = (
            '__all__'
        )


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализация комментариев.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            '__all__'
        )
        read_only_fields = (
            'post',
        )

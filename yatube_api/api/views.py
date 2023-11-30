from rest_framework import filters, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import OnlyAuthorDeleteUpdateOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Comment, Follow, Group, Post, User


class CreateListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Кастомный вьюсет для чтения списка или создания объекта.
    """

    pass


class FollowListCreateViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = get_object_or_404(
            User,
            pk=self.request.user.id
        )
        return Follow.objects.filter(
            user=user
        ).all()

    def perform_create(self, serializer):
        """
        Дополнительное добавление поля при сохранении в БД.
        """
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OnlyAuthorDeleteUpdateOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs.get('post_id')
        ).all()

    def perform_create(self, serializer):
        """
        Дополнительное добавление поля при сохранении в БД.
        """
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(
            post=post,
            author=self.request.user
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Операции чтения для групп.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    """
    Все операции CRUD для поста через вьюсет.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OnlyAuthorDeleteUpdateOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """
        Дополнительное добавление поля при сохранении в БД.
        """
        serializer.save(author=self.request.user)

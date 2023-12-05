from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.mixins import CreateListViewSet
from api.permissions import OnlyAuthorDeleteUpdateOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Group, Post


def get_post(pk):
    return get_object_or_404(Post, pk=pk)


class FollowListCreateViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """
        Дополнительное добавление поля при сохранении в БД.
        """
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OnlyAuthorDeleteUpdateOrReadOnly,)

    def get_queryset(self):
        return get_post(self.kwargs.get('post_id')).comments.all()

    def perform_create(self, serializer):
        """
        Дополнительное добавление поля при сохранении в БД.
        """
        serializer.save(
            post=get_post(self.kwargs.get('post_id')),
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

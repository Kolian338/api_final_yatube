from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.mixins import CreateListViewSet
from api.permissions import OnlyAuthorDeleteUpdateOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Group, Post


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
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """
        Дополнительное добавление поля при сохранении в БД.
        """
        serializer.save(
            post=self.get_post(),
            author=self.request.user
        )

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))


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

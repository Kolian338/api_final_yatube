from django.urls import include, path
from rest_framework import routers

from api.views import (CommentViewSet, FollowListCreateViewSet, GroupViewSet,
                       PostViewSet)

router = routers.DefaultRouter()
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comments')
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register('follow', FollowListCreateViewSet, basename='follow')

urls = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]

urlpatterns = [
    path('v1/', include(urls)),
]

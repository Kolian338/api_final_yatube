from django.urls import include, path
from rest_framework import routers

from api.views import (CommentViewSet, FollowListCreateViewSet, GroupViewSet,
                       PostViewSet)

router = routers.DefaultRouter()
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comment')
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowListCreateViewSet, basename='follow')

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
]

from django.urls import include, path
from rest_framework import routers

from api.views import (CommentViewSet, FollowListCreateViewSet, GroupViewSet,
                       PostViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet, basename='comments')
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register('follow', FollowListCreateViewSet, basename='follow')

urls = [
    path('', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(urls)),
]

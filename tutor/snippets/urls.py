from django.urls import path, include
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import SnippetViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)



snippet_list = SnippetViewSet.as_view({
   'get': 'list',
   'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
   'get': 'retrieve',
   'put': 'update',
   'patch': 'partial_update',
   'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
   'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
   'get': 'list'
})
user_detail = UserViewSet.as_view({
   'get': 'retrieve'
})



urlpatterns = [
   path('', include(router.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)

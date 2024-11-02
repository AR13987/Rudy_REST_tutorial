from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status, renderers, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import mixins
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse


from .models import Snippet
from .permissions import IsOwnerOrReadOnly
from .serializers import SnippetSerializer, UserSerializer



# Очень подробно:
# class SnippetList(APIView):
#    """
#    List all snippets, or create a new snippet.
#    """
#
#    def get(self, request, format=None):
#        snippets = Snippet.objects.all()
#        serializer = SnippetSerializer(snippets, many=True)
#        return Response(serializer.data)
#
#    def post(self, request, format=None):
#        serializer = SnippetSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SnippetDetail(APIView):
#    """
#    Retrieve, update or delete a snippet instance.
#    """
#
#    def get_object(self, pk):
#        try:
#            return Snippet.objects.get(pk=pk)
#        except Snippet.DoesNotExist:
#            raise Http404
#
#    def get(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        serializer = SnippetSerializer(snippet)
#        return Response(serializer.data)
#
#    def put(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        serializer = SnippetSerializer(snippet, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        snippet.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)



# Подробно:
# class SnippetList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#
#    def get(self, request, *args, **kwargs):
#        return self.list(request, *args, **kwargs)
#
#    def post(self, request, *args, **kwargs):
#        return self.create(request, *args, **kwargs)
#
#
# class SnippetDetail(mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    generics.GenericAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#
#    def get(self, request, *args, **kwargs):
#        return self.retrieve(request, *args, **kwargs)
#
#    def put(self, request, *args, **kwargs):
#        return self.update(request, *args, **kwargs)
#
#    def delete(self, request, *args, **kwargs):
#        return self.destroy(request, *args, **kwargs)



# Менее детально:
# class SnippetList(generics.ListCreateAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#    def perform_create(self, serializer):
#        serializer.save(owner=self.request.user)
#
#
#
# class SnippetHighlight(generics.GenericAPIView):
#    queryset = Snippet.objects.all()
#    renderer_classes = [renderers.StaticHTMLRenderer]
#
#    def get(self, request, **kwargs):
#        snippet = self.get_object()
#        return Response(snippet.highlighted)
#
#
#
#
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]



# Кратко:
class SnippetViewSet(viewsets.ModelViewSet):
   """
   This viewset automatically provides `list`, `create`, `retrieve`,
   `update` and `destroy` actions.

   Additionally we also provide an extra `highlight` action.
   """
   queryset = Snippet.objects.all()
   serializer_class = SnippetSerializer
   permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                         IsOwnerOrReadOnly]

   @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
   def highlight(self, request, *args, **kwargs):
       snippet = self.get_object()
       return Response(snippet.highlighted)

   def perform_create(self, serializer):
       serializer.save(owner=self.request.user)



# Create your views here.
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
   """
   List all code snippets, or create a new snippet.
   """
   if request.method == 'GET':
       snippets = Snippet.objects.all()
       serializer = SnippetSerializer(snippets, many=True)
       return Response(serializer.data)

   elif request.method == 'POST':
       serializer = SnippetSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
   """
   Retrieve, update or delete a code snippet.
   """
   try:
       snippet = Snippet.objects.get(pk=pk)
   except Snippet.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)

   if request.method == 'GET':
       serializer = SnippetSerializer(snippet)
       return Response(serializer.data)
   elif request.method == 'PUT':
       serializer = SnippetSerializer(snippet, data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   elif request.method == 'DELETE':
       snippet.delete()
       return Response(status=status.HTTP_204_NO_CONTENT)


# Подробно:
# class UserList(generics.ListAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer



# Кратко:
class UserViewSet(viewsets.ReadOnlyModelViewSet):
   """
   This viewset automatically provides `list` and `retrieve` actions.
   """
   queryset = User.objects.all()
   serializer_class = UserSerializer

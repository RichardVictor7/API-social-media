from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from rest_framework import status, generics
from rest_framework.views import APIView
# Create your views here.

class GetPostOrAddPost(APIView):
    def get(self,request, id_post):
        post = get_object_or_404(Post, id=id_post)

        serializer = PostSerializer(post)

        return Response(serializer.data)
    
    def post(self,request):
        data = request.data

        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteOrUpdatePost(APIView):
    def put(self, request, id_post):
        data = request.data
        post = get_object_or_404(Post,id=id_post)

        serializer = PostSerializer(post, data=data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id_post):

        post = get_object_or_404(Post, id = id_post)

        post.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    
class FeedPosts(generics.ListAPIView):
    """
    Retorna todos os posts com paginação.
    """
    queryset = Post.objects.all().order_by('-data_criacao')
    serializer_class = PostSerializer
    # A classe de paginação é herdada automaticamente das configurações (settings.py)
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer, PostLikeSerializer
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
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
    
class FeedPosts(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        posts = Post.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class PostLikeView(APIView):
    """View para toggle de likes em posts"""
    
    def post(self, request, id_post):
        """Toggle do status de like (true/false)"""
        post = get_object_or_404(Post, id=id_post)
        
        serializer = PostLikeSerializer(post, data={})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'id': post.id,
                'liked': post.liked,
                'message': f'Post {"curtido" if post.liked else "descurtido"} com sucesso!'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id_post):
        """Obter status atual do like"""
        post = get_object_or_404(Post, id=id_post)
        
        return Response({
            'id': post.id,
            'liked': post.liked
        })
from rest_framework import viewsets, permissions, filters, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

from rest_framework import generics

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get users that the current user follows
        following_users = self.request.user.following.all()
        # Return posts from those users, ordered by creation date (newest first)
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """Like a post"""
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already liked
        if Like.objects.filter(post=post, user=request.user).exists():
            return Response(
                {'error': 'You have already liked this post'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create like
        like = Like.objects.create(post=post, user=request.user)
        
        # Create notification (simplified - would need notifications app import)
        # In a real app: create_notification(post.author, request.user, 'like', post)
        
        return Response({
            'message': 'Post liked successfully',
            'like_id': like.id,
            'likes_count': post.likes.count()
        }, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        """Unlike a post"""
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete like if exists
        deleted_count, _ = Like.objects.filter(post=post, user=request.user).delete()
        
        if deleted_count > 0:
            return Response({
                'message': 'Post unliked successfully',
                'likes_count': post.likes.count()
            })
        else:
            return Response(
                {'error': 'You have not liked this post'},
                status=status.HTTP_400_BAD_REQUEST
            )

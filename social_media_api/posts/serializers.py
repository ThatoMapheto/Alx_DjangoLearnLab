from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_at', 'updated_at', 'post')
        read_only_fields = ('author', 'created_at', 'updated_at')

class PostSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comments_count')
        read_only_fields = ('author', 'created_at', 'updated_at')
    
    def get_comments_count(self, obj):
        return obj.comments.count()

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content')

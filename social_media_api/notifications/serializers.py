from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSimpleSerializer(read_only=True)
    verb_display = serializers.CharField(source='get_verb_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = ('id', 'actor', 'verb', 'verb_display', 'target_object_id', 'read', 'timestamp')
        read_only_fields = ('id', 'actor', 'verb', 'target_object_id', 'timestamp')

from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()
    secret_token = serializers.CharField()
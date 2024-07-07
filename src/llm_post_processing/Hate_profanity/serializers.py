from rest_framework import serializers


class CommentSerializer(serializers.Serializer):
    input_text = serializers.CharField(max_length=1000)

from rest_framework import serializers

class InputTextSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)

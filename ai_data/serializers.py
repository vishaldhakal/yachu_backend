from rest_framework import serializers

from .models import AIData


class AIDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIData
        fields = "__all__"

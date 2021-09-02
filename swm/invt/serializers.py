from .models import WasteML
from rest_framework import serializers


class WasteMLEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteML


class WasteMLListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteML
        fields = '__all__'
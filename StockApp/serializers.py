# stockdata/serializers.py
from rest_framework import serializers
from .models import FyersToken

class FyersTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FyersToken
        fields = '__all__'

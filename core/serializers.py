# core/serializers.py
from rest_framework import serializers
from .models import Pharmacy

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ['name', 'address', 'phone', 'latitude', 'longitude']

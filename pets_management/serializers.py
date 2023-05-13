from rest_framework import serializers
from pets_management.models import Pet


class PetsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('name', 'device_no', 'icon')
        depth = 2


class PetsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'
        depth = 2

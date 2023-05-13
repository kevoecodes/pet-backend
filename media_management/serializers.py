from rest_framework import serializers
from media_management.models import Media


class MediaPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ('name', 'uuid_name', 'extension')


class MediaGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = '__all__'
        depth = 1

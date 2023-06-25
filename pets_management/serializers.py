from rest_framework import serializers
from pets_management.models import Pet, PetLocation, PetGeofenceCoord


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


class PetLocationsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetLocation
        fields = '__all__'
        depth = 2


class PetLocationPostSerializer(serializers.Serializer):
    device_number = serializers.CharField(max_length=255)
    longitudes = serializers.FloatField()
    latitudes = serializers.FloatField()

    def create(self, validated_data):
        device_number = validated_data.pop('device_number')
        pet_location = PetLocation.objects.create(**validated_data)
        return pet_location

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        try:
            pet = Pet.objects.get(device_no=data['device_number'])
        except Pet.DoesNotExist:
            raise serializers.ValidationError('Device number unknown')

        return data


class PetGeofenceCoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetGeofenceCoord
        fields = ['longitudes', 'latitudes']


class PetGeofencePostSerializer(serializers.Serializer):
    points = serializers.ListField(
        child=PetGeofenceCoordSerializer(),
        min_length=4,
        max_length=20
    )

    def create(self, validated_data):
        pet = validated_data.pop('pet')
        prev_points = PetGeofenceCoord.objects.filter(pet_id=pet.id)
        for p in prev_points:
            p.delete()
        points = validated_data.pop('points')
        geofence = []
        for point in points:
            geofence.append(PetGeofenceCoord.objects.create(pet=pet, **point))
        print(geofence)
        return geofence

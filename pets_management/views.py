from rest_framework import status, generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from pet_backend.utils.common import StandardResultsSetPagination
from pets_management.models import Pet, PetLocation
from pets_management.serializers import PetsListSerializer, PetsPostSerializer, PetLocationsListSerializer, \
    PetLocationPostSerializer
from pets_management.sockets.managers import PetTrackChannel


class PetsView(APIView):

    @staticmethod
    def get(request):
        pets = Pet.objects.all()
        return Response(
            PetsListSerializer(instance=pets, many=True).data
        )

    @staticmethod
    def post(request):
        serializer = PetsPostSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save(created_by=request.user)
            return Response({
                "status": True,
                "data": PetsListSerializer(instance=obj, many=False).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PetDetail(APIView):

    @staticmethod
    def get(request, pk):
        try:
            pet = Pet.objects.get(id=pk)
        except Pet.DoesNotExist:
            return Response("Pet not found", status=status.HTTP_404_NOT_FOUND)

        return Response(
            PetsListSerializer(instance=pet, many=False).data
        )

    @staticmethod
    def put(request, pk):
        try:
            pet = Pet.objects.get(id=pk)
        except Pet.DoesNotExist:
            return Response("Pet not found", status=status.HTTP_404_NOT_FOUND)

        serializer = PetsPostSerializer(instance=pet, data=request.data)
        if serializer.is_valid():
            obj = serializer.save(created_by=request.user)
            return Response({
                "status": True,
                "data": PetsListSerializer(instance=obj, many=False).data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        try:
            pet = Pet.objects.get(id=pk)
        except Pet.DoesNotExist:
            return Response("Pet not found", status=status.HTTP_404_NOT_FOUND)

        pet.delete()

        return Response('Pet deleted successfully')


class ListPets(generics.ListAPIView):
    search_fields = ['name', 'created_by__first_name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PetsListSerializer
    queryset = Pet.objects.all().order_by('-created_at')
    pagination_class = StandardResultsSetPagination


class PetsLocationView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        pet_locations = PetLocation.objects.all()
        return Response(
            PetLocationsListSerializer(instance=pet_locations, many=True).data
        )

    @staticmethod
    def post(request):
        serializer = PetLocationPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save(pet=Pet.objects.get(device_no=serializer.validated_data['device_number']))
            data = PetLocationsListSerializer(instance=obj, many=False).data
            PetTrackChannel(data)
            return Response({
                "status": True,
                "data": data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListPetLocations(generics.ListAPIView):
    search_fields = ['pet__name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PetLocationsListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = PetLocation.objects.all()
            pet_id = self.request.GET.get('pet_id', None)

            if pet_id is not None:
                queryset = queryset.filter(pet_id=pet_id)

            return queryset
        return []


from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from pet_backend.utils.common import StandardResultsSetPagination
from pets_management.models import Pet
from pets_management.serializers import PetsListSerializer, PetsPostSerializer


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


class ListPets(generics.ListAPIView):
    search_fields = ['name', 'created_by__first_name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PetsListSerializer
    queryset = Pet.objects.all().order_by('-created_at')
    pagination_class = StandardResultsSetPagination

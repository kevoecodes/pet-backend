from django.urls import path, re_path
from pets_management.views import PetsView, ListPets, PetDetail, PetsLocationView, ListPetLocations, GoogleApiKey, CreatePetGeofence

urlpatterns = [
    path('pets', PetsView.as_view(), name='pets-CRUD'),
    path('pet/<str:pk>', PetDetail.as_view(), name='pets-CRUD'),
    re_path(r'^list-pets/$', ListPets.as_view(), name='list-PETS'),

    re_path(r'^list-pet-locations/$', ListPetLocations.as_view(), name='list-pet-locations'),
    path('pet-location', PetsLocationView.as_view(), name='Pet-location'),
    path('create-pet-geofence/<str:pk>', CreatePetGeofence.as_view(), name='Google Api Key'),

    path('google-api=key', GoogleApiKey.as_view(), name='Google-Api Key')
]

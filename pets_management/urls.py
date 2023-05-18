from django.urls import path, re_path
from pets_management.views import PetsView, ListPets, PetDetail

urlpatterns = [
    path('pets', PetsView.as_view(), name='pets-CRUD'),
    path('pet/<str:pk>', PetDetail.as_view(), name='pets-CRUD'),
    re_path(r'^list-pets/$', ListPets.as_view(), name='list-PETS')
]

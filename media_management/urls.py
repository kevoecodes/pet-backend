from django.urls import path

from media_management.views import UploadImage

urlpatterns = [
    path('upload-image', UploadImage.as_view(), name='pets-CRUD'),
]

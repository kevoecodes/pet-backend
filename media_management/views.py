import os
import uuid
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from pet_backend.utils.constants import Constant
from media_management.serializers import MediaPostSerializer


class UploadImage(APIView):
    permission_classes = [AllowAny]
    parser_classes = [FormParser, MultiPartParser]

    @staticmethod
    def saveFile(file, name):
        try:
            fout = open(os.path.join(Constant.image_path, name), 'wb+')
            file_content = ContentFile(file.read())
            for chunk in file_content.chunks():
                fout.write(chunk)
            fout.close()
            return True, "Success"
        except Exception as e:
            return False, e

    def post(self, request, *args, **kwargs):
        if 'image' in request.FILES:
            file_obj = request.data['image']
            file_name = file_obj.name
            split_file_name = os.path.splitext(file_name)
            file_extension = split_file_name[1].lower()
            serializer = MediaPostSerializer(data={
                'name': str(file_name),
                'uuid_name': f'{uuid.uuid4()}{file_extension}',
                'extension': split_file_name[1].lower(),
            })

            if serializer.is_valid():
                media = serializer.save()
                res, message = self.saveFile(file_obj, media.uuid_name)

                if res:
                    return Response({"status": True, "name": media.uuid_name})

                return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("Image not provided", status=400)

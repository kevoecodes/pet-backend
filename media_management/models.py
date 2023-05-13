from django.db import models


class Extensions:
    PDF = '.pdf'
    PNG = '.png'
    JPG = '.jpg'
    JPEG = '.jpeg'
    DOCX = '.docx'
    DOC = '.doc'

    ALLOWED = [PDF, PNG, JPEG, DOCX, DOC, JPG]


class Media(models.Model):

    EXTENSIONS = (
        (Extensions.PDF, f'{Extensions.PDF} Extension'),
        (Extensions.JPG, f'{Extensions.JPG} Extension'),
        (Extensions.JPEG, f'{Extensions.JPEG} Extension'),
        (Extensions.PNG, f'{Extensions.PNG} Extension'),
        (Extensions.DOCX, f'{Extensions.DOCX} Extension'),
        (Extensions.DOC, f'{Extensions.DOC} Extension'),
    )

    name = models.CharField(max_length=255)
    uuid_name = models.CharField(max_length=255)

    extension = models.CharField(choices=EXTENSIONS)

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


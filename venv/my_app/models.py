from django.db import models


class Document(models.Model):
    uploadedFile = models.ImageField(upload_to = "Uploaded_Files/")
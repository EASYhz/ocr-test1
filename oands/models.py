from django.db import models
# from cloudinary.models import CloudinaryField

# Create your models here.
class Ocr(models.Model):
    # image = models.ImageField(upload_to='images/')
    # title=models.CharField(max_length=500)
    # image=CloudinaryField('image')
    image = models.BinaryField(max_length=100)

class Meta:
    model = Ocr
    fields = ['image']

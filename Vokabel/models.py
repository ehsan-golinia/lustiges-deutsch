from django.db import models

# Create your models here.


class Vokabel(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    german = models.CharField(max_length=100)
    english = models.CharField(max_length=100)
    turkish = models.CharField(max_length=100)

    def __str__(self):
        return f'#{self.id} - {self.german} - {self.english}'


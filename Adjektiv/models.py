from django.db import models

# Create your models here.


class Adjektiv(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    english = models.CharField(max_length=100)
    turkish = models.CharField(max_length=100)
    positiv = models.CharField(max_length=100)
    komparativ = models.CharField(max_length=100)
    superlativ = models.CharField(max_length=100)

    def __str__(self):
        return f'#{self.id} - {self.english} - {self.positiv}'

    class Meta:
        verbose_name = "Adjektiv"
        verbose_name_plural = "Adjektiv"
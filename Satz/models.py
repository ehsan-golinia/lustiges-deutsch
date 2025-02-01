from django.db import models

# Create your models here.


class Satz(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    english = models.CharField(max_length=200)
    turkish = models.CharField(max_length=200)
    german = models.CharField(max_length=200)

    def __str__(self):
        return f'#{self.id}'

    class Meta:
        verbose_name = "Satz"
        verbose_name_plural = "Satz"

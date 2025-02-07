from django.db import models

# Create your models here.


class KI(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    english = models.CharField(max_length=300)
    turkish = models.CharField(max_length=300)
    german = models.CharField(max_length=300)

    def __str__(self):
        return f'#{self.id} - {self.english} - {self.german}'

    class Meta:
        verbose_name = "KI"
        verbose_name_plural = "KI"

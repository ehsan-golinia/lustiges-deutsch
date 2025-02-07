from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class Zahlen(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    number = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    german = models.CharField(max_length=300)

    def __str__(self):
        return f'#{self.id} - {self.number}'

    class Meta:
        verbose_name = "Zahlen"
        verbose_name_plural = "Zahlen"

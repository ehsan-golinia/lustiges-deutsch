from django.db import models
from Vokabel.models import Vokabel

# Create your models here.


class SingularPlural(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    vokabel = models.ForeignKey(Vokabel, on_delete=models.CASCADE, related_name='singular_plural')
    singular = models.CharField(max_length=100)
    plural = models.CharField(max_length=100)

    def __str__(self):
        return f'Singular: {self.singular}, Plural: {self.plural}'

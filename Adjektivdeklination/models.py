from django.db import models

# Create your models here.


class Adjektivdeklination(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    english = models.CharField(max_length=100)
    turkish = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    def __str__(self):
        return f'#{self.id} - {self.english} - {self.turkish}'


class AdjKasus(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    adjDek = models.ForeignKey(Adjektivdeklination, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100, null=True)
    akk = models.CharField(max_length=100, null=True)
    dat = models.CharField(max_length=100, null=True)
    gen = models.CharField(max_length=100, null=True)


    def __str__(self):
        return f'#{self.id} - {self.nom}'

    class Meta:
        verbose_name = "Adjektiv Kasus"
        verbose_name_plural = "Adjektiv Kasus"

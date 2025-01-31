from django.db import models

# Create your models here.

class Verb(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    level = models.CharField(max_length=20)
    infinitiv = models.CharField(max_length=100)
    english = models.CharField(max_length=100)
    turkish = models.CharField(max_length=100)

    def __str__(self):
        return f'#{self.id} - {self.infinitiv}'

    class Meta:
        verbose_name = "Verb"  # Singular name
        verbose_name_plural = "Verb"  # Plural name without 's'


class Praesens(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    verb = models.ForeignKey(Verb, on_delete=models.CASCADE, related_name='praesens')
    ich = models.CharField(max_length=100, null=True, blank=True)
    du = models.CharField(max_length=100, null=True, blank=True)
    er_sie_es = models.CharField(max_length=100, null=True, blank=True)
    wir = models.CharField(max_length=100, null=True, blank=True)
    ihr = models.CharField(max_length=100, null=True, blank=True)
    sie_Sie = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'#{self.id} - {self.verb.infinitiv} - {self.sie_Sie}'

    class Meta:
        verbose_name = "Präsens"  # Singular name
        verbose_name_plural = "Präsens"  # Plural name without 's'


class Praeteritum(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    verb = models.ForeignKey(Verb, on_delete=models.CASCADE, related_name='praeteritum')
    ich = models.CharField(max_length=100, null=True, blank=True)
    du = models.CharField(max_length=100, null=True, blank=True)
    er_sie_es = models.CharField(max_length=100, null=True, blank=True)
    wir = models.CharField(max_length=100, null=True, blank=True)
    ihr = models.CharField(max_length=100, null=True, blank=True)
    sie_Sie = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'#{self.id} - {self.verb.infinitiv} - {self.sie_Sie}'

    class Meta:
        verbose_name = "Präteritum"  # Singular name
        verbose_name_plural = "Präteritum"  # Plural name without 's'


class Perfekt(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    verb = models.ForeignKey(Verb, on_delete=models.CASCADE, related_name='perfekt')
    partizip_ii = models.CharField(max_length=100, null=True, blank=True)
    ich = models.CharField(max_length=100, null=True, blank=True)
    du = models.CharField(max_length=100, null=True, blank=True)
    er_sie_es = models.CharField(max_length=100, null=True, blank=True)
    wir = models.CharField(max_length=100, null=True, blank=True)
    ihr = models.CharField(max_length=100, null=True, blank=True)
    sie_Sie = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'#{self.id} - {self.verb.infinitiv} - {self.partizip_ii}'

    class Meta:
        verbose_name = "Perfekt"  # Singular name
        verbose_name_plural = "Perfekt"  # Plural name without 's'


class Futur_I(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    verb = models.ForeignKey(Verb, on_delete=models.CASCADE, related_name='futur_i')
    ich = models.CharField(max_length=100, null=True, blank=True)
    du = models.CharField(max_length=100, null=True, blank=True)
    er_sie_es = models.CharField(max_length=100, null=True, blank=True)
    wir = models.CharField(max_length=100, null=True, blank=True)
    ihr = models.CharField(max_length=100, null=True, blank=True)
    sie_Sie = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'#{self.id} - {self.verb.infinitiv} - {self.sie_Sie}'

    class Meta:
        verbose_name = "Futur I"  # Singular name
        verbose_name_plural = "Futur I"  # Plural name without 's'


class Konjunktiv_II(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    verb = models.ForeignKey(Verb, on_delete=models.CASCADE, related_name='konjunktiv_ii')
    ich = models.CharField(max_length=100, null=True, blank=True)
    du = models.CharField(max_length=100, null=True, blank=True)
    er_sie_es = models.CharField(max_length=100, null=True, blank=True)
    wir = models.CharField(max_length=100, null=True, blank=True)
    ihr = models.CharField(max_length=100, null=True, blank=True)
    sie_Sie = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'#{self.id} - {self.verb.infinitiv} - {self.sie_Sie}'

    class Meta:
        verbose_name = "Konjunktiv II"  # Singular name
        verbose_name_plural = "Konjunktiv II"  # Plural name without 's'
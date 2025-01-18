from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_scores = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        default='profile_images/user-photo.png'  # Path to the default image
    )

    def __str__(self):
        return f"{self.user.username}"


class GamesRecords(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_records')
    game_name = models.CharField(default='', max_length=100)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.score} - {self.date}'


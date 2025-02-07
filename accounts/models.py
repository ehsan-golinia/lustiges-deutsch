from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        default='profile_images/user-photo.png'  # Path to the default image
    )

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class UserScores(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='scores')
    vokabel_score = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    singular_plural_score = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    artikel_score = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    adjektiv_score = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    adjektiv_deklination_score = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    verb_score = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    present_verb_score = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    past_verb_score = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    partizip_II_score = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    satz_score = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])
    zahlen_score = models.IntegerField(default=0, validators=[MinValueValidator(0, message="Total scores must be 0 or greater.")])

    def __str__(self):
        return f"{self.user.username}"

    def total_scores(self):
        return sum([
            self.vokabel_score,
            self.singular_plural_score,
            self.artikel_score,
            self.adjektiv_score,
            self.adjektiv_deklination_score,
            self.verb_score,
            self.present_verb_score,
            self.past_verb_score,
            self.partizip_II_score,
            self.satz_score,
            self.zahlen_score
        ])

    class Meta:
        verbose_name = "User Score"
        verbose_name_plural = "User Scores"


class GamesRecords(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_records')
    game_name = models.CharField(default='', max_length=100)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.score} - {self.date}'

    class Meta:
        verbose_name = "Games Records"
        verbose_name_plural = "Games Records"


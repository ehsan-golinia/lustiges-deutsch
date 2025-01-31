from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserScores, UserProfile


@receiver(post_save, sender=UserScores)
def update_total_scores(sender, instance, **kwargs):
    # Calculate the total score from UserScores
    total = (
        instance.vokabel_score +
        instance.singular_plural_score +
        instance.artikel_score +
        instance.adjektiv_score +
        instance.adjektiv_deklination_score +
        instance.verb_score +
        instance.present_verb_score +
        instance.past_verb_score +
        instance.partizip_II_score
    )

    # Update the UserProfile's total_scores field
    user_profile, created = UserProfile.objects.get_or_create(user=instance.user)
    user_profile.total_scores = total
    user_profile.save()

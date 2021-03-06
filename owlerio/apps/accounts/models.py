from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from preferences.models import Preference

class Profile(models.Model):

    user = models.OneToOneField(User, related_name='profile')
    preference = models.OneToOneField(Preference, related_name='profile')

    def save(self, *args, **kwargs):
        try:
            preference = self.preference
        except Preference.DoesNotExist:
            self.preference = Preference.objects.create(
                    track_request=Preference.CHOICES.disabled,
                    track_response=Preference.CHOICES.disabled,
                    email_errors=Preference.CHOICES.enabled,
                    signature=Preference.CHOICES.disabled,
                    signature_text="Sent from owler.io",
                    )
        super(Profile, self).save(*args, **kwargs)


class Email(models.Model):

    user = models.ForeignKey(User, related_name='emails')
    email = models.EmailField(unique=True)


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created and not instance.pk == 1:
        Profile.objects.create(user=instance)


import requests
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile  # import your profile model

MAKE_WEBHOOK_URL = 'https://hook.eu2.make.com/x6lroqwbh3syg2ba08b9n872iyu9rjbr'


@receiver(post_save, sender=User)
def trigger_welcome_mail(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        # Get or create the profile for this user
        profile, _ = UserProfile.objects.get_or_create(user=instance)

        if not profile.welcome_email_sent:
            try:
                # Send webhook to Make.com
                requests.post(MAKE_WEBHOOK_URL, json={
                    'id': instance.id,
                    'email': instance.email,
                    'name': instance.get_full_name(),
                })
                print(f"[Webhook Triggered] for {instance.email}")

                # Update the profile field
                profile.welcome_email_sent = True
                profile.save()

            except Exception as e:
                print(f"[Webhook Error] {e}")

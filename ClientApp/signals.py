# signals.py

import requests
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

MAKE_WEBHOOK_URL = 'https://hook.eu2.make.com/13p5foepmloe5w679z2psu50xqclzg8q'
@receiver(post_save, sender=User)
def trigger_welcome_email(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        if not instance.welcome_email_sent:
            payload = {
                'id': instance.id,
                'email': instance.email,
                'name': instance.get_full_name()
            }
            try:
                response = requests.post(MAKE_WEBHOOK_URL, json=payload)
                print(f"[Webhook Sent] {instance.email} | Status: {response.status_code}")
            except Exception as e:
                print(f"[Webhook Failed] {e}")

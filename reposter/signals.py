from .models import event_post, event_toPost
from django.db.models.signals import post_save
from django.dispatch import receiver

# When an event is created, it gets marked onto the repost cache
@receiver(post_save, sender=event_post)
def mark_post(sender, instance, created, **kwargs):
    if created:
        event_toPost.objects.create(event=instance)

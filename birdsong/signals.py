from datetime import date, timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from birdsong.conf import BIRDSONG_DOUBLE_OPT_IN_ENABLED
from birdsong.models import Campaign, Contact


@receiver(post_save)
def clean_unconfirmed_contacts(sender, instance, created, **kwargs):
    if issubclass(sender, Campaign) & BIRDSONG_DOUBLE_OPT_IN_ENABLED == True:
        Contact.objects.filter(
            created_at__lt=date.today() - timedelta(weeks=1), is_confirmed=False
        ).delete()

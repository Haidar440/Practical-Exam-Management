from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User,Group
from .models import Allocation_Record
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.sessions.models import Session



def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="examiners")
        instance.groups.add(group)
        obj = Allocation_Record.objects.latest('id')
        obj.user = instance
        obj.save()
    print("Profile Created")

post_save.connect(customer_profile, sender=User)

@receiver(post_delete,sender=User)
def user_deleted(sender,instance,**kwargs):
      # Get all active sessions for the user
    user_sessions = Session.objects.filter(
        expire_date__gte=timezone.now(),
        session_data__contains=str(instance.id)  # Searching for user ID in session data
    )

    # Delete the sessions related to the deleted user
    for session in user_sessions:
        session_data = session.get_decoded()
        # Check if the user ID exists in the session data and delete the session
        if instance.id in session_data.get('_auth_user_id'):
            session.delete()
    
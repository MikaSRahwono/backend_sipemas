from django.dispatch import receiver, Signal

from api.academic.models import ActivityStep
from api.activity.models import Activity, StepCompletion

activity_complete_step = Signal()
@receiver(activity_complete_step)
def handle_activity_completed_signal(sender, activity, user,  **kwargs):
    activity = Activity.objects.get(id=activity.id)
    complete_steps = StepCompletion.objects.filter(activity=activity)
    activity_steps = ActivityStep.objects.filter(course=activity.course)

    if len(complete_steps) == len(activity_steps):
        activity.is_completed = True
        activity.save()
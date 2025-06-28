from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .models import CustomSession, SessionFeedback, SessionMaterial
from .notifications import notify_users

@receiver(post_save, sender=CustomSession)
def customsession_status_signal(sender, instance, created, **kwargs):
    users = [instance.tutor_or_guide, instance.learner_or_visitor]
    topic = instance.topic_or_location
    session_type = instance.get_session_type_display()
    if created:
        message = _("A new {typ} session about '{topic}' has been scheduled.").format(
            typ=session_type, topic=topic)
        notify_users(users, message, subject=_("Session scheduled: {topic}").format(topic=topic))
    else:
        if instance.status == "confirmed":
            message = _("Session '{topic}' has been confirmed.").format(topic=topic)
            notify_users(users, message, subject=_("Session confirmed: {topic}").format(topic=topic))
        elif instance.status == "in_progress":
            message = _("Session '{topic}' is now in progress.").format(topic=topic)
            notify_users(users, message, subject=_("Session in progress: {topic}").format(topic=topic))
        elif instance.status == "completed":
            message = _("Session '{topic}' has been completed.").format(topic=topic)
            notify_users(users, message, subject=_("Session completed: {topic}").format(topic=topic))
        elif instance.status == "cancelled":
            message = _("Session '{topic}' has been cancelled.").format(topic=topic)
            notify_users(users, message, subject=_("Session cancelled: {topic}").format(topic=topic))
        elif instance.status == "no_show":
            message = _("Session '{topic}' marked as no-show.").format(topic=topic)
            notify_users(users, message, subject=_("Session no-show: {topic}").format(topic=topic))

@receiver(post_save, sender=SessionFeedback)
def session_feedback_signal(sender, instance, created, **kwargs):
    if created:
        session = instance.session
        users = [session.tutor_or_guide, session.learner_or_visitor]
        topic = session.topic_or_location
        message = _("A new feedback was submitted for '{topic}'.").format(topic=topic)
        notify_users(users, message, subject=_("Feedback for session: {topic}").format(topic=topic))

@receiver(post_save, sender=SessionMaterial)
def session_material_signal(sender, instance, created, **kwargs):
    if created:
        session = instance.session
        users = [session.tutor_or_guide, session.learner_or_visitor]
        message = _("New material '{title}' uploaded for session '{topic}'.").format(
            title=instance.title, topic=session.topic_or_location)
        notify_users(users, message, subject=_("Material added: {title}").format(title=instance.title))

@receiver(post_delete, sender=SessionMaterial)
def session_material_delete_signal(sender, instance, **kwargs):
    session = instance.session
    users = [session.tutor_or_guide, session.learner_or_visitor]
    message = _("Material '{title}' was removed from session '{topic}'.").format(
        title=instance.title, topic=session.topic_or_location)
    notify_users(users, message, subject=_("Material removed: {title}").format(title=instance.title))
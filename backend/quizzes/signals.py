from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from notifications.tasks import notify_user

def get_quiz_result_model():
    return apps.get_model('quizzes', 'UserQuizProgress')

@receiver(post_save, sender=None)
def notify_learner_quiz_result(sender, instance, created, **kwargs):
    QuizResult = get_quiz_result_model()
    if sender is QuizResult and created:
        notify_user.delay(
            user_id=instance.learner.id,
            subject="Quiz Result Available",
            message=f"You scored {instance.score} on quiz: {instance.quiz.title}",
            in_app_title="Quiz Result",
            in_app_type="success",
            link="/dashboard/learner/quizzes/"
        )

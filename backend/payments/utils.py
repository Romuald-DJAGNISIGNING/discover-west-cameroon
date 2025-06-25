from .models import Payment
from tutorials.models import Tutorial, TutorialEnrollment
from notifications.tasks import notify_user
from django.contrib.auth import get_user_model

User = get_user_model()

def mark_tutorial_payment_complete(payment):
    if payment.purpose == "tutorial":
        tutorial = Tutorial.objects.get(id=payment.related_object_id)
        TutorialEnrollment.objects.create(
            tutorial=tutorial,
            learner=payment.payer,
            paid=True
        )

        # Notify learner and admin
        notify_user.delay(
            user_id=payment.payer.id,
            subject="Tutorial Purchase Confirmed",
            message=f"You've gained access to: {tutorial.title}.",
            in_app_title="Tutorial Access Granted",
            in_app_type="success",
            link="/dashboard/learner/tutorials/"
        )

        for admin in User.objects.filter(is_staff=True):
            notify_user.delay(
                user_id=admin.id,
                subject="Tutorial Purchased",
                message=f"{payment.payer} purchased tutorial {tutorial.title}.",
                in_app_title="New Purchase",
                in_app_type="info",
                link="/admin/payments/"
            )


def create_payment_for_tutorial(user, tutorial):
    return Payment.objects.create(
        payer=user,
        amount=tutorial.price,
        purpose="tutorial",
        related_object_id=tutorial.id,
        status="pending"  # update to "completed" later
    )

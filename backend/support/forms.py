from django import forms
from .models import SupportTicket, SupportMessage

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ["subject", "message", "priority", "village", "attraction", "festival"]

class SupportMessageForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ["message", "attachment"]
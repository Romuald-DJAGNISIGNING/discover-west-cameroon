from django import forms
from .models import Tutorial, TutorialComment

class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = [
            "title", "category", "description", "content", "video_url", "pdf_file",
            "image", "village", "attraction", "festival", "is_published"
        ]

class TutorialCommentForm(forms.ModelForm):
    class Meta:
        model = TutorialComment
        fields = ["comment"]
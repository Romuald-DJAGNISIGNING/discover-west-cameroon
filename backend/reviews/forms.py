from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "title", "content", "village", "attraction", "festival", "hosting_family", "social_immersion"]
        widgets = {
            "rating": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "village": forms.Select(attrs={"class": "form-select"}),
            "attraction": forms.Select(attrs={"class": "form-select"}),
            "festival": forms.Select(attrs={"class": "form-select"}),
            "hosting_family": forms.Select(attrs={"class": "form-select"}),
            "social_immersion": forms.Select(attrs={"class": "form-select"}),
        }
from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'type', 'title', 'description', 'village',
            'attraction', 'festival'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'village': forms.Select(attrs={'class': 'form-select'}),
            'attraction': forms.Select(attrs={'class': 'form-select'}),
            'festival': forms.Select(attrs={'class': 'form-select'}),
        }

class ReportReviewForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['status', 'resolution_comment']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'resolution_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
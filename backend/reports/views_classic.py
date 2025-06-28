from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Report
from .forms import ReportForm, ReportReviewForm

@login_required
def report_list(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, "reports/report_list.html", {"reports": reports})

@login_required
def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, "reports/report_detail.html", {"report": report})

@login_required
def report_create(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            report.save()
            return redirect("report_detail", pk=report.pk)
    else:
        form = ReportForm()
    return render(request, "reports/report_form.html", {"form": form})

@login_required
def report_edit(request, pk):
    report = get_object_or_404(Report, pk=pk, reported_by=request.user)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect("report_detail", pk=report.pk)
    else:
        form = ReportForm(instance=report)
    return render(request, "reports/report_form.html", {"form": form, "edit": True})

@user_passes_test(lambda u: u.is_superuser or getattr(u, "role", None) in ("admin", "tutor", "guide"))
def report_review(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = ReportReviewForm(request.POST, instance=report)
        if form.is_valid():
            reviewed = form.save(commit=False)
            reviewed.reviewed_by = request.user
            reviewed.save()
            return redirect("report_detail", pk=report.pk)
    else:
        form = ReportReviewForm(instance=report)
    return render(request, "reports/report_review_form.html", {"form": form, "report": report})
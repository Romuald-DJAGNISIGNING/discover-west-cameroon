from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tutorial, TutorialComment
from .forms import TutorialForm, TutorialCommentForm

@login_required
def tutorial_list(request):
    tutorials = Tutorial.objects.filter(is_published=True).order_by('-created_at')
    return render(request, "tutorials/tutorial_list.html", {"tutorials": tutorials})

@login_required
def tutorial_detail(request, pk):
    tutorial = get_object_or_404(Tutorial, pk=pk)
    comments = tutorial.comments.all().order_by('created_at')
    comment_form = TutorialCommentForm()
    if request.method == "POST":
        comment_form = TutorialCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.tutorial = tutorial
            comment.user = request.user
            comment.save()
            return redirect("tutorial_detail", pk=tutorial.pk)
    return render(request, "tutorials/tutorial_detail.html", {"tutorial": tutorial, "comments": comments, "comment_form": comment_form})

@user_passes_test(lambda u: getattr(u, "role", None) in ("tutor", "guide", "admin") or u.is_superuser)
def tutorial_create(request):
    if request.method == "POST":
        form = TutorialForm(request.POST, request.FILES)
        if form.is_valid():
            tutorial = form.save(commit=False)
            tutorial.created_by = request.user
            tutorial.save()
            return redirect("tutorial_detail", pk=tutorial.pk)
    else:
        form = TutorialForm()
    return render(request, "tutorials/tutorial_form.html", {"form": form})

@user_passes_test(lambda u: getattr(u, "role", None) in ("tutor", "guide", "admin") or u.is_superuser)
def tutorial_edit(request, pk):
    tutorial = get_object_or_404(Tutorial, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = TutorialForm(request.POST, request.FILES, instance=tutorial)
        if form.is_valid():
            form.save()
            return redirect("tutorial_detail", pk=tutorial.pk)
    else:
        form = TutorialForm(instance=tutorial)
    return render(request, "tutorials/tutorial_form.html", {"form": form, "edit": True})
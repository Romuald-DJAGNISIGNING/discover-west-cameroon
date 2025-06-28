from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from .forms import ReviewForm

@login_required
def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, "reviews/review_list.html", {"reviews": reviews})

@login_required
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, "reviews/review_detail.html", {"review": review})

@login_required
def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("review_detail", pk=review.pk)
    else:
        form = ReviewForm()
    return render(request, "reviews/review_form.html", {"form": form})

@login_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("review_detail", pk=review.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/review_form.html", {"form": form, "edit": True})
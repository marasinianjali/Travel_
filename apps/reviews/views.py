from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'review/review_list.html', {'reviews': reviews})

# @login_required(login_url='/user-login/')
def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'review/add_review.html', {'form': form})

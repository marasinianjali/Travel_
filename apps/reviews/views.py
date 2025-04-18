from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm



def review_list(request):
    if "user_id" not in request.session:
        return redirect("user_login:user-login")
    reviews = Review.objects.select_related('user', 'package', 'guide', 'hotel', 'company')[:10]
    return render(request, 'review/review_list.html', {'reviews': reviews})



def add_review(request):
    if "user_id" not in request.session:
        return redirect("user_login:user-login")
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect('review:review_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReviewForm()
    return render(request, 'review/add_review.html', {'form': form})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# def add_review(request):
#     if "user_id" not in request.session:
#         return redirect("/user-login/")  # Redirect if not logged in
    
#     try:
#         user = User.objects.get(id=request.session["user_id"])
#     except User.DoesNotExist:
#         return redirect("/user-login/")

#     if request.method == "POST":
#         form = ReviewForm(request.POST, request.FILES)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = user  # ✅ Use fetched user instance
#             review.save()
#             return redirect('review_list')
#     else:
#         form = ReviewForm()
    
#     return render(request, 'review/add_review.html', {'form': form})

# def add_review(request):
#     if "user_id" not in request.session:
#         return redirect("/user-login/")  # Redirect if not logged in
    
#     try:
#         user = User.objects.get(id=request.session["user_id"])
#     except User.DoesNotExist:
#         return redirect("/user-login/")

#     if request.method == "POST":
#         form = ReviewForm(request.POST, request.FILES)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = user  # ✅ Use fetched user instance
#             review.save()
#             return redirect('review_list')
#     else:
#         form = ReviewForm()
    
#     return render(request, 'review/add_review.html', {'form': form})


# @login_required(login_url='/user-login/')
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

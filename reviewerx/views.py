import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib import messages
from .models import (
    User,
    Business,
    Review,
    Comment,
    ReviewLike,
    CommentLike,
    BusinessPhoto,
    ReviewPhoto,
    BusinessType,
)

from .forms import (
    BusinessForm,
    BusinessPhotoForm,
    ReviewForm,
    ReviewPhotoForm,
    CommentForm,
)


def index(request):
    context = {}
    p = Paginator(Business.objects.all(), 3)
    page = request.GET.get("page")
    businesses = p.get_page(page)
    nums = "a" * businesses.paginator.num_pages

    context = {"businesses": businesses, "nums": nums}

    return render(request, "reviewerx/index.html", context)


def business_detail(request, id):
    business = Business.objects.get(id=id)
    review_photos = ReviewPhoto.objects.all()

    context = {
        "business": business,
        "review_photos": review_photos,
    }

    return render(request, "reviewerx/business_detail.html", context)


@login_required
def add_business_form(request):
    business_form = BusinessForm(initial={"type": BusinessType.objects.first()})
    business_photo_form = BusinessPhotoForm()

    if request.method == "POST":
        business_form = BusinessForm(request.POST)
        business_photo_form = BusinessPhotoForm(request.FILES)
        if business_form.is_valid() and business_photo_form.is_valid():
            business = business_form.save(commit=False)
            business.user_id = request.user
            business.save()
            for index, photo in enumerate(request.FILES.getlist("photo")):
                business_photo = BusinessPhoto(photo=photo)
                if index == 0:
                    business_photo.is_primary = True
                business_photo.save()
                business.photos.add(business_photo)

            if len(request.FILES.getlist("photo")) == 0:
                default_photo = BusinessPhoto(is_primary=True)
                default_photo.save()
                business.photos.add(default_photo)

            return redirect("business_detail", id=business.id)

    return render(
        request,
        "reviewerx/add_business_form.html",
        {
            "form": business_form,
            "business_photo_form": business_photo_form,
        },
    )


@login_required
def update_business(request, id):
    obj = get_object_or_404(Business, id=id)

    if request.user != obj.user_id:
        messages.success(request, "You are not authorized to edit this business!")
        return redirect("business_detail", id=id)

    business_form = BusinessForm(
        instance=obj,
        initial={"type": BusinessType.objects.get(name=obj.type)},
    )

    photos = obj.photos.all()
    business_photo_form = BusinessPhotoForm()

    if request.method == "POST":
        business_form = BusinessForm(request.POST, instance=obj)
        business_photo_form = BusinessPhotoForm(request.FILES)

        if business_form.is_valid() and business_photo_form.is_valid():
            business = business_form.save(commit=False)
            business.user_id = request.user
            business.save()

            for index, photo in enumerate(request.FILES.getlist("photo")):
                business_photo = BusinessPhoto(photo=photo)
                business_photo.save()
                business.photos.add(business_photo)

            if (
                len(request.FILES.getlist("photo")) > 0
                and business.photos.all()
                .filter(photo="business/none/default.png")
                .count()
                != 0
            ):
                default_photo = business.photos.get(photo="business/none/default.png")
                default_photo.delete()
                new_primary_photo = business.photos.all().first()
                new_primary_photo.is_primary = True
                new_primary_photo.save()

            business.save()

            return redirect("business_detail", id=id)

    return render(
        request,
        "reviewerx/update_business_form.html",
        {
            "business_form": business_form,
            "photos": photos,
            "business_photo_form": business_photo_form,
            "business_id": id,
        },
    )


@login_required
def delete_business(request, id):
    business = get_object_or_404(Business, id=id)

    if request.user != business.user_id:
        messages.success(request, "You are not authorized to delete this business")
        return redirect("business_detail", id=id)

    messages.success(request, "Business was deleted.")
    business.delete()
    return redirect("index")


@login_required
def set_photo_as_primary(request, business_id, photo_id):
    business = get_object_or_404(Business, id=business_id)

    if request.user != business.user_id:
        messages.success(request, "You are not authorized to edit this business!")
        return redirect("business_detail", id=id)

    new_primary_photo = get_object_or_404(BusinessPhoto, id=photo_id)
    previous_primary_photo = business.photos.get(is_primary=True)
    previous_primary_photo.is_primary = False
    previous_primary_photo.save()
    new_primary_photo.is_primary = True
    new_primary_photo.save()
    return redirect("update_business", id=business_id)


@login_required
def delete_photo(request, business_id, photo_id):
    business = get_object_or_404(Business, id=business_id)

    if request.user != business.user_id:
        messages.success(request, "You are not authorized to edit this business!")
        return redirect("business_detail", id=id)

    photo = BusinessPhoto.objects.get(id=photo_id)
    was_primary = photo.is_primary
    photo.delete()

    if business.photos.count() == 0:
        default_photo = BusinessPhoto(is_primary=True)
        default_photo.save()
        business.photos.add(default_photo)
        return redirect("update_business", id=business_id)

    if was_primary:
        new_primary = business.photos.all().first()
        if new_primary:
            new_primary.is_primary = True
            new_primary.save()

    return redirect("update_business", id=business_id)


@login_required
def add_review_form(request, id):
    business = Business.objects.get(id=id)
    review_form = ReviewForm()
    review_photo_form = ReviewPhotoForm()

    if request.user == business.user_id:
        messages.success(request, ("You cannot review your own business."))
        return redirect("business_detail", id=id)

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        review_photo_form = ReviewPhotoForm(request.FILES)
        if review_form.is_valid() and review_photo_form.is_valid():
            review = review_form.save(commit=False)
            review.user_id = request.user
            review.save()

            for photo in request.FILES.getlist("photo"):
                review_photo = ReviewPhoto(photo=photo)
                review_photo.save()
                review.photos.add(review_photo)

            business.reviews.add(review)
            return redirect("business_detail", id=business.id)

    context = {
        "business": business,
        "review_form": review_form,
        "review_photo_form": review_photo_form,
    }

    return render(request, "reviewerx/add_review_form.html", context)


@login_required
def update_review(request, id):
    review = get_object_or_404(Review, id=id)

    if request.user != review.user_id:
        messages.success(request, ("You cannot edit this review."))
        return redirect("business_detail", id=review.businesses.get().id)

    review_form = ReviewForm(instance=review)
    review_photo_form = ReviewPhotoForm()
    photos = review.photos.all()

    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=review)
        review_photo_form = ReviewPhotoForm(request.FILES)
        if review_form.is_valid() and review_photo_form.is_valid():
            review = review_form.save(commit=False)
            review.user_id = request.user
            review.save()

            for photo in request.FILES.getlist("photo"):
                review_photo = ReviewPhoto(photo=photo)
                review_photo.save()
                review.photos.add(review_photo)

            return redirect("business_detail", id=review.businesses.get().id)

    return render(
        request,
        "reviewerx/update_review.html",
        {
            "review_form": review_form,
            "review_photo_form": review_photo_form,
            "photos": photos,
            "review": review,
        },
    )


@login_required
def delete_review_photo(request, id):
    photo = get_object_or_404(ReviewPhoto, id=id)
    review_id = photo.review_photo.get().id

    if request.user != photo.review_photo.get().user_id:
        messages.success(request, "You are not authorized to delete this photo!")
        return redirect(
            "business_detail", id=photo.review_photo.get().businesses.get().id
        )

    photo.delete()
    messages.success(request, "Photo successfully deleted!")
    return redirect("update_review", id=review_id)


@login_required
def delete_review(request, id):
    review = get_object_or_404(Review, id=id)
    business_id = review.businesses.get().id

    if request.user != review.user_id:
        messages.success(request, "You are not authorized to delete this review!")
        return redirect("business_detail", id=business_id)

    review.delete()
    return redirect("business_detail", id=business_id)


@login_required
def like_review(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        review_id = data.get("review_id")
        author = request.user

        review = Review.objects.get(id=review_id)
        liked_by_author = review.likes.filter(user_id=author)

        if review.user_id == author:
            return JsonResponse({"review_like_count": review.likes.count()}, status=201)

        if liked_by_author.count() != 0:
            liked_by_author.first().delete()
            # review.save()
            return JsonResponse({"review_like_count": review.likes.count()}, status=201)
        else:
            like = ReviewLike(user_id=author)
            like.save()
            review.likes.add(like)
            return JsonResponse({"review_like_count": review.likes.count()}, status=201)

    return HttpResponseRedirect(reverse("index"))


@login_required
def like_comment(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        comment_id = data.get("comment_id")
        author = request.user

        comment = Comment.objects.get(id=comment_id)
        liked_by_author = comment.likes.filter(user_id=author)

        if comment.user_id == author:
            return JsonResponse(
                {"comment_like_count": comment.likes.count()}, status=201
            )

        if liked_by_author.count() != 0:
            liked_by_author.first().delete()
            return JsonResponse(
                {"comment_like_count": comment.likes.count()}, status=201
            )
        else:
            like = CommentLike(user_id=author)
            like.save()
            comment.likes.add(like)
            return JsonResponse(
                {"comment_like_count": comment.likes.count()}, status=201
            )

    return HttpResponseRedirect(reverse("index"))


@login_required
def add_comment(request, id):
    review = get_object_or_404(Review, id=id)
    comment_form = CommentForm()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user_id = request.user
            comment.save()
            review.comments.add(comment)
            return business_detail(request, review.businesses.first().id)

    return render(request, "reviewerx/add_comment.html", {"comment_form": comment_form})


@login_required
def update_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    business_id = comment.comment.get().businesses.get().id

    if request.user != comment.user_id:
        messages.success(request, "You are not authorized to edit this comment!")
        return redirect("business_detail", id=business_id)

    comment_form = CommentForm(instance=comment)

    if request.method == "POST":
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_obj = comment_form.save(commit=False)
            comment_obj.user_id = request.user
            comment_obj.save()
            return redirect("business_detail", id=business_id)

    return render(
        request,
        "reviewerx/update_comment.html",
        {"comment_form": comment_form, "comment": comment},
    )


@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    business_id = comment.comment.get().businesses.get().id

    if request.user != comment.user_id:
        messages.success(request, "You are not authorized to delete this comment!")
        return redirect("business_detail", id=business_id)

    comment.delete()
    messages.success(request, "Your comment was deleted!")
    return redirect("business_detail", id=business_id)


def search_business(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        p = Paginator(Business.objects.filter(name__contains=searched), 3)
        page = request.GET.get("page")
        businesses = p.get_page(page)
        nums = "a" * businesses.paginator.num_pages

        return render(
            request,
            "reviewerx/search_business.html",
            {"businesses": businesses, "nums": nums},
        )
    else:
        return render(request, "reviewerx/search_business.html", {})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "reviewerx/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "reviewerx/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "reviewerx/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "reviewerx/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "reviewerx/register.html")

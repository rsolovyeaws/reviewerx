from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from uuid import uuid4
import os


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "avatars/%s.%s" % (str(uuid4().hex), extension)


def business_upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "business/%s.%s" % (str(uuid4().hex), extension)


def review_upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "review/%s.%s" % (str(uuid4().hex), extension)


def comment_upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "comment/%s.%s" % (str(uuid4().hex), extension)


class User(AbstractUser):
    first_name = models.CharField(max_length=24, null=True, blank=True)
    last_name = models.CharField(max_length=24, null=True, blank=True)
    photo = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        default="avatars/none/default.png",
    )


class Business(models.Model):
    user_id = models.ForeignKey("User", related_name="user", on_delete=models.PROTECT)
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.CharField(max_length=1024, null=False, blank=False)
    type = models.CharField(max_length=32, null=False, blank=False)
    website = models.URLField(null=True, blank=True)
    street = models.CharField(max_length=512, null=False, blank=False)
    city = models.CharField(max_length=32, null=False, blank=False)
    state = models.CharField(max_length=32, null=True, blank=True)
    country = models.CharField(max_length=32, null=False, blank=False)
    zip_code = models.CharField(max_length=32, null=True, blank=True)
    schedule = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    photos = models.ManyToManyField(
        "BusinessPhoto", null=True, blank=True, related_name="businesses"
    )
    reviews = models.ManyToManyField(
        "Review", null=True, blank=True, related_name="businesses"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    @property
    def average_rating(self):
        count = 0
        sum = 0
        result = 0
        for review in self.reviews.all():
            count += 1
            sum += review.rating
        if count != 0:
            result = sum / count

        return round(result, 2)


class Review(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.PROTECT)
    title = models.CharField(max_length=128, null=False, blank=False)
    text = models.CharField(max_length=1024, null=False, blank=False)
    rating = models.PositiveSmallIntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    likes = models.ManyToManyField("ReviewLike", related_name="review", blank=True)
    photos = models.ManyToManyField(
        "ReviewPhoto", related_name="review_photo", blank=True
    )
    comments = models.ManyToManyField("Comment", related_name="comment", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.user_id}"


class Comment(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.PROTECT)
    likes = models.ManyToManyField(
        "CommentLike", related_name="comment_like", null=True, blank=True
    )
    text = models.CharField(max_length=1024, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text[0:50]} by {self.user_id}"


class ReviewLike(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_id}"


class CommentLike(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_id}"


class BusinessPhoto(models.Model):
    photo = models.ImageField(
        upload_to=business_upload_location,
        null=True,
        blank=True,
        default="business/none/default.png",
    )
    timestamp = models.DateTimeField(default=timezone.now)
    is_primary = models.BooleanField(default=False)


class ReviewPhoto(models.Model):
    photo = models.ImageField(upload_to=review_upload_location, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)


class CommentPhoto(models.Model):
    # comment_id = models.ForeignKey("Comment", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=comment_upload_location, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Photo for Review: {self.review_id}"


class BusinessType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

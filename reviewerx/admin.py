from django.contrib import admin
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

# Register your models here.
admin.site.register(User)
admin.site.register(Business)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(ReviewLike)
admin.site.register(CommentLike)
admin.site.register(BusinessPhoto)
admin.site.register(ReviewPhoto)
admin.site.register(BusinessType)

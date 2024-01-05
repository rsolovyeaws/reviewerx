from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #
    path("business/<int:id>", views.business_detail, name="business_detail"),
    path("add-review/<int:id>", views.add_review_form, name="add_review"),
    path("add-comment/<int:id>", views.add_comment, name="add_comment"),
    path("add-business", views.add_business_form, name="add_business"),
    #
    path("update-business/<int:id>", views.update_business, name="update_business"),
    path(
        "set-primary-photo/<int:business_id>/<int:photo_id>",
        views.set_photo_as_primary,
        name="set_photo_as_primary",
    ),
    path(
        "delete-photo/<int:business_id>/<int:photo_id>",
        views.delete_photo,
        name="delete_photo",
    ),
    path("update-review/<int:id>", views.update_review, name="update_review"),
    path(
        "delete-review-photo/<int:id>",
        views.delete_review_photo,
        name="delete_review_photo",
    ),
    path("delete-review/<int:id>", views.delete_review, name="delete_review"),
    path("update-comment/<int:id>", views.update_comment, name="update_comment"),
    path("delete-comment/<int:id>", views.delete_comment, name="delete_comment"),
    #
    path("like_review", views.like_review, name="like_review"),
    path("like_comment", views.like_comment, name="like_comment"),
    #
    path("search_business", views.search_business, name="search_business"),
    path("delete_business/<int:id>", views.delete_business, name="delete_business"),
]

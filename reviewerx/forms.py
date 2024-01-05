from django import forms
from django.forms import ModelForm
from .models import Business, BusinessPhoto, BusinessType, Comment, Review, ReviewPhoto


class BusinessForm(ModelForm):
    type = forms.ModelChoiceField(
        queryset=BusinessType.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Business
        fields = (
            "name",
            "type",
            "description",
            "website",
            "street",
            "city",
            "state",
            "country",
            "zip_code",
            "schedule",
            "phone",
            "email",
        )
        labels = {
            "name": "",
            "type": "",
            "description": "",
            "website": "",
            "street": "",
            "city": "",
            "state": "",
            "country": "",
            "zip_code": "",
            "schedule": "",
            "phone": "",
            "email": "",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Business Name"}
            ),
            "type": forms.Select(
                attrs={"class": "form-select", "placeholder": "Business Type"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "website": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "Website"}
            ),
            "street": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Street"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "State"}
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Country"}
            ),
            "zip_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Zip/Postal Code"}
            ),
            "schedule": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Schedule"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }


class BusinessPhotoForm(ModelForm):
    class Meta:
        model = BusinessPhoto
        fields = ("photo", "is_primary")
        labels = {"photo": "Photo", "is_primary": "Is primary"}
        widgets = {
            "photo": forms.FileInput(
                attrs={"class": "form-control-file", "multiple": ""}
            ),
            "is_primary": forms.CheckboxInput(attrs={"class": "form-control"}),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        labels = {"text": ""}
        widgets = {
            "text": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Comment"}
            )
        }


class ReviewForm(ModelForm):
    """title = models.CharField(max_length=128, null=False, blank=False)
    text = models.CharField(max_length=1024, null=False, blank=False)
    rating = models.PositiveSmallIntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    """

    class Meta:
        model = Review
        fields = ("title", "text", "rating")
        labels = {"title": "", "text": "", "rating": ""}
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "text": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Comment"}
            ),
            "rating": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "max": "5", "default": "5"}
            ),
        }


class ReviewPhotoForm(ModelForm):
    class Meta:
        model = ReviewPhoto
        fields = ("photo",)
        labels = {"photo": ""}
        widgets = {
            "photo": forms.FileInput(
                attrs={"class": "form-control-file", "multiple": ""}
            ),
        }

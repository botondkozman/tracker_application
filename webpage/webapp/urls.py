from django.urls import path
from . import views

urlpatterns = [
    path("", views.UploadImage.as_view()),
    path("upload/", views.UploadImage.as_view(), name = "upload"),
    path("upload/success/", views.upload_success, name = "success")
]
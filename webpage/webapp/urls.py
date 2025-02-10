from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("upload/", views.UploadImage.as_view(), name = "upload"),
    path("upload/success/", views.upload_success, name = "success"),
    path('ads/', views.ads, name = "ads"),
    path('generate/', views.generate, name = "generate")
]
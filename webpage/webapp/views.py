from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import View
from django.conf import settings

import os

from .forms import ImageForm
from .models import UploadedFileModel
from .detect_object import detect_object

# Create your views here.
class UploadImage(View):
    def get(self, request):
        form = ImageForm()
        return render(request, "upload_file.html", {
            "form" : form
        })

    def post(self, request):
        submitted_form = ImageForm(request.POST, request.FILES)

        if submitted_form.is_valid():
            self.store_file(request.FILES["user_image"])
            image = UploadedFileModel(image = request.FILES["user_image"])
            image.save()
            image_name = image.image.name
            uploads_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
            full_path = uploads_path + "/"+ image_name
            cropped_file_name = detect_object(full_path)

            image_name = image.image.name
            image_path = f"{settings.MEDIA_URL}{image_name}"
            cropped_image_path = f"{settings.MEDIA_URL}{cropped_file_name}"

            return render(request, "upload_success.html", {
                "original_image" : image_path,
                "cropped_image" : cropped_image_path
            })
    
        return render(request, "upload_file.html", {
            "form" : submitted_form
        })
    
    def store_file(self, file):
        with open("temp/" + file.name, "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk) 

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def ads(request):
    template = loader.get_template('ads.html')
    return HttpResponse(template.render())

def generate(request):
    if request.method == 'POST':
        print(request.POST.get('slider_value'))

    return render(request, 'generate.html')

def upload_success(request):
    template = loader.get_template('upload_success.html')
    return HttpResponse(template.render())
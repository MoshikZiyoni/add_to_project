from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.models import AddAttraction
# Create your views here.
def add_attraction(request):
    name=request.data['name']
    city=request.data['city']
    description=request.data['description'] if request.data['description'] else None
    website=request.data['website'] if request.data['website'] else None
    hours=request.data['hours'] if request.data['hours'] else None
    tel=request.data['tel'] if request.data['tel'] else None
    address=request.data['address'] if request.data['address'] else None
    tips=request.data['tips'] if request.data['tips'] else None
    uploaded_image = request.FILES.get('photos')
    if uploaded_image:
        # Process the uploaded image here and save it
        # Generate a unique filename, save it to a directory, and store the URL in your database
        # Example:
        from django.core.files.storage import FileSystemStorage

        fs = FileSystemStorage()
        image_name = fs.save(uploaded_image.name, uploaded_image)
        image_url = fs.url(image_name)
        print (image_url)
        # AddAttraction(name=name,city=city,description=description,website=website,hours=hours,tel=tel,address=address,tips=tips,photos=image_url)
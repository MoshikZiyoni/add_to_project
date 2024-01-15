from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from unidecode import unidecode
from rest_framework.decorators import api_view
from app.models import AddAttraction,City,Night_Life
import random
import time
import requests
import re
from django.db.models import Q
from geopy.geocoders import Nominatim
from app.serializer import Night_Lifeserializers
import math
from geopy.distance import geodesic
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import json

@api_view(['GET', 'POST'])
def night_life(request):
    # s=City.objects.all().values()
    # print (s)
    # return Response(s)
    if request.method == 'GET':

        # Access query parameters from request.GET for GET requests
        city=request.data.get('city')
        lon=request.data.get('longitude')
        lat=request.data.get('latitude')

        radius = 10  # Default to 10 if not provided
    elif request.method == 'POST':
        # Access JSON data from request.data for POST requests
        city=request.data.get('city')
        lon=request.data.get('longitude')
        lat=request.data.get('latitude')
        radius =  10
    # # return Response('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    # print (request.data,'@@@@@@@@@@@@@@@@@@@@@@@')
    # city=request.data['city']
    # lon=request.data['longitude']
    # lat=request.data['latitude']
    # dala=(city,lon,lat,'@@@@@@@@@@@@@@@@@@@@@@')
    # return JsonResponse(dala,safe=False)
    # radius=request.data.get('radius',10)

    # normalized_city_name = unidecode(city)
    # normalized_city_name = normalized_city_name.strip()
    # city_objs = City.objects.filter(Q(city__iexact=normalized_city_name) | Q(city__icontains=normalized_city_name)).first()
    # if city_objs:
        # night_life_attractions=Night_Life.objects.filter(city_id=city_objs)
    center_point = (lat, lon)

    night_life_attractions = [
        obj for obj in Night_Life.objects.all() if
        geodesic(center_point, (obj.latitude, obj.longitude)).km <= radius
    ]
    serializer = Night_Lifeserializers(night_life_attractions, many=True)

    if serializer:
        return Response(serializer.data, status=200)
    else:
        return Response('Sorry',status=400)



@api_view(['GET', 'POST'])
def ai_bot(request):
    print ('start ai@@@@@@@@@@@@@@@@@@')
    # return JsonResponse("dale pai",safe=False)
    attractions=request.data.get('attractions')
    restaurants=request.data.get('restaurants')
    days=request.data.get('days')
    # return JsonResponse(f"dale pai{attractions}{restaurants}{days}",safe=False)

    start_time = time.time()  # Start measuring the time

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver.maximize_window()
    driver.get('https://api.deepai.org/chat')
    # time.sleep(2)
    # cities = ['Tel Aviv','Haifa','Eilat']
    counter = 3
    # while True:
    # question=f'I need your help to organize my trip and make it with schedules with times for each day. I have a list of attractions {attractions} and list of restaurants {restaurants} and I need you to organize that to be the best trip for {days} days,please organize that as a schedules with times for example: ("day1": {"Tel Aviv": { "8:00 am": "Open your day with Breakfast at Cafe Xoho", "9:00 am": "Visit Tel Aviv Promenade","11:00 am": "Explore Tel Aviv Beaches", "1:00 pm": "Lunch at HaBasta","2:30 pm": "Visit Tel Aviv Port","4:00 pm": "Explore Rabin Square","6:00 pm": "Visit Tel Aviv Museum of Art","8:00 pm": "Dinner at The Blue Rooster"}})I want only 2-3 attractions in a day not more.return me the answer with the exact days I provided not less not more.return in JSON format'
    format_json='"day1": {"Tel Aviv": { "8:00 am": "Open your day with Breakfast at Cafe Xoho", "9:00 am": "Visit Tel Aviv Promenade","11:00 am": "Explore Tel Aviv Beaches", "1:00 pm": "Lunch at HaBasta","2:30 pm": "Visit Tel Aviv Port","4:00 pm": "Explore Rabin Square","6:00 pm": "Visit Tel Aviv Museum of Art","8:00 pm": "Dinner at The Blue Rooster"}'
    question=f'I need your help to organize my trip and make it with schedules with times for each day. I have a list of attractions {attractions} and list of restaurants {restaurants} and I need you to organize that to be the best trip for {days} days,please organize that as a schedules with times for example: ({format_json})I want only 2-3 attractions in a day not more.return me the answer with the exact days I provided not less not more.return in JSON format'
    time.sleep(3)
    print ('start for looking for chat box')
    chat_box = driver.find_element(By.XPATH,f'/html/body/div[{counter}]/textarea').send_keys(question)
    action=ActionChains(driver)
    action.send_keys(Keys.ENTER)
    action.perform()
    text_is_ready = True
    print ('start the loop')

    while text_is_ready:
        try:
            driver.find_element(By.XPATH,f'/html/body/div[{counter+2}]/textarea').send_keys('Check')
            text_is_ready = False
            print('text is ready to send@@@@@@@@@@@@@@@@@@')
        except:
            pass
    text_to_check = driver.find_element(By.XPATH,f'/html/body/div[{counter+1}]')
    answer=text_to_check.text
    # print('@@@@@',answer,'@@@@@')
    start_index = answer.find('{')
    end_index = answer.rfind('}') + 1

    # Extract the JSON portion
    json_string = answer[start_index:end_index]        # Load the JSON data
    json_data = json.loads(json_string)
    print(json_data)
    # return answer
    # time.sleep(2)
    # driver.find_element(By.XPATH, '/html/body/div[5]/textarea').clear()
    # counter+=2
    driver.quit()
    end_time = time.time()  # Stop measuring the time
    elapsed_time = end_time - start_time
    print(f"The function took {elapsed_time:.2f} seconds to return a response.")
    return JsonResponse(json_data,safe=False)





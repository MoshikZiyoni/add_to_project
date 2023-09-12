from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from unidecode import unidecode
from rest_framework.decorators import api_view
from selenium import webdriver
from app.models import AddAttraction,City,Night_Life
import random
import time
import requests
import re
from selenium.webdriver.common.by import By
from django.db.models import Q
from geopy.geocoders import Nominatim
from app.serializer import Night_Lifeserializers
import math
from geopy.distance import geodesic


@api_view(['GET', 'POST'])
def night_life(request):
    city=request.data['city']
    lon=request.data['longitude']
    lat=request.data['latitude']
    radius=request.data.get('radius',10)
    normalized_city_name = unidecode(city)
    normalized_city_name = normalized_city_name.strip()
    city_objs = City.objects.filter(Q(city__iexact=normalized_city_name) | Q(city__icontains=normalized_city_name)).first()
    if city_objs:
        # night_life_attractions=Night_Life.objects.filter(city_id=city_objs)
        center_point = (lat, lon)

        night_life_attractions = [
            obj for obj in Night_Life.objects.all() if
            geodesic(center_point, (obj.latitude, obj.longitude)).km <= radius
        ]
        serializer = Night_Lifeserializers(night_life_attractions, many=True)
        
        return Response(serializer.data, status=200)


@api_view(['GET', 'POST'])
def add_attraction(request):
    return JsonResponse('add_attraction',safe=False)
#     # delll=Night_Life.objects.filter(city_id=567).delete()
#     # return 'kk'
#     def extract_restaurants_data(attractions):
#         geolocator = Nominatim(user_agent="dream-trip")

#         try:
#             # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
#             user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/100.0"

#             # Set up the Chrome WebDriver with User-Agent and headless mode
#             chrome_options = webdriver.ChromeOptions()
#             # chrome_options.add_argument(f"user-agent={user_agent}")
#             # chrome_options.add_argument("--headless")  # Run in headless mode
#             random_time = random.uniform(3,6)

#             # Create a Chrome WebDriver instance
#             # service_path = "C:/Users/moshi/Downloads/chromedriver.exe"
#             # service = Service(service_path)
#             driver = webdriver.Chrome( options=chrome_options)
#             # Initialize the WebDriver (in this case, using Chrome)
#             cities_list=['Las Vegas', 'Brașov', 'Cluj-Napoca', 'Boquete','Kandy']
#             for attraction_data in attractions:
#                 city = attraction_data["city"]
#                 # if city not in cities_list:
#                 #     print ('continue')
#                     # continue
                
#                 name = attraction_data["name"]
#                 normalized_city_name = unidecode(city)
#                 try:
#                     formatted_address=attraction_data["formatted address"]
#                 except:
#                     pass
#                 try:
#                     formatted_address=attraction_data["formatted_address"]
#                 except:
#                     pass
#                 try:
#                     city_objs = City.objects.filter(city=city).first()
#                     if not city_objs:
#                         print ('no regular')
#                         normalized_city_name = normalized_city_name.strip()
#                         print(normalized_city_name)
#                         city_objs = City.objects.filter(Q(city__iexact=normalized_city_name) | Q(city__icontains=normalized_city_name)).first()
#                     if city_objs:
#                         print(city_objs.city)
                    
#                 except:
                        
#                         words = formatted_address.split()
#                         last_word = words[-1]
#                         last_word = last_word.strip('",)')
#                         location = geolocator.geocode(f"{last_word}")
#                         if location:
#                             landmarks = [location.latitude, location.longitude]
#                             print (landmarks)
#                             city_query = City(
#                             city=city,
#                             latitude=landmarks[0],
#                             longitude=landmarks[1],
#                             )
#                             city_query.save()
#                             city_objs = City.objects.filter(city=city).first()
#                         else:
#                             print(f"Could not geocode: {last_word}")
#                 check_name=Night_Life.objects.filter(name=name,city_id=city_objs.id).first()
                      
#                 if not check_name:
                    
                    
#                     latitude= attraction_data["latitude"] if attraction_data["latitude"] else ""
#                     longitude= attraction_data["longitude"] if attraction_data["longitude"] else ""
#                     name_for_flicker=f"{name} Night Life, {city}"
                    
#                     # driver.get(f"google.com/search?tbm=isch&q={name_for_flicker}")
#                     driver.get(f"https://www.google.com/search?tbm=isch&q={name_for_flicker}")
#                     # /html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img
#                     time.sleep(random_time)
#                     first_image = driver.find_element(By.XPATH,"/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img").get_attribute('src')
                    
#                     # first_image=""
#                     # photos=""
#                     if len(first_image)>2:
#                         image_data = first_image.split(',')[1].encode()
#                         url = "https://api.imgbb.com/1/upload"
#                         api_key = '5c63908b4a43125a2ef458c94f23e123'
#                         payload = {
#                             "key": api_key,
#                             "image": image_data,
#                         }
#                         response = requests.post(url, payload)
#                         print (response.text)
#                         photos=(response.json()["data"]["url"])

#                     # image_data = base64.b64decode(first_image.split(',')[1])
#                     # headers = {
#                     #     "Authorization": "Client-ID 92a43ec7ca67375" 
#                     # }
#                     # url = "api.imgur.com/3/image"
#                     # response = requests.post(url, headers=headers, data=image_data)
#                     # imgur_response = json.loads(response.text)
#                     # print (imgur_response)
#                     # # Get image link
#                     # image_link = imgur_response['data']['link']
#                     # photos=(image_link)
#                     # photos = flickr_api(name=name_for_flicker, latitude=latitude, longitude=longitude)
#                     if photos==None:
#                         photos=""
#                     print (photos,'@@@@@',name)
#                     review_score= attraction_data["review_score"] if attraction_data["review_score"] else ""
#                     website= attraction_data["website"] if attraction_data["website"] else ""
#                     try:
#                         hours= attraction_data["hours"] 
#                     except:
#                         hours=""
#                     price_range= attraction_data["price_range"] if attraction_data["price_range"] else ""
#                     category=attraction_data["category"] if attraction_data["category"] else ""
                   

#                     try:
#                         tel=attraction_data['telephone']
#                     except:
#                         tel=""
#                     website= website or ""
#                     try:
#                         tips=attraction_data["tips"]
#                         if isinstance(tips, list):
#                             pass
#                         elif isinstance(tips, str):
#                             tips_list = [tip.strip() for tip in re.split(r'\d+\.', tips) if tip.strip()]
#                             tips=tips_list
#                             print (tips)
#                     except Exception as e:
#                         tips= ""
#                         print(e)
                    
#                     # print (name,latitude,longitude,review_score,description,website,hours,distance,real_price,tips,formatted_address)
                    
#                     if city_objs:
#                         try:
#                             print (city_objs.id,'AAAAAAA')
#                             # city_obj = city_objs[0]
#                             # print (city_objs.id,'AAAAAAA')
#                             atrc_query = Night_Life(
#                             name=name,
#                             city=city_objs,
#                             latitude=latitude,
#                             longitude=longitude,
#                             photos=photos,
#                             review_score=review_score,
#                             website=website,
#                             hours=hours,
#                             category=category,
#                             price_range=price_range,
#                             address=formatted_address,
#                             tips=tips,
#                             tel=tel
#                         )
#                             atrc_query.save()
#                             print("Save attraction successfully")
#                             with open('restaurants_saved.txt', 'a', encoding='utf-8') as f:
#                                 f.write(name + '\n')
#                         except Exception as e:
#                             print (e)

#                     else:
#                         print ("no city obj")
#                         with open('restaurants_not_saved.txt', 'a', encoding='utf-8') as f:
#                             f.write(name + '\n')
#                 else:
#                     print ('there is the attrac already')
#         except Exception as e:
#             print (e,'erorrrrrr')
#     extract_restaurants_data(attractions  = [


	
#     ])
#     return JsonResponse('ok',safe=False)


    # name=request.data['name']
    # city=request.data['city']
    # description=request.data['description'] if request.data['description'] else None
    # website=request.data['website'] if request.data['website'] else None
    # hours=request.data['hours'] if request.data['hours'] else None
    # tel=request.data['tel'] if request.data['tel'] else None
    # address=request.data['address'] if request.data['address'] else None
    # tips=request.data['tips'] if request.data['tips'] else None
    # uploaded_image = request.FILES.get('photos')
    # if uploaded_image:
    #     # Process the uploaded image here and save it
    #     # Generate a unique filename, save it to a directory, and store the URL in your database
    #     # Example:
    #     from django.core.files.storage import FileSystemStorage

    #     fs = FileSystemStorage()
    #     image_name = fs.save(uploaded_image.name, uploaded_image)
    #     image_url = fs.url(image_name)
    #     print (image_url)
    #     # AddAttraction(name=name,city=city,description=description,website=website,hours=hours,tel=tel,address=address,tips=tips,photos=image_url)



# def add_city(request):
    
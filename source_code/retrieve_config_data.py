import json


with open("config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

news_apikey = jsonObject['news_apikey']
covid_terms = jsonObject['covid_terms']
defualt_local_location = jsonObject['defualt_local_location']
defualt_local_location_type = jsonObject['defualt_local_location_type']
defualt_national_location = jsonObject['defualt_national_location']
defualt_national_location_type = jsonObject['defualt_national_location_type']
filepath = jsonObject['filepath']
image_name = jsonObject['image_name']
# Covid Dashboard

## Introduction
This project is a covid-19 dashboard. It displays infection rates along with other covid data (such as deaths) from the Public Health England API and displays news stories related to covid-19. It shows both national and local infection rates, the location of which can be changed in the config.json file.

It is a python back end with a webpage front end.

## Prerequisites
python 3.9
be sure to have the python standard libary and pip installed with python 3.9

## Installation
install flask:  
    pip install Flask
public health england API:
    pip install uk-covid19
news api:
    get api key here https://newsapi.org/

run setup.py with:
    python setup.py sdist bdist_wheel

## Getting Started Tutorial
Once installation is complete, open the config.json file. Insert the news api key where it says INSERT API KEY. all other config options should be filled in however change them when approriate. 
Below is a description of what each of the config items are:
news_apikey - the key for the news api
covid_terms - the terms the news api uses to search for articles, works as a filter
defualt_local_location - the location that the covid_API_request function in covid_data_handler.py takes as a defualt value. It is the location the public health england api will search for when being called
defualt_local_location_type - the location type that the covid_API_request function in covid_data_handler.py takes as a defualt value. It is the location type the public health england api will search for when being called
defualt_national_location - It is the national location  the public health england api will search for when being called and specified to search for national location
defualt_national_location_type - It is the national location type the public health england api will search for when being called and specified to search for national location
filepath - the file name for the log file
image_name - the name of the image saved in the static/images folder. The name of the image file which is displayed at the top of the dashboard

## Testing
Once the config is setup correctly run the covid-data_handler.py module by chaning the file directory to be inside the source_code file, then running the command python covid_data_handler.py . Then go to http://127.0.0.1:5000/.

To test the code run the test.py file (python test.py). The results of test will be in the app.log file. 

## Developer Documentation
Once the config is setup correctly run the covid-data_handler.py module by chaning the file directory to be inside the source_code file, then running the command python covid_data_handler.py . Then go to http://127.0.0.1:5000/.

Here you'll see the local infection rate in the last 7 days, the national infection rate in the last 7 days, the current number of hospital cases and the death total. To the right of this is the list of news articles. Click the x button on any of the news articles to remove them. Below the covid data you'll notice a box. This box is where you enter the time when you want the data and or news to update. Below this box is a label in this label you enter the name of the update. Below this label you will see 3 check boxes. The first check box is called "Repeat update", tick this checkbox if you want the update to repeat every 24 hours. The second check box is called "Update Covid data", tick this check box if you want the covid data to update. The third check box is called "Update news articles", tick this check box if you want the news articles to update. Once you have enterred the time, name and desired checkboxes then click this submit button below. This will schedule an update. Sheduled updates can be viwed in the list of scheduled updates on the left of the page. If at anytime you want to cancel an update click the x button on the update in the list of schedled updates.

## Deatils
Author: Joshua Curry
license: read license.txt
source: https://newsapi.org/
        https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/
        https://flask.palletsprojects.com/en/2.0.x/
        https://www.python.org/
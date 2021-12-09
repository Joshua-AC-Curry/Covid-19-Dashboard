from requests.api import request
from uk_covid19 import Cov19API
import sched, time
from covid_news_handling import update_news
from flask import Flask
from flask import render_template
from flask import request
import calc_time
import logging
from retrieve_config_data import defualt_local_location, defualt_local_location_type, defualt_national_location, defualt_national_location_type, filepath, image_name

""""Global variables"""
app = Flask(__name__)                       #the Flask application
s = sched.scheduler(time.time, time.sleep)  #scheduler, schedules the updates
articles = []                               #List(dictionary), news articles being displayed
deleted_articles = []                       #List(dictionary), news articles which as been removed
scheduled_updates = []                      #List(dictionary), names and description of updates which are to be exectued at scheduled time
infections_local = 0                        #int, value representing the current infections in local area
infections_national = 0                     #int, value representing the current infections in local area
hospital_cases = 0                          #int, value representing current number of hospital cases
death_total = 0                             #int, value representing the total number of deaths

def parse_csv_data(csv_filename):
    """argument string 
    with the name of a csv file  
    
    return a list
    each element of list being a line in the csv"""
    try:
        file = open( csv_filename , 'r' ).readlines()
        logging.info("csv file succesfully opened")
    except:
        logging.error("csv_filename not string, or file is not in directory")

    return list(file)

def process_covid_csv_data(covid_csv_data):
    """argument list
    usually the return of parse_csv_data
    each element of list being a line in the csv#

    Function takes in covid data and extracts desired data
    
    return int, int, int
    the number of covid cases in the last 7 days,
    current number of hopsital cases,
    the total number of deaths
    """
    [covid_csv_data[i:i+5] for i in range(0, len(covid_csv_data), 5)]
    current_hospitals = 0
    week_cases = 0
    death_total = 0
    got_deaths = False
    cases_day_count = 0
    got_hospitals = False
    for i in covid_csv_data:
        j = i.split(",")

        #ingore any empty data

        #for number of deaths
        if j[4] != "" and got_deaths == False and j[4].isdigit():
            death_total = int(j[4])
            got_deaths = True

        #for current number of hospital cases
        if j[5] != "" and got_hospitals == False and j[5].isdigit():
            current_hospitals =  int(j[5])
            got_hospitals = True
        
        #for cases in the last 7 days
        j[6] = j[6].strip()
        #ignoring first entry as data isn't complete on that day
        if cases_day_count > 0 and cases_day_count < 8 and j[6].isdigit():
            week_cases += int(j[6])
        if j[6].isdigit():
            cases_day_count += 1  

    logging.debug("week_cases : " + str(week_cases))
    logging.debug("current_hospitals : " + str(current_hospitals))
    logging.debug("death_total : " + str(death_total))

    return week_cases, current_hospitals, death_total

def covid_API_request(location = defualt_local_location, location_type = defualt_local_location_type):
    """argument string, string
    the name of the location, the type of location

    function to get the call the covid api and retreive its data

    return dictionary,
    covid data          
    """
    logging.info("requesting covid API")

    loc = [
        'areaType=' + location_type,
        'areaName=' + location
    ]

    cases_and_deaths = {
        "date": "date",
        "areaName" : "areaName",
        "areaCode" : "areaCode",
        "cumDailyNsoDeathsByDeathDate" : "cumDailyNsoDeathsByDeathDate",
        "hospitalCases" : "hospitalCases",
        "newCasesBySpecimenDate" : "newCasesBySpecimenDate"
        }

    return Cov19API(filters = loc, structure = cases_and_deaths).get_json()

def fetch_specified_covid_data(data, search):
    """argument dictionary, string
    covid data from the api, the data to be retrieved 

    A function which gets the desired covid data from the dictionary of all the data

    return case1: int, case2: int, case3: int
    case1: the number of infections from the last 7 days
    case2: the current number of hospital cases
    case3: the total number of deaths
    """

    #getting data for cases in the last 7 days
    if search == "7day_infections":
        infections = []
        for i in data:
            try:
                infections.append(i['newCasesBySpecimenDate'])
            except:
                logging.error("fetch_specified_covid_data, data missing key newCasesBySpecimenDate")

        logging.info("Calcuated cases in last seven days")
        logging.debug("cases in last seven days is: " + str(sum(infections[1:8])))

        return sum(infections[1:8])

    #getting data for the current number of hospital cases
    elif search == "hospital_cases":
        for i in data:
            if not(i['hospitalCases'] == None):
                logging.info("fetched hospital cases")
                logging.debug("hospital cases is: " + str(i['hospitalCases']))

                return i['hospitalCases']

        logging.error("no hospital cases found")

    #getting data for the total number of deaths
    elif search == "deaths_total":
        for i in data:
            if not(i['cumDailyNsoDeathsByDeathDate'] == None):
                logging.info("fetched total number of deaths")
                logging.debug("total deaths is: " + str(i['cumDailyNsoDeathsByDeathDate']))

                return i['cumDailyNsoDeathsByDeathDate']
    logging.error("no data found")

def remove_scheduled_event(label_name):
    """argument string
    the text in the label of index.html when the submit button is clicked

    removes the update with the name label_name from scheduled_updates

    """
    logging.info("removing scheduled event")

    for i in range(len(scheduled_updates)):
        if scheduled_updates[i]['title'] == label_name:
            del scheduled_updates[i]
            break 

def check_if_update_present(label_name):
    """argument string
    the text in the label of index.html when the submit button is clicked

    checks to see if the covid data should still be updated or the user as decided not to update before hand
    by clicking the x of the list of scheduled events

    return boolean
    indicates whether or not label_name is present in scheduled_updates
    """
    logging.debug("checking if update is present")

    present = False
    for i in range(len(scheduled_updates)):
        if scheduled_updates[i]['title'] == label_name:
            present = True

    return present

def update_covid_data(label_name):
    """argument string
    the text in the label of index.html when the submit button is clicked

    function which updates all of the covid data global variables

    """
    #calls function which checks if label_name is present in scheduled_updates
    present = check_if_update_present(label_name)

    #updating the covid data
    if present:
        data_exeter = covid_API_request()["data"]
        data_england = covid_API_request(defualt_national_location, defualt_national_location_type)["data"]
        infections_local = fetch_specified_covid_data(data_exeter,'7day_infections')
        infections_national = fetch_specified_covid_data(data_england, '7day_infections')
        hospital_cases = fetch_specified_covid_data(data_england, 'hospital_cases')
        death_total = fetch_specified_covid_data(data_england, 'deaths_total')
    else:
        logging.debug("an update was not executed as it was previously removed")

    logging.info("updated covid data")

def update_covid_data_non_repeating(label_name):
    """argument string
    the text in the label of index.html when the submit button is clicked

    called when the user doesn't want the update to repeat every day
    updates the covid data once
    
    """
    #calling function that updates the covid data
    update_covid_data(label_name)

    #calling function that removes the update from the list of updates
    remove_scheduled_event(label_name)

def update_covid_data_repeating(label_name):
    """argument string
    the text in the label of index.html when the submit button is clicked

    called when the user does want the update to repeat every day
    updates the covid data every 24 hours

    """
    #calling function that updates the covid data
    update_covid_data(label_name)

    #repeationg the update in 24 hours
    logging.debug("scheduled update " + str(label_name) + " to repeat in 24 hours")

    e2 = s.enter(24*60*60, 1, update_covid_data_repeating)

def schedule_covid_updates(update_interval, update_name, repeat = False):
    """int, string, bool
    delay until the update, the text in the label of index.html when the submit button is clicked, check to see if the user wants the update to repeat or not

    schedules the covid updates

    """
    #checks to see if the user wants to repeats the update then schedules accordingly 
    logging.info("scheduling a covid update")

    try:
        assert type(update_name) == str
        logging.debug("test, assert type(update_name) == str, passed")
    except:
        logging.error("test, assert type(update_name) == str, failed")

    if repeat:
        logging.debug("scheduling repeating update")

        e1 = s.enter(update_interval,1,update_covid_data_repeating, update_name)
    else:
        e1 = s.enter(update_interval,1,update_covid_data_non_repeating, update_name)

def schedule_news_function(label_name):
    """argument string
    the text in the label of index.html when the submit button is clicked

    updates the news
    does not update news which the user has previously requested not to update
    i.e clicked the x on the news article

    """
    present = check_if_update_present(label_name)
    
    if present:
        #calling functuion to update the news articles
        #from covid_news_handling
        update_news("Covid COVID-19 coronavirus", articles)

        #removing articles which have previously been deleted
        for rem in deleted_articles:
            remove_news_article(rem)

def schedule_news_function_non_repeating(label_name):
    """argument string
    the text in the label of index.html when the submit button is clicked

    updates the news
    only does this once

    """
    #calls function which updates the news
    schedule_news_function(label_name)

    #calls function which removes the event from scheduled_updates
    remove_scheduled_event(label_name)

def schedule_news_function_repeating(label_name):
    """argument string
    the text in the label of index.html when the submit button is clicked

    updates the news
    repeats this every 24 hours

    """
    #calls function which updates the news
    schedule_news_function(label_name)
    
    #reschedules the event in 24 hours
    e2 = s.enter(24*60*60, 1, schedule_news_function_repeating, label_name)

    logging.debug("repeating the exectued news update in 24 hours")

def schedule_news_update(repeat = False, desired_time = "00:00", label_name = ""):
    """argument bool, string, string
    check to see if the user wants the update to repeat or not, time at which the updates happens, the text in the label of index.html when the submit button is clicked
    
    schedules the news updates

    """
    #checks to see if the user wants to repeats the update then schedules accordingly 
    logging.info("scheduling a news update")

    try:
        assert type(label_name) == str
        logging.debug("test, assert type(label_name) == str, passed")
    except:
        logging.error("test, assert type(label_name) == str, failed")

    if repeat:
        e1 = s.enter(calc_time.get_delay(desired_time),1,schedule_news_function_repeating, label_name)##updates when desired time is met
    else:
        e1 = s.enter(calc_time.get_delay(desired_time),1,schedule_news_function_non_repeating, label_name)##updates when desired time is met

def remove_news_article(to_remove_article = ""):
    """argument string
    title of article which is to be removed

    removes a news article from the list of articles when the x is clicked on the list of news articles

    """
    logging.info("removing a news article")

    for art in articles:
        if art['title'] == to_remove_article:
            articles.remove(art)
    if not(to_remove_article in deleted_articles):
        deleted_articles.append(to_remove_article)
        logging.debug("appended deleted article to deleted_articles")

def manage_url():
    """

    calls the functions which are needed to perform the tasks which the user specifies
    the sepcified tasks appear in the url when specified

    """
    #Text in the label the user inputs 
    label_name = request.args.get('two')
    logging.debug("request in label is " + str(label_name))
    
    #checking to see if the event with that name already exists 
    allow = True
    for up_dicts in scheduled_updates:
        if up_dicts['title'] == label_name:#in log draw them having the same label as an existing one as an error, mention this in README.txt
            allow = False
            logging.warning("user tried to enter an update with the same label_name as an existing update")

    #checks if there is text in the label and the text is allowed
    if label_name and allow:
        update_time = request.args.get('update')
        logging.debug("desired time for update is " + str(update_time))

        #variable to check if the user wants the update to repeat
        to_repeat = request.args.get('repeat')

        #checks to see if the user did enter a desired time for the update
        if update_time != "":

            #checks to see if the news should be updated
            to_update_news = request.args.get('news')
            if to_update_news == 'news':
                logging.debug("user wishes to schedule an update for news")
                if to_repeat:
                    schedule_news_update(True, update_time, label_name)
                else:
                    schedule_news_update(False, update_time, label_name)

            #checks to see if the covid data should be updated
            to_update_covid = request.args.get('covid-data')
            if to_update_covid == 'covid-data':
                logging.debug("user wishes to schedule an update for covid data")
                if to_repeat:
                    schedule_covid_updates(calc_time.get_delay(update_time), label_name, True)
                else:
                    schedule_covid_updates(calc_time.get_delay(update_time), label_name, False)

            #adding the event to schedule_updates
            new_event = {'title': label_name, 'content': "Update schedueld for " + update_time}
            scheduled_updates.append(new_event)
            logging.info("added new update to list of updates")
            logging.debug("list of scheduled updates is now" + str(scheduled_updates))
        else:
            logging.warning("no update time yet there has been a label submitted")

    #if the user wants to remove a news article
    to_remove_article = request.args.get('notif')
    if to_remove_article:
        logging.info("user wishes ro remove an article of name" + str(to_remove_article))
        remove_news_article(to_remove_article)

    #if the user wants to remove an update
    to_remove_event = request.args.get('update_item')
    if to_remove_event:
        logging.info("user wishes ro remove an article of name" + str(to_remove_event))
        remove_scheduled_event(to_remove_event)

#ran when the user first loads the page
@app.route('/')
def startup_page():
    """

    code and variables for when the page first runs

    """
    logging.info("Loading Original Website")

    #runs the scheduler
    s.run(blocking=False)

    #assigning the correct variables to their respective postitions on the template
    return render_template('index.html',
    title='Daily Update',
    location = 'Exeter', local_7day_infections = infections_local,
    nation_location = 'England', national_7day_infections = infections_national,
    hospital_cases = 'Current hospitals cases: ' + str(hospital_cases),
    deaths_total = 'Total deaths: ' + str(death_total),
    news_articles = articles,
    updates = scheduled_updates,
    image = image_name)

#ran after the first time the page refreshes
@app.route('/index')
def index():
    """

    code and variables for when the page refreshes
    
    """
    logging.info("Loading updated Website")

    #calls the function which calls the functions which are needed to perform the tasks which the user specifies
    manage_url()
    
    #runs the scheduler
    s.run(blocking=False)

    #assigning the correct variables to their respective postitions on the template
    return render_template('index.html',
    title='Daily Update',
    location = 'Exeter', local_7day_infections = infections_local,
    nation_location = 'England', national_7day_infections = infections_national,
    hospital_cases = 'Current hospitals cases: ' + str(hospital_cases),
    deaths_total = 'Total deaths: ' + str(death_total),
    news_articles = articles,
    updates = scheduled_updates,
    image = image_name)

#this is what is run first
if __name__ == '__main__':
    #setting up log file
    logging.basicConfig(filename=filepath, encoding='utf-8' , format='%(name)s - %(levelname)s - %(message)s', level= logging.DEBUG)

    #updating the respective variables to the correct values at the start of the program
    data_exeter = covid_API_request()["data"]
    data_england = covid_API_request(defualt_national_location, defualt_national_location_type)["data"]
    infections_local = fetch_specified_covid_data(data_exeter,'7day_infections')
    infections_national = fetch_specified_covid_data(data_england, '7day_infections')
    hospital_cases = fetch_specified_covid_data(data_england, 'hospital_cases')
    death_total = fetch_specified_covid_data(data_england, 'deaths_total')
    articles = update_news("Covid COVID-19 coronavirus", articles)

    logging.info("Fetched initial covid and news data")
 
    #runs the flask application
    app.run()

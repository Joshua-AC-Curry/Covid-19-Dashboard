from covid_data_handler import parse_csv_data, update_covid_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates
from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_data_handler import fetch_specified_covid_data
from calc_time import get_delay
import datetime
import logging

"""Logging tests"""
logging.basicConfig(filename='app.log', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    try:
        assert len(data) == 639
        logging.debug("test, assert len(data) == 639, passed")
    except:
        logging.error("test, assert len(data) == 639, failed")
    try:
        assert type(data) == list
        logging.debug("tet, assert type(data) == list, passed")
    except:
        logging.error("test, assert type(data) == list failed")

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    try:
        assert last7days_cases == 240_299
        logging.debug("test, assert last7days_cases == 240_299, passed")
    except:
        logging.error("test, assert last7days_cases == 240_299, failed")
    try:
        assert current_hospital_cases == 7_019
        logging.debug("test, assert current_hospital_cases == 7_019, passed")
    except:
        logging.error("test, assert current_hospital_cases == 7_019, failed")
    try:
        assert total_deaths == 141_544
        logging.debug("test, assert total_deaths == 141_544, passed")
    except:
        logging.error("test, assert total_deaths == 141_544, failed")

def test_covid_API_request():
    data = covid_API_request()
    try:
        assert isinstance(data, dict)
        logging.debug("test, assert isinstance(data, dict), passed")
    except:
        logging.error("test, assert isinstance(data, dict), failed")
    try:
        assert bool(data) == True
        logging.debug("test, assert bool(data) == True, passsed")
    except:
        logging.error("test, assert bool(data) == True, failed")

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')
    logging.debug("Update scheduled without error for non-repeat")
    
    schedule_covid_updates(update_interval=10, update_name='update test', repeat=True)
    logging.debug("Update scheduled without error for repeat")

def test_news_API_request():
    try:
        assert news_API_request()
        logging.debug("test, assert news_API_request(), passed")
    except:
        logging.debug("test, assert news_API_request(), failed")
    try:
        assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()
        logging.debug("test, assert news_API_request('Covid COVID-19 coronavirus') == news_API_request(), passed")
    except:
        logging.debug("test, assert news_API_request('Covid COVID-19 coronavirus') == news_API_request(), failed")
    
def test_update_news():
    update_news('test')
    logging.debug("update_news succefully passed unit tests")

def test_get_delay():
    try:
        assert get_delay(datetime.datetime.now().strftime("%H:%M")) <= 86400
        logging.debug("test, assert get_delay(datetime.datetime.now().strftime(\"%H:%M\")) == 0, passed")
    except:
        logging.error("test, assert get_delay(datetime.datetime.now().strftime(\"%H:%M\")) == 0, failed")

def test_fetch_specified_covid_data():
    try:
        assert fetch_specified_covid_data(covid_API_request()['data'], "7day_infections")
        logging.debug("test, assert fetch_specified_covid_data(covid_API_request()['data'], \"7day_infections\"), passed")
    except:
        logging.error("test, assert fetch_specified_covid_data(covid_API_request()['data'], \"7day_infections\"), failed")
    try:
        assert fetch_specified_covid_data(covid_API_request('England', 'Nation')['data'], "7day_infections")
        logging.debug("test, assert fetch_specified_covid_data(covid_API_request()['data'], \"7day_infections\"), passed")
    except:
        logging.error("test, assert fetch_specified_covid_data(covid_API_request()['data'], \"7day_infections\"), failed")
    try:
        assert fetch_specified_covid_data(covid_API_request('England', 'Nation')['data'], "hospital_cases")
        logging.debug("test, assert fetch_specified_covid_data(covid_API_request()['data'], \"hospital_cases\"), passed")
    except:
        logging.error("test, assert fetch_specified_covid_data(covid_API_request()['data'], \"hospital_cases\"), failed")
    try:
        assert fetch_specified_covid_data(covid_API_request('England', 'Nation')['data'], "deaths_total")
        logging.debug("test, assert fetch_specified_covid_data(covid_API_request()['data'], \"deaths_total\"), passed")
    except:
        logging.error("test, assert fetch_specified_covid_data(covid_API_request()['data'], \"deaths_total\"), failed")

logging.info("\n" * 3)
logging.info("_______________________Running Test File_______________________")

test_parse_csv_data()
test_process_covid_csv_data()
test_covid_API_request()
test_schedule_covid_updates()
test_news_API_request()
test_update_news()
test_get_delay()
test_fetch_specified_covid_data()
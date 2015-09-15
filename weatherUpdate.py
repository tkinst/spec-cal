__author__ = 'tk'

import requests
from datetime import date, datetime, timedelta
from SpecWeather import WeatherUpdate, db
from time import sleep
from sqlalchemy import desc

API_KEY = "" # insert your wunderground api key here

def query(location, target_date):

    lastWeatherUpdate = WeatherUpdate.query.filter_by(location=location).order_by(WeatherUpdate.date.desc()).first()
    if not lastWeatherUpdate:
        lastUpdateDate = datetime(2015, 1, 31)
    else:
        lastUpdateDate = lastWeatherUpdate.date

    datestring = "%d%02d%02d" % (target_date.year, target_date.month, target_date.day)

    print str(location) + " / " + datestring

    URI = "http://api.wunderground.com/api/%s/history_%s/q/NY/%s.json" % (API_KEY,datestring,location)

    r = requests.get(URI)
    data = r.json()


    raincount = 0.0
    is_rain = False

    for eachEntry in data['history']['observations']:

        precipi = float(eachEntry['precipi'])
        if precipi < 0:
            precipi = 0

        entry_datetime = datetime(int(eachEntry['date']['year']),int(eachEntry['date']['mon']),int(eachEntry['date']['mday']),int(eachEntry['date']['hour']),int(eachEntry['date']['min']))

        if entry_datetime > lastUpdateDate:
            newUpdate = WeatherUpdate(entry_datetime, location, precipi)
            db.session.add(newUpdate)
            db.session.commit()


if __name__ == "__main__":
    # locations = ["West_Nyack", "Haverstraw", "Goshen", "Maybrook", "Newburgh", "New_Hamburg", "Tomkins_Cove"]
    locations = ['Blauvelt','Congers_FD','Crugers','Wappingers_Falls','Maybrook','Goshen']

    counter = 0

    for loc in locations:
        lastWeatherUpdate = WeatherUpdate.query.filter_by(location=loc).order_by(WeatherUpdate.date.desc()).first()
        if not lastWeatherUpdate:
            lastUpdateDate = datetime(2015, 3, 31)
        else:
            lastUpdateDate = lastWeatherUpdate.date

        numdays = datetime.now() - lastUpdateDate
        date_list = [datetime.now() - timedelta(days=x) for x in range(0, numdays.days)]
        date_list.append(datetime.now())

        date_list.sort()

        for target_day in date_list:
            query(loc, target_day)
            counter += 1
            if counter == 8:
                sleep(60)
                counter = 0

        print str(loc)
        print "Calls: " + str(counter)
        print "---"
        #sleep(60)

from flask import Flask, jsonify, redirect, make_response, render_template
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from sqlalchemy import func
from flask.ext.cors import CORS
import simplejson as json


app = Flask(__name__)
api = restful.Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

CORS(app, resources=r'/*')

class WeatherUpdateResource(restful.Resource):
    def get(self, location):
        updates = WeatherUpdate.query.filter_by(location=location).all()

        the_array = []
        the_dict = {}

        for eachItem in updates:
            the_array.append(eachItem.as_dict())

        the_dict['data'] = the_array
        return jsonify(the_dict)


class byDayResource(restful.Resource):
    def get(self, location):
        precip_dates = db.session.query(func.sum(WeatherUpdate.precipitation), WeatherUpdate.date).filter_by(location=location).group_by(func.extract('day',WeatherUpdate.date), func.extract('month', WeatherUpdate.date)).all()

        counter = 1
        the_array = []
        the_dict = {}

        for precip, eachDate in precip_dates:
            y = {'id': counter,
            'title': str(location) + ": " + str(precip) + "in",
            'allDay': True,
            'start' :eachDate.date().isoformat(),
            # 'end':'',
            'url':'',
            'color': ''}

            if precip > 0.1:
                y['color'] = '#FF0000'
            elif precip > 0:
            	y['color'] = '#ff912f'

            the_array.append(y)

            counter += 1

        # the_dict['events'] = the_array

        # return jsonify(the_dict)
        return make_response(json.dumps(the_array))



class allDayResource(restful.Resource):
    def get(self):
        precip_dates = db.session.query(func.sum(WeatherUpdate.precipitation), WeatherUpdate).group_by(WeatherUpdate.location, func.extract('day',WeatherUpdate.date), func.extract('month', WeatherUpdate.date)).all()

        counter = 1
        the_array = []
        the_dict = {}

        for precip, eachUpdate in precip_dates:
            url = "http://spec-cal.tomkinstrey.com/single/%s/%s/%s/%s/" % (eachUpdate.location,eachUpdate.date.year,eachUpdate.date.month,eachUpdate.date.day)


            y = {'id': counter,
            'title': str(eachUpdate.location) + ": " + str(precip) + "in",
            'allDay': True,
            'start' :eachUpdate.date.date().isoformat(),
            # 'end':'',
            'url': url,
            'color': ''}

            if precip > 0.1:
                y['color'] = '#FF0000'
            elif precip > 0:
            	y['color'] = '#ff912f' 

            the_array.append(y)

            counter += 1

        # the_dict['events'] = the_array

        # return jsonify(the_dict)
        return make_response(json.dumps(the_array))


# class singleDay(restful.Resource):
@app.route('/single/<string:location>/<int:year>/<int:month>/<int:day>/')
def singleDayView(location, year, month, day):
    updates = WeatherUpdate.query.filter_by(location=location).filter(WeatherUpdate.date > datetime(year, month, day)).filter(WeatherUpdate.date < datetime(year, month, day, 23, 59, 59)).all()

    return render_template('single.html', updates=updates, location=location, year=year, month=month, day=day)




api.add_resource(allDayResource, '/cal/')
api.add_resource(byDayResource, '/cal/<string:location>')
api.add_resource(WeatherUpdateResource, '/<string:location>')
# api.add_resource(singleDay, '/single/<string:location>/<int:year>/<int:month>/<int:day>')

@app.route('/')
def hello_world():
    counter = 1
    return render_template('app.html')


@app.route("/updatedb")
def updatedb():
    db.create_all()
    return redirect('/')


class WeatherUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    location = db.Column(db.String(60))
    precipitation = db.Column(db.Float())


    def __init__(self, date, location, precipitation):
        self.date = date
        self.location = location
        self.precipitation = precipitation

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = getattr(self, c.name)

        return d

        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<WeatherUpdate %r>' % self.id


if __name__ == '__main__':
    app.run(debug=True)

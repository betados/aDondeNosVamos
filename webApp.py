#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, request
from wtforms import Form, TextAreaField, validators, StringField, PasswordField
import random
import sqlite3
import googlemaps
import pprint


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

conn = sqlite3.connect('dataBases/data.db')
c = conn.cursor()
t = ('mapsKey',)
c.execute('SELECT value FROM data WHERE name=?', t)
key = c.fetchone()[0]
gmaps = googlemaps.Client(key=key)


class tavel_name_form(Form):
    travel_name = StringField('Nombre de tu viaje:', validators=[validators.required()])
    password = PasswordField('Contraseña:  ', validators=[validators.required()])
    password2 = PasswordField('Repite la contraseña:', validators=[validators.required()])


class travel_questionnaire_form(Form):
    user_name = StringField('Tu nombre:', validators=[validators.required()])

    origin = TextAreaField('Origen:', validators=[validators.required()],
                           default='Madrid')
    destinations = TextAreaField('Destinos:', validators=[validators.required()],
                                 # description='destinos separados con ;',
                                 # default='destinos separados con ;')
                                 default='Barakaldo; Cádiz')


def createUrl():
    """ Creates a random url unique for each travel"""
    url = ''
    for _ in range(9):
        code = random.randrange(36)
        if code in range(10):
            code += 48
        elif code in range(10, 36):
            code += 87
        url += chr(code)
    return url


def createTravel(name, password, url):
    conn = sqlite3.connect('dataBases/viajes.db')
    c = conn.cursor()
    values = (name, password, url)
    c.execute('create table if not exists viajes(name, password, url)')
    c.execute('insert into viajes values (?,?,?)', values)
    conn.commit()


def saveAnswer(url, travel_name, user_name, respuesta):
    conn = sqlite3.connect('dataBases/viajes.db')
    c = conn.cursor()
    values = (url, travel_name, user_name, respuesta)
    c.execute('create table if not exists respuestas(url, travel_name, user_name, respuesta)')
    c.execute('insert into respuestas values (?,?,?,?)', values)
    conn.commit()

def getLatsLongs(places):
    lats = []
    longs = []
    for place in places:
        lat, lng = getLatLong(place)
        lats.append(str(lat))
        longs.append(str(lng))

    return ';'.join(lats), ';'.join(longs)

def getLatLong(place):
    data = gmaps.geocode(place, components={'country': 'ES'})
    return data[0]['geometry']['location']['lat'], data[0]['geometry']['location']['lng']


@app.route("/", methods=['GET', 'POST'])
def home():

    form = tavel_name_form(request.form)
    print(form.errors)

    if request.method == 'POST':
        travel_name = request.form['travel_name']
        password = request.form['password']
        password2 = request.form['password2']

        if form.validate():
            if password == password2:
                url = createUrl()
                flash('La URL para compartir con tus compañeras de viaje es: ' + request.url + url)
                createTravel(travel_name, password, url)
                return render_template('home.html', form=form, link=request.url + url)
            else:
                flash('Las contraseñas no coinciden')
                return render_template('home.html', form=form, link=None)
        else:
            flash('All the form fields are required. ')
            return render_template('home.html', form=form, link=None)

    else:
        return render_template('home.html', form=form, link=None)


@app.route('/<url>', methods=['GET', 'POST'])
def show_questionnaire(url):
    conn = sqlite3.connect('dataBases/viajes.db')
    c = conn.cursor()
    values = (url,)
    c.execute('SELECT name FROM viajes WHERE url=?', values)
    try:
        travel_name = c.fetchone()[0]
    except:
        return render_template('404.html')

    from flask import request


    admin = request.args.get('admin', type=bool)
    if admin:
        # TODO hacer que pida la contraseña para acceder a esto
        conn = sqlite3.connect('dataBases/viajes.db')
        c = conn.cursor()
        values = (travel_name,)
        c.execute('SELECT * FROM respuestas WHERE travel_name=?', values)
        query_result = c.fetchall()
        # [0]
        return render_template('results.html', travel_name=travel_name, query_result=query_result)

    form = travel_questionnaire_form(request.form)
    # flash('Nombre del viaje: %s' % travel_name)

    if request.method == 'POST':
        user_name = request.form['user_name']
        destinations = request.form['destinations']
        origin = request.form['origin']

        if form.validate():
            saveAnswer(url, travel_name, user_name, destinations)
            destinations = destinations.split(';')
            lats, longs = getLatsLongs(destinations)
            # TODO pasar una lista con todos los destinos
            return render_template('map.html', key=key, latArray=lats, longArray=longs)

    return render_template('questionnaire.html', form=form, travel_name=travel_name, url=url)

@app.route('/map')
def show_map():
    # FIXME esto solo sirve para debuguear
    return render_template('map.html', key=key, latArray='40.4;43.2;36.5', longArray='-3.7;-2.9;-6.3')



if __name__ == "__main__":
    app.run()

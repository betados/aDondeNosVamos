#!/usr/bin/python
# -*- coding: utf-8 -*-

import googlemaps
from datetime import datetime
import sqlite3


def getDistance(origen='Madrid', destino='Madrid'):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    t = ('mapsKey',)
    c.execute('SELECT value FROM data WHERE name=?', t)
    key = c.fetchone()[0]
    # print(key)
    gmaps = googlemaps.Client(key=key)

    # Geocoding an address
    # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

    # Look up an address with reverse geocoding
    # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

    # Request directions via public transit
    # now = datetime.now()
    # directions_result = gmaps.directions('Madrid', 'Santander, Cantabria', mode="transit", departure_time=now)
    directions_result = gmaps.directions(origen, destino, mode="driving")

    # print(directions_result[0])
    print('Distancia de', origen, 'a', destino, ':', end=' ')
    print(directions_result[0]['legs'][0]['distance']['text'])

destinos = ['Bilbao', 'Santander, Cantabria', 'Valencia, Comunidad valenciana']
for destino in destinos:
    getDistance(origen='Madrid', destino=destino)

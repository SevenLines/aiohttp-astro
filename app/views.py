import traceback
from asyncio.tasks import sleep
from datetime import datetime, timedelta

import aiohttp
import aiohttp_jinja2
import ephem
from aiohttp import web
import json
import asyncio
import astropy.units as u
from astropy.coordinates import EarthLocation, get_moon, AltAz, get_sun
from astropy.time import Time

from app import settings


class IndexPage(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        tm = Time(datetime.now()) - 8 * u.hour
        location = EarthLocation(lat=52 * u.deg, lon=104 * u.deg)

        moon = get_moon(tm, location)
        moon_altaz = moon.transform_to(AltAz(obstime=tm, location=location))
        sun = get_sun(tm)
        sun_altaz = sun.transform_to(AltAz(obstime=tm, location=location))

        return {
            'moon_altaz': moon_altaz,
            'sun_altaz': sun_altaz,
        }


class ObjectsPositionView(web.View):
    ws = None
    lat = settings.LAT
    lon = settings.LON
    active = False

    def __init__(self, request):
        super().__init__(request)
        self.gatech = ephem.Observer()
        self.planets = {
            'moon': {'ephem': ephem.Moon(), 'last_ecliptic': None, 'ecliptic': None, 'day': {
                'number': '',
                'start': None,
                'end': None,
            }},
            'sun': {'ephem': ephem.Sun(), 'last_ecliptic': None, 'ecliptic': None},
            'mars': {'ephem': ephem.Mars(), 'last_ecliptic': None, 'ecliptic': None},
            'jupiter': {'ephem': ephem.Jupiter(), 'last_ecliptic': None, 'ecliptic': None},
            'saturn': {'ephem': ephem.Saturn(), 'last_ecliptic': None, 'ecliptic': None},
            'mercury': {'ephem': ephem.Mercury(), 'last_ecliptic': None, 'ecliptic': None},
            'pluto': {'ephem': ephem.Pluto(), 'last_ecliptic': None, 'ecliptic': None},
            'neptune': {'ephem': ephem.Neptune(), 'last_ecliptic': None, 'ecliptic': None},
            'uranus': {'ephem': ephem.Uranus(), 'last_ecliptic': None, 'ecliptic': None},
            'venus': {'ephem': ephem.Venus(), 'last_ecliptic': None, 'ecliptic': None},
        }

    async def calculate_moon_day(self, info):
        if self.lon and self.lat:
            moon = ephem.Moon()
            obs = ephem.Observer()
            obs.lat = str(self.lat)
            obs.lon = str(self.lon)
            obs.date = self.gatech.date

            date_start = ephem.previous_new_moon(obs.date)
            date_next_new_moon = ephem.next_new_moon(obs.date)

            last_day = date_start
            for i in range(1, 30):
                obs.date = last_day
                day_end = obs.next_rising(moon, last_day, True)
                if last_day <= self.gatech.date <= day_end:
                    info['day']['number'] = i
                    info['day']['start'] = '{:%Y-%m-%d %H:%M:%S}'.format(last_day.datetime())
                    info['day']['end'] = '{:%Y-%m-%d %H:%M:%S}'.format(day_end.datetime())
                    break
                last_day = day_end

    async def calculate_planet(self, info):
        info['ephem'].compute(self.gatech)
        info['ecliptic'] = ephem.Ecliptic(info['ephem'])
        info['reverse'] = info['ecliptic'].lon - info['last_ecliptic'].lon < 0 \
            if info['last_ecliptic'] else False

    async def update_positions(self):
        self.gatech.lon = str(self.lon)
        self.gatech.lat = str(self.lat)
        self.gatech.date = datetime.utcnow()

        for planet, info in self.planets.items():
            await self.calculate_planet(info)

        # if self.planets['moon']['day']['start'] is None:
        self.calculate_moon_day(self.planets['moon'])

        for planet, info in self.planets.items():
            info['last_ecliptic'] = info['ecliptic']

    async def compute_positions(self):
        if self.ws and not self.ws.closed:
            try:
                if self.lon and self.lat:
                    await self.update_positions()
                    await self.ws.send_json({
                        'planets': [{
                            'name': name,
                            'alt': round(info['ephem'].alt, 2),
                            'az': round(info['ephem'].az, 2),
                            'ra': round(info['ephem'].ra, 2),
                            'dec': round(info['ephem'].dec, 2),
                            'lon': round(info['ecliptic'].lon, 2),
                            'day': info.get('day', None),
                            'reverse': info['reverse']
                        } for name, info in self.planets.items()]
                    })
            except Exception as exp:
                traceback.print_exc()
            await sleep(5)
            asyncio.ensure_future(self.compute_positions())

    async def set_location(self, lat, lon):
        self.lat = lat
        self.lon = lon
        await self.calculate_moon_day(self.planets['moon'])

    async def get(self):
        self.ws = web.WebSocketResponse()
        await self.ws.prepare(self.request)

        print('websocket connection opened')
        self.request.app['websockets'].append(self.ws)

        asyncio.ensure_future(self.compute_positions())

        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await self.ws.close()
                else:
                    try:
                        data = json.loads(msg.data)
                        print(data)
                        if data['type'] == 'set_location':
                            await self.set_location(**data['data'])
                    except Exception as ex:
                        print(ex)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % self.ws.exception())
            else:
                pass

        self.request.app['websockets'].remove(self.ws)
        print('websocket connection closed')

        return self.ws

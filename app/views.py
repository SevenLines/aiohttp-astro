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
    lat = None
    lon = None
    active = False

    gatech = ephem.Observer()

    def __init__(self, request):
        super().__init__(request)
        self.planets = {
            'moon': ephem.Moon(),
            'sun': ephem.Sun(),
            'mars': ephem.Mars(),
            'jupiter': ephem.Jupiter(),
            'saturn': ephem.Saturn(),
            'mercury': ephem.Mercury(),
            'pluto': ephem.Pluto(),
            'neptune': ephem.Neptune(),
            'uranus': ephem.Uranus(),
            'venus': ephem.Venus(),
        }

    async def compute_positions(self):
        if self.ws and not self.ws.closed:
            try:
                if self.lon and self.lat:
                    self.gatech.lon = str(self.lon)
                    self.gatech.lat = str(self.lat)
                    self.gatech.date = datetime.utcnow()

                    for planet, info in self.planets.items():
                        info.compute(self.gatech)

                    await self.ws.send_json({
                        'planets': [{
                            'name': name,
                            'alt': round(info.alt, 2),
                            'az': round(info.az, 2),
                            'ra': round(info.ra, 2),
                            'dec': round(info.dec, 2),
                            'lon': round(ephem.Ecliptic(info).lon, 2)
                        } for name, info in self.planets.items()]
                    })
            except Exception as exp:
                print(exp)
            await sleep(2)
            asyncio.ensure_future(self.compute_positions())

    async def set_location(self, lat, lon):
        self.lat = lat
        self.lon = lon

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

import asyncio
import json
import traceback
from asyncio.tasks import sleep
from datetime import datetime

import aiohttp
import ephem
from aiohttp import web

from app import planets
from app import settings
from app.helpers import DateTimeEncoder
from app.planets import Planet


class ObjectsPositionView(web.View):
    ws = None
    lat = settings.LAT
    lon = settings.LON
    active = False
    force_next_update = False

    def __init__(self, request):
        super().__init__(request)
        self.observer = ephem.Observer()
        self.planets = {
            'moon': planets.Moon(),
            'sun': planets.Sun(),
            'mars': planets.Mars(),
            'jupiter': planets.Jupiter(),
            'saturn': planets.Saturn(),
            'mercury': planets.Mercury(),
            'pluto': planets.Pluto(),
            'neptune': planets.Neptune(),
            'uranus': planets.Uranus(),
            'venus': planets.Venus(),
        }

    async def calculate_planet(self, planet: Planet, force: bool = False):
        planet.compute(self.observer, force=force)

    async def update_positions(self):
        self.observer.lon = str(self.lon)
        self.observer.lat = str(self.lat)
        self.observer.date = datetime.utcnow()

        for planet, planet in self.planets.items():
            await self.calculate_planet(planet, self.force_next_update)

    async def compute_positions(self):
        if self.ws and not self.ws.closed:
            try:
                if self.lon and self.lat:
                    await self.update_positions()
                    msg = json.dumps({
                        'planets': [planet.to_dict() for name, planet in self.planets.items()]
                    }, cls=DateTimeEncoder)
                    await self.ws.send_str(msg)
            except Exception:
                traceback.print_exc()
            await sleep(5)
            asyncio.ensure_future(self.compute_positions())

    async def set_location(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.force_next_update = True

    async def get(self):
        self.ws = web.WebSocketResponse()
        try:
            await self.ws.prepare(self.request)

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
                            traceback.print_exc()
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print('ws connection closed with exception %s' % self.ws.exception())
                else:
                    pass
        finally:
            self.request.app['websockets'].remove(self.ws)

        return self.ws

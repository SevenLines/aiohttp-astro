import asyncio
from asyncio import sleep
from datetime import datetime

import ephem


async def compute_positions(app):
    websockets = app['websockets'] if 'websockets' in app else []
    if websockets:
        moon = ephem.Moon()
        moon.compute(datetime.now())
        sun = ephem.Moon()
        sun.compute(datetime.now())

        gatech = ephem.Observer()
        gatech.lon

        for ws in websockets:
            await ws.send_json({
                'moon': {
                    'alt': str(moon.alt),
                    'az': str(moon.az),
                },
                'sun': {
                    'alt': str(sun.alt),
                    'az': str(sun.az),
                },
            })
    await sleep(1)
    asyncio.ensure_future(compute_positions(app))

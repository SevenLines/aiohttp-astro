import asyncio

import aiohttp_jinja2
import jinja2
from aiohttp import web

from app.background import compute_positions
from app.routes import routes
from app.signals import on_shutdown

loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('app'))

for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])
app.router.add_static('/static', "/home/m/PycharmProjects/moon/app/static", show_index=True, name="static")


app['websockets'] = []
# app.on_startup.append(compute_positions)
app.on_shutdown.append(on_shutdown)

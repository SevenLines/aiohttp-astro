from aiohttp.web import Application

from .views import ObjectsPositionView

routes = [
    ('*', '/ws/positions/', ObjectsPositionView, 'positions'),
]


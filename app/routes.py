from aiohttp.web import Application

from .views import IndexPage, ObjectsPositionView

routes = [
    ('*', '/', IndexPage, 'index'),
    ('*', '/ws/positions/', ObjectsPositionView, 'positions'),
]


import json

import ephem
import pytest
from ephem import Observer

from app.helpers import DateTimeEncoder
from app.planets import Sun
from app.views import ObjectsPositionView

#
# def async_test(f):
#     def wrapper(*args, **kwargs):
#         coro = asyncio.coroutine(f)
#         future = coro(*args, **kwargs)
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(future)
#
#     return wrapper
#
#
# class TestMoon(TestCase):
#     def test_moon_day_calulcation(self):
#         dt = datetime.utcnow()
#         moon = ephem.Moon()
#
#         obs = ephem.Observer()
#         obs.lat = '52.26312730000001'
#         obs.lon = '104.3399244'
#
#         new_moon = ephem.previous_new_moon(dt)
#         next_new_moon = ephem.next_new_moon(dt)
#         next_full_moon = ephem.next_full_moon(dt).datetime() + timedelta(hours=8)
#         last_day = new_moon
#         for i in range(1, 32):
#             obs.date = last_day
#             day_end = obs.next_rising(moon, last_day, True)
#             print("day {} {} - {}".format(i, last_day.datetime() + timedelta(hours=8),
#                                           day_end.datetime() + timedelta(hours=8)))
#             if day_end > next_new_moon:
#                 break
#             last_day = day_end
#
#         moon.compute(obs)
# #         print(moon)
#
# @pytest.fixture
# def observer():
#     obs = ephem.Observer()
#     obs.lat = '52.26312730000001'
#     obs.lon = '104.3399244'
#     return obs
#
#
# async def test_compute_moon(test_client):
#     view = ObjectsPositionView(None)
#     await view.set_location('52.26312730000001', '104.3399244')
#
#
# async def test_computation(test_client):
#     view = ObjectsPositionView(None)
#     await view.set_location(52.26312730000001, 104.3399244)
#     await view.update_positions()


@pytest.fixture
def observer():
    obs = ephem.Observer()
    obs.lat = '52.26312730000001'
    obs.lon = '104.3399244'
    return obs


@pytest.fixture
def view():
    v = ObjectsPositionView(None)
    return v


async def test_profile_computation(view: ObjectsPositionView):
    for _ in range(10000):
        await view.update_positions()
        server_time = view.observer.date.datetime().utcnow().isoformat()
        msg = json.dumps({
            'planets': [planet.to_dict() for name, planet in view.planets.items()],
            'server_time': server_time
        }, cls=DateTimeEncoder)


def test_sun_day(observer):
    planet = Sun()
    planet.compute(observer)


def test_asc_coordinate(observer: Observer):
    asc = ephem.Equatorial(0, 0)
    asc.compute(observer)
    print (asc.az)


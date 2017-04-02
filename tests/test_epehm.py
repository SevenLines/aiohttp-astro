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
#         print(moon)


async def test_compute_moon(test_client):
    view = ObjectsPositionView(None)
    await view.set_location('52.26312730000001', '104.3399244')


async def test_computation(test_client):
    view = ObjectsPositionView(None)
    await view.set_location(52.26312730000001, 104.3399244)
    await view.update_positions()

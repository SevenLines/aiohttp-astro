from datetime import datetime

import ephem
import pytest
from ephem import Observer

from app.planets import Moon


class TestMoon(object):
    @pytest.fixture
    def observer(self):
        obs = ephem.Observer()
        obs.lat = '52.26312730000001'
        obs.lon = '104.3399244'
        return obs

    @pytest.fixture
    def moon(self):
        return Moon()

    @pytest.mark.parametrize("dt,number", [
        (datetime(2017, 3, 28, 23), 1),
        (datetime(2017, 3, 29, 23), 2),
        (datetime(2017, 3, 30, 23), 3),
        (datetime(2017, 3, 31, 23), 4),
        (datetime(2017, 4, 1, 23), 5),
        (datetime(2017, 4, 2, 23), 6),
        (datetime(2017, 4, 3, 23), 7),
        (datetime(2017, 4, 4, 23), 8),
        (datetime(2017, 4, 5, 23), 9),
        (datetime(2017, 4, 6, 23), 10),
        (datetime(2017, 4, 7, 23), 11),
        (datetime(2017, 4, 8, 23), 12),
        (datetime(2017, 4, 9, 23), 13),
        (datetime(2017, 4, 10, 23), 14),
        (datetime(2017, 4, 11, 23), 15),
        (datetime(2017, 4, 12, 23), 16),
        (datetime(2017, 4, 13, 23), 17),
        (datetime(2017, 4, 14, 23), 18),
        (datetime(2017, 4, 15, 23), 19),
        (datetime(2017, 4, 16, 23), 20),
        (datetime(2017, 4, 17, 23), 21),
        (datetime(2017, 4, 18, 23), 22),
        (datetime(2017, 4, 19, 23), 23),
        (datetime(2017, 4, 20, 23), 24),
        (datetime(2017, 4, 21, 23), 25),
        (datetime(2017, 4, 22, 23), 26),
        (datetime(2017, 4, 23, 23), 27),
        (datetime(2017, 4, 24, 23), 28),
        (datetime(2017, 4, 25, 23), 29),
    ])
    def test_moon_day_calculation_simple(self, observer: Observer, moon: Moon, dt, number):
        observer.date = dt
        moon.compute(observer)
        assert moon.get_day()['number'] == number, (moon.get_day()['number'], number)

    @pytest.mark.parametrize("dt,number", [
        (datetime(2017, 3, 28, 12), 1),
        (datetime(2017, 3, 29, 1), 2),
        (datetime(2017, 3, 30, 1), 3),
        (datetime(2017, 3, 31, 1), 4),
        (datetime(2017, 4, 1, 1), 5),
        (datetime(2017, 4, 2, 1), 6),
        (datetime(2017, 4, 3, 1), 7),
        (datetime(2017, 4, 4, 1), 8),
        (datetime(2017, 4, 5, 1), 9),
        (datetime(2017, 4, 6, 1), 10),
        (datetime(2017, 4, 7, 1), 11),
        (datetime(2017, 4, 8, 1), 12),
        (datetime(2017, 4, 9, 1), 13),
        (datetime(2017, 4, 10, 1), 14),
        (datetime(2017, 4, 11, 1), 15),
        (datetime(2017, 4, 12, 1), 16),
        (datetime(2017, 4, 13, 1), 17),
        (datetime(2017, 4, 14, 1), 18),
        (datetime(2017, 4, 15, 1), 19),
        (datetime(2017, 4, 16, 1), 20),
        (datetime(2017, 4, 17, 1), 21),
        (datetime(2017, 4, 18, 1), 22),
        (datetime(2017, 4, 19, 1), 23),
        (datetime(2017, 4, 20, 1), 24),
        (datetime(2017, 4, 21, 1), 25),
        (datetime(2017, 4, 22, 1), 26),
        (datetime(2017, 4, 23, 1), 27),
        (datetime(2017, 4, 24, 1), 28),
        (datetime(2017, 4, 25, 1), 29),
        (datetime(2017, 4, 26, 1), 30),
        (datetime(2017, 4, 27, 1), 1),
    ])
    def test_moon_day_calculation_twelve(self, observer: Observer, moon: Moon, dt, number):
        moon.use_twelve_algorithm = True
        observer.date = dt
        moon.compute(observer)
        assert moon.get_day()['number'] == number, (dt, moon.get_day()['number'], number)

    def test_optimization_day_calculation_simple(self, observer: Observer, moon: Moon):
        observer.date = datetime(2017, 4, 3, 23)
        for i in range(10000):
            moon.compute(observer)
            assert moon.get_day()['number'] == 7, (moon.get_day()['number'], 7)

    def test_moon(self,  observer: Observer, moon: Moon):
        moon.compute(observer)
        print(moon)

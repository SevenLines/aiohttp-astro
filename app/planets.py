import traceback
from copy import copy

import ephem
from datetime import date, datetime, timedelta

import math
from ephem import Observer


class Planet(object):
    name = None
    ephem = None
    last_ecliptic = None
    ecliptic = None
    update_speed = 0

    _current_update_value = 0
    _updates_counter = 0

    def __init__(self):
        if self.name is None:
            self.name = self.get_name()
        if self.ephem is None:
            self.ephem = self.get_ephem()

    def get_name(self):
        return self.name or self.__class__.__name__.lower()

    def get_ephem(self):
        return self.ephem or getattr(ephem, self.name.capitalize())()

    def compute(self, observer: Observer, force=False):
        if self._updates_counter <= 2 or self._current_update_value <= 0:
            self.last_ecliptic = copy(self.ecliptic)

            self._current_update_value = self.update_speed
            self.ephem.compute(observer)
            if not self.ecliptic:
                self.ecliptic = ephem.Ecliptic(self.ephem)
            else:
                self.ecliptic.from_radec(self.ephem.ra, self.ephem.dec)
            self._updates_counter += 1
        else:
            self._current_update_value -= 1

    @property
    def is_reverse(self):
        return self.last_ecliptic and self.ecliptic.lon - self.last_ecliptic.lon < 0

    def get_day(self):
        return None

    def to_dict(self):
        return {
            'name': self.name,
            'alt': self.ephem.alt,
            'az': self.ephem.az,
            'ra': self.ephem.ra,
            'dec': self.ephem.dec,
            'lat': self.ecliptic.lat,
            'lon': self.ecliptic.lon,
            'day': self.get_day(),
            'reverse': self.is_reverse,
        }


class Sun(Planet):
    day_info = None

    def __init__(self):
        super().__init__()
        self.day_info = {
            'number': None,
            'month_number': None,
            'start': None,
            'end': None,
        }

    def compute(self, observer, force=False, **kwargs):
        super().compute(observer, **kwargs)

        if not force and self.day_info['start'] and self.day_info['end'] \
                and self.day_info['start'] < observer.date.datetime() < self.day_info['end']:
            pass
        else:
            obs = observer.copy()
            # find last spring equinox
            date_start = ephem.previous_spring_equinox(obs.date)
            obs.date = date_start

            # get start of first new day
            date_start = obs.next_rising(self.ephem)

            diff_days = (datetime.utcnow() - date_start.datetime()).days
            day = diff_days % 30 + 1
            month = diff_days // 30 + 1

            obs.date = datetime.utcnow()

            self.day_info['number'] = day
            self.day_info['month_number'] = month
            self.day_info['start'] = obs.previous_rising(self.ephem).datetime()
            self.day_info['end'] = obs.next_rising(self.ephem).datetime()

    def get_day(self):
        return self.day_info


class Moon(Planet):
    day_info = None
    use_twelve_algorithm = False  # использовать 12 градусный алгоритм рассчета дня

    def __init__(self):
        super().__init__()
        self.day_info = {
            'number': None,
            'start': None,
            'end': None,
        }

    def update_day_info_simple(self, observer: Observer, force=False):
        # calculate day only if we outside of previously computed period
        obs = observer.copy()
        dt = observer.date

        date_start = ephem.previous_new_moon(obs.date)
        date_next_new_moon = ephem.next_new_moon(obs.date)
        self.day_info['next_new_moon'] = date_next_new_moon.datetime()
        self.day_info['current_time'] = dt.datetime()

        last_day = date_start
        for i in range(1, 30):
            obs.date = last_day
            day_end = obs.next_rising(self.ephem, last_day, True)
            if last_day <= dt <= day_end:
                self.day_info['number'] = i
                self.day_info['start'] = last_day.datetime()
                self.day_info['end'] = day_end.datetime()
                break
            last_day = day_end

    def update_day_info_twelve(self, observer: Observer):
        sun = ephem.Sun()
        sun.compute(observer)
        sun_ecliptic = ephem.Ecliptic(sun)

        if self.ecliptic.lon > sun_ecliptic.lon:
            degress = math.degrees(self.ecliptic.lon - sun_ecliptic.lon)
        else:
            degress = 360 - math.degrees(sun_ecliptic.lon - self.ecliptic.lon)

        self.day_info['number'] = degress // 12 + 1

    def compute(self, observer: Observer, **kwargs):
        super(Moon, self).compute(observer, **kwargs)
        force = kwargs.get('force', False)

        try:
            if not force and self.day_info['start'] and self.day_info['end'] \
                    and self.day_info['start'] < observer.date.datetime() < self.day_info['end']:
                pass
            else:
                if self.use_twelve_algorithm:
                    self.update_day_info_twelve(observer)
                else:
                    self.update_day_info_simple(observer, force)
        except Exception as exc:
            traceback.print_exc()

    def get_day(self):
        return self.day_info


class Mars(Planet):
    update_speed = 4


class Jupiter(Planet):
    update_speed = 4


class Saturn(Planet):
    update_speed = 4


class Mercury(Planet):
    update_speed = 4


class Pluto(Planet):
    update_speed = 4


class Neptune(Planet):
    update_speed = 4


class Uranus(Planet):
    update_speed = 4


class Venus(Planet):
    update_speed = 4

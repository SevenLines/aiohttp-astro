import traceback

import ephem
from ephem import Observer


class Planet(object):
    name = None
    ephem = None
    last_ecliptic = None
    ecliptic = None
    is_reverse = False

    def __init__(self):
        if self.name is None:
            self.name = self.get_name()
        if self.ephem is None:
            self.ephem = self.get_ephem()

    def get_name(self):
        return self.name or self.__class__.__name__.lower()

    def get_ephem(self):
        return self.ephem or getattr(ephem, self.name.capitalize())()

    def compute(self, observer):
        self.ephem.compute(observer)
        self.ecliptic = ephem.Ecliptic(self.ephem)
        self.is_reverse = self.ecliptic.lon - self.last_ecliptic.lon < 0 if self.last_ecliptic else False
        self.last_ecliptic = self.ecliptic

    def get_day(self):
        return None

    def to_dict(self):
        return {
            'name': self.name,
            'alt': self.ephem.alt,
            'az': self.ephem.az,
            'ra': self.ephem.ra,
            'dec': self.ephem.dec,
            'lon': self.ecliptic.lon,
            'day': self.get_day(),
            'reverse': self.is_reverse,
        }


class Sun(Planet):
    pass


class Moon(Planet):
    day_info = None

    def __init__(self):
        super().__init__()
        self.day_info = {
            'number': None,
            'start': None,
            'end': None,
        }

    def compute(self, observer: Observer):
        super(Moon, self).compute(observer)

        try:
            obs = observer.copy()
            dt = observer.date

            date_start = ephem.previous_new_moon(obs.date)
            date_next_new_moon = ephem.next_new_moon(obs.date)

            last_day = date_start
            for i in range(1, 30):
                obs.date = last_day
                day_end = obs.next_rising(self.ephem, last_day, True)
                if last_day <= dt <= day_end:
                    self.day_info['number'] = i
                    self.day_info['start'] = '{:%Y-%m-%d %H:%M:%S}'.format(last_day.datetime())
                    self.day_info['end'] = '{:%Y-%m-%d %H:%M:%S}'.format(day_end.datetime())
                    break
                last_day = day_end
        except Exception as exc:
            traceback.print_exc()

    def get_day(self):
        return self.day_info


class Mars(Planet):
    pass


class Jupiter(Planet):
    pass


class Saturn(Planet):
    pass


class Mercury(Planet):
    pass


class Pluto(Planet):
    pass


class Neptune(Planet):
    pass


class Uranus(Planet):
    pass


class Venus(Planet):
    pass
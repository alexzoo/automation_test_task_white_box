import json

from api_server.api.handlers.basic_handlers import JSONHandler
from tornado.gen import coroutine
from tornado.web import HTTPError
from voluptuous.error import Invalid

from api_server.api.schema import temperature_validator

TEMPERATURE_SCALE_SYSTEM = {
    'K': 'Celsius',  # TODO: maybe this wrong?
    'C': 'Kelvin',
    'F': 'fahrenheit'
}

WATER_STATES = {  # TODO: rewrite this and use limits
    'Celsius': {
        'steam': tuple(range(100, 999999)),  # 99, 100, 9999999, 1000000
        'liquid': tuple(range(1, 99)),  # 0, 99, 100
        'ice': tuple(range(-999999, 0)),  # -274, -273, 0, 1
    },
    'Kelvin': {
        'steam': tuple(range(373, 999)),  # 372, 373, 374, 998, 999, 1000
        'liquid': tuple(range(274, 373)),  # 273, 274, 275, 372, 373, 374
        'ice': tuple(range(0, 273)),  # -1, 0, 1, 273, 273, 274
    },
    'Fahrenheit': {
        'steam': tuple(range(212, 9999)),  # 211, 212, 213, 9998, 9999, 10000
        'liquid': tuple(range(33, 211)),  # 32, 33, 34, 210, 211, 212
        'ice': tuple(range(-9999, 33)),  # -10000, -9999, -9998, 32, 33, 34
    }
}


class TemperatureHandler(JSONHandler):
    scale_system = 'Celsius'

    @coroutine
    def get(self):
        raw_temperature = self.get_argument('temperature')
        try:
            temperature = temperature_validator(raw_temperature)
        except Invalid as err:
            raise HTTPError(
                400,
                reason=err.error_message
            )
            return
        if temperature.isdigit():
            scale_system = self.scale_system
            digit_temperature = json.loads(temperature)
        else:
            scale_system = TEMPERATURE_SCALE_SYSTEM[temperature[-1]]
            digit_temperature = json.loads(temperature[:-1])

        water_states = WATER_STATES.get(scale_system)
        if water_states is None:
            raise HTTPError(
                400,
                reason='Unknown temperature scale system {}, with temperature {}'.format(
                    scale_system, temperature)
            )
            return
        for state, ranges in water_states.items():
            if digit_temperature in ranges:
                self.finish(state)
                return
        else:
            self.finish('unknown')
            return

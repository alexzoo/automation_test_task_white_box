import os
from operator import contains

import requests
import pytest

liquid = "b'liquid'"
steam ="b'steam'"
ice = "b'ice'"
error_fahreheith = "b'Unknown value for a Fahrenheit temperature scale'"
random_string = "-+=jlyvTQZоргесщЩo674642756@%$"
error_temperature = "Invalid temperature"

class TestMakeUrl:
    def setup_method(self):
        #  спросить не нужно ли перенести это все в инит(13-15 строки) а то ругается
        self.host = os.environ.get("test_host", "localhost:8888")
        self.command = "temperature_check"
        self.browser_url = f"http://{self.host}/{self.command}"


class TestTempCheckWithInvalidParams(TestMakeUrl):
    @pytest.mark.parametrize("defolt_temp, expected_response, right_condition", [
        (random_string, 400, error_temperature)
    ])
    def test_check_temp_params_from_temp_checker_with_invalid_temperature(
            self, defolt_temp, expected_response, right_condition
    ):
        response = requests.get(self.browser_url, params={"temperature": defolt_temp})
        assert response.status_code == expected_response
        assert contains(str(response.content), error_temperature)

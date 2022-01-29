import os
import requests
import pytest

liquid = "b'liquid'"
steam ="b'steam'"
ice = "b'ice'"


class TestMakeUrl:
    def setup_method(self):
        #  спросить не нужно ли перенести это все в инит(13-15 строки) а то ругается
        self.host = os.environ.get("test_host", "localhost:8888")
        self.command = "temperature_check"
        self.browser_url = f"http://{self.host}/{self.command}"


class TestTempCheckFahrenheit(TestMakeUrl):
    @pytest.mark.parametrize("defolt_temp, expected_response, right_condition", [
        ("33F", 200, liquid),
        ("-9999F", 200, ice),
        ("212F", 200, steam),
    ])
    @pytest.mark.xfail(reason="expected 200, but got 400 Unknown temperature scale system fahrenheit")
    def test_check_temp_params_from_temp_checker_fahrenheit_lower_valid_level(
            self, defolt_temp, expected_response, right_condition
    ):
        response = requests.get(self.browser_url, params={"temperature": defolt_temp})
        assert response.status_code == expected_response
        assert str(response.content) == right_condition
        # assert response.json().dumps == right_condition

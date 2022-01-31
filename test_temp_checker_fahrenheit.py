import os
import requests
import pytest

liquid = "b'liquid'"
steam ="b'steam'"
ice = "b'ice'"
error_fahreheith = "b'Unknown value for a Fahrenheit temperature scale'"


class TestMakeUrl:
    def setup_method(self):
        #  спросить не нужно ли перенести это все в инит(13-15 строки) а то ругается
        self.host = os.environ.get("test_host", "localhost:8888")
        self.command = "temperature_check"
        self.browser_url = f"http://{self.host}/{self.command}"


class TestTempCheckFahrenheit(TestMakeUrl):
    @pytest.mark.parametrize("defolt_temp, expected_response, right_condition", [
        ("33F", 200, liquid),
        ("-9999F", 400, error_fahreheith),
        ("212F", 200, steam),
    ])
    @pytest.mark.xfail(reason="""
                        expected 200, but got 400: 'Unknown temperature scale system fahrenheit', need to fix \
                        absolute zero at fahrenheit is -459.67 and the lowest range for ice need to fix, \
                        """)
    def test_check_temp_params_from_temp_checker_fahrenheit_the_lowest_level_from_temp_checker_range(
            self, defolt_temp, expected_response, right_condition
    ):
        response = requests.get(self.browser_url, params={"temperature": defolt_temp})
        assert response.status_code == expected_response
        assert str(response.content) == right_condition
        # assert response.json().dumps == right_condition

    @pytest.mark.parametrize("defolt_temp, expected_response, right_condition", [
        ("211F", 200, liquid),
        ("33F", 200, ice),
        ("9999F", 400, error_fahreheith),
    ])
    @pytest.mark.xfail(reason="""
                        expected 200, but got 400: 'Unknown temperature scale system fahrenheit', need to fix \
                        max. temp at fahrenheit for steam is 2192 and the highest range for steam need to fix,
                        max. temp at fahrenheit for ice is 32.9 and the highest range for ice need to fix
                        """)
    def test_check_temp_params_from_temp_checker_fahrenheit_the_highest_level_from_temp_checker_range(
            self, defolt_temp, expected_response, right_condition
    ):
        response = requests.get(self.browser_url, params={"temperature": defolt_temp})
        assert response.status_code == expected_response
        assert str(response.content) == right_condition

    @pytest.mark.parametrize("defolt_temp, expected_response, right_condition", [
        ("33.1F", 200, liquid),
        ("-459.67F", 200, ice),
        ("212.1F", 200, steam),
    ])
    @pytest.mark.xfail(reason="""
                        expected 200, but got 400: 'Unknown temperature scale system fahrenheit', need to fix \
                        expected 200 but got 500: 'Internal Server Error', need to fix the processing of floats numbers
                        """)
    def test_check_temp_params_from_temp_checker_fahrenheit_the_lowest_valid_level_with_float_numbers(
            self, defolt_temp, expected_response, right_condition
    ):
        response = requests.get(self.browser_url, params={"temperature": defolt_temp})
        assert response.status_code == expected_response
        assert str(response.content) == right_condition

    @pytest.mark.parametrize("defolt_temp, expected_response, right_condition", [
        ("33F", 200, liquid),
        ("-460F", 200, ice),
        ("212F", 200, steam),
    ])
    @pytest.mark.xfail(reason="expected 200, but got 400: 'Unknown temperature scale system fahrenheit', need to fix ")
    def test_check_temp_params_from_temp_checker_fahrenheit_the_lowest_valid_level_with_integers(
            self, defolt_temp, expected_response, right_condition
    ):
        response = requests.get(self.browser_url, params={"temperature": defolt_temp})
        assert response.status_code == expected_response
        assert str(response.content) == right_condition

    @pytest.mark.parametrize("defolt_temp, expected_response, right_condition", [
        # check that with this value result is ise not liquid
        ("32F", 200, ice),
        # check that with this value result is error because -459.67 is absolute zero
        ("-459F", 400, error_fahreheith),
        # check that with this value result is liquid not steam
        ("211F", 200, liquid),
    ])
    @pytest.mark.xfail(reason="""
                        expected 200, but got 400: 'Unknown temperature scale system fahrenheit', need to fix, \
                        expected 400, but got 500: 'Internal Server Error', need to fix
     """)
    def test_check_temp_params_from_temp_checker_fahrenheit_out_of_the_range_level_with_integers(
            self, defolt_temp, expected_response, right_condition
    ):
        response = requests.get(self.browser_url, params={"temperature": defolt_temp})
        assert response.status_code == expected_response
        assert str(response.content) == right_condition

    @pytest.mark.parametrize("defolt_temp, expected_response, right_condition", [
        ("31F", 200, ice),
        ("213F", 200, steam),
        ("33F", 200, liquid),
    ])
    @pytest.mark.xfail(reason="expected 200, but got 400: 'Unknown temperature scale system fahrenheit', need to fix")
    def test_check_temp_params_from_temp_checker_fahrenheit_the_highest_range_level_with_integers(
            self, defolt_temp, expected_response, right_condition
    ):
        response = requests.get(self.browser_url, params={"temperature": defolt_temp})
        assert response.status_code == expected_response
        assert str(response.content) == right_condition

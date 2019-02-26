import pytest
from hamcrest import *
import requests
import os

liquid = "b'liquid'"
ice = "b'ice'"
steam = "b'steam'"
long_string_error = 'b\'{"error": "length of value must be at most 10"}\''
invalid_params = '{"error": "Invalid temperature'
not_allowed = '{"error": "Method Not Allowed"}'

"""
- Не верно реализованны возможности функции Range.
- Не верная обработка отрицательных значений, если не указан параметр шкалы.
- Некорректная обработка значений выше(ниже) граничных.
- Неправильные теги для шкал Kelvin и Celsius.
- Неверная обработка значений с длинной строки более 11. 
- Неверная обработка значений со знаком '+'.
- Неверная обработка десятичных значений .
- Неверная обработка значений в которых шкала с маленькой буквы.
- Неверная обработка метод POST HTTP протокола.
- Eсли в параметре передавать числовое значение без указания тега температурной шкалы, то по умолчанию API считает, что
запрос идет в градусах цельсия. 
- Сервер не работает со шкалой Fahrenheit.
- Неверная обработка значений начинающихся с 0.
- Неверная обработка значения None
- Для шкалы Celsius минимальное значение может быть -273,15, а используется -999999
- Для шкалы Fahrenheit минимальное значение может быть −459,67, а используется -9999
"""

# @pytest.fixture(scope="session", autouse=True)
# def setup_fixture():
#     host = os.environ.get('TEST_HOST', 'localhost:8888')
#     command = 'temperature_check'
#     url = 'http://{}/{}'.format(host, command)
#     return url


class TestServerFunctionality:
    def setup_class(self):
        self.host = os.environ.get('TEST_HOST', 'localhost:8888')
        self.command = 'temperature_check'
        self.url = 'http://{}/{}'.format(self.host, self.command)

    # Check negative and basic value

    def test_max_string(self):
        # Incorrect processing of values above the boundary
        response = requests.get(self.url, params={'temperature': '9999999999'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(steam))

    def test_eleven_signs(self, fahrenheit_temp, expected_response_code):
        response = requests.get(self.url, params={'temperature': fahrenheit_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(long_string_error))

    def test_twelve_signs(self):
        # Incorrect handling of values from a long string greater than 11
        response = requests.get(self.url, params={'temperature': '999999999999'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.content), equal_to(long_string_error))

    def test_bad_params(self):
        response = requests.get(self.url, params={'temperature': 'A'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_without_params(self):
        response = requests.get(self.url, params={'temperature': ''})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_with_spacebar_params(self):
        response = requests.get(self.url, params={'temperature': ' '})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_with_none_params(self):
        # Incorrect handling of None
        response = requests.get(self.url, params={'temperature': None})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_with_only_real_tag(self):
        response = requests.get(self.url, params={'temperature': 'F'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_with_plus_value(self):
        # Incorrect handling of values with the sign plus
        response = requests.get(self.url, params={'temperature': '+10'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_with_float_value(self):
        # Incorrect handling of float values float
        response = requests.get(self.url, params={'temperature': '10.5'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.text), contains_string(liquid))

    def test_with_small_letter(self):
        # Incorrect processing of values in which the scale with a small letter
        response = requests.get(self.url, params={'temperature': '10с'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_with_spacebar_between_params(self):
        response = requests.get(self.url, params={'temperature': '10 C'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_hard_symbol(self):
        # Incorrect character handling
        response = requests.get(self.url, params={'temperature': '«»‘~!@#$%^&*()?>,./\<][ /*<!—«»♣☺♂'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_sql(self):
        response = requests.get(self.url, params={'temperature': 'select*'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_xss(self):
        response = requests.get(self.url, params={'temperature': '<script>alert("XSS1")</script>'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_injections(self):
        response = requests.get(self.url, params={'temperature': 'DROP TABLE temperature'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_html_injections(self):
        response = requests.get(self.url, params={
            'temperature': '< form % 20 action =»http: // live.hh.ru» > < input % 20 type =»submit» > < / form >'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_starts_with_zero(self):
        # Incorrect handling of values starting with 0
        response = requests.get(self.url, params={'temperature': '010'})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_inverted_commas(self):
        response = requests.get(self.url, params={'temperature': ' \'10\' '})
        assert_that(response.status_code, equal_to(400))
        assert_that(str(response.text), contains_string(invalid_params))

    def test_put_requests(self):
        response = requests.put(self.url, params={'temperature': '10'})
        assert_that(response.status_code, equal_to(405))
        assert_that(str(response.text), equal_to(not_allowed))

    def test_post_requests(self):
        # Incorrect processing of methods supported by HTTP Protocol
        response = requests.post(self.url, params={'temperature': '10'})
        assert_that(response.status_code, equal_to(405))
        assert_that(str(response.text), equal_to(not_allowed))

    def test_delete_requests(self):
        response = requests.delete(self.url, params={'temperature': '10'})
        assert_that(response.status_code, equal_to(405))
        assert_that(str(response.text), equal_to(not_allowed))


class TestDefaultFunctionality:
    def setup_class(self):
        self.host = os.environ.get('TEST_HOST', 'localhost:8888')
        self.command = 'temperature_check'
        self.url = 'http://{}/{}'.format(self.host, self.command)

    # Check work with default value == Celsius

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('999999', 200, steam),   # Range function was not used correctly, max value is absent
                                 ('1000000', 200, steam),  # Incorrect processing of values above the boundary
                                 ('100', 200, steam)       # min steam - test correct
                             ])
    def test_default_steam_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), contains_string(condition))

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('99', 200, liquid),  # Range function was not used correctly, max value for liquid(99) is absent
                                 ('1', 200, liquid)    # min liquid - test correct
                             ])
    def test_default_liquid_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('0', 200, ice),        # Range function was not used correctly, max value for ice(0) is absent
                                 ('-999999', 200, ice),  # Incorrect handling of negative values
                                 ('-1000000', 200, ice)  # Incorrect handling of negative values
                             ])
    def test_default_ice_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': '0'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))


class TestKelvinFunctionality:
    def setup_class(self):
        self.host = os.environ.get('TEST_HOST', 'localhost:8888')
        self.command = 'temperature_check'
        self.url = 'http://{}/{}'.format(self.host, self.command)

    # We know that the tags for the Kelvin and Celsius scales are incorrect
    #  so we will check Kelvin that the boundary values work correctly with the wrong parameter C.

    def test_kelvin_max(self):
        # Range function was not used correctly, max value is absent
        response = requests.get(self.url, params={'temperature': '999C'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(steam))

    def test_kelvin_value_above_border(self):
        # Incorrect processing of values above the boundary
        response = requests.get(self.url, params={'temperature': '1000C'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(steam))

    def test_kelvin_steam_min(self):
        # Incorrect handling of float values float
        response = requests.get(self.url, params={'temperature': '373.15C'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(steam))

    def test_kelvin_check_steam_status_on_response(self):
        response = requests.get(self.url, params={'temperature': '374C'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(steam))

    def test_kelvin_max_liquid(self):
        # Incorrect handling of float values float
        response = requests.get(self.url, params={'temperature': '373.154C'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(liquid))

    def test_kelvin_liquid_min(self):
        # Incorrect handling of float values float
        response = requests.get(self.url, params={'temperature': '273.16C'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(liquid))

    def test_kelvin_check_liquid_status_on_response(self):
        response = requests.get(self.url, params={'temperature': '274C'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(liquid))

    def test_kelvin_max_ice(self):
        # Incorrect handling of float values float
        response = requests.get(self.url, params={'temperature': '273.15C'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))

    def test_kelvin_min_ice(self):
        response = requests.get(self.url, params={'temperature': '0C'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))

    def test_kelvin_value_below_border(self):
        # Incorrect processing of values above the boundary
        response = requests.get(self.url, params={'temperature': '-100C'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))


class TestCelsiusFunctionality:
    def setup_class(self):
        self.host = os.environ.get('TEST_HOST', 'localhost:8888')
        self.command = 'temperature_check'
        self.url = 'http://{}/{}'.format(self.host, self.command)

    # We know that the tags for the Kelvin and Celsius scales are incorrect
    #  so we will check Celsius that the boundary values work correctly with the wrong parameter K.

    def test_celsius_max(self):
        # Range function was not used correctly, max value is absent
        response = requests.get(self.url, params={'temperature': '999999K'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(steam))

    def test_celsius_value_above_border(self):
        # Incorrect processing of values above the boundary
        response = requests.get(self.url, params={'temperature': '1000000K'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(steam))

    def test_celsius_steam_min(self):
        response = requests.get(self.url, params={'temperature': '100K'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(steam))

    def test_celsius_max_liquid(self):
        # Range function was not used correctly, max value for liquid(99) is absent
        response = requests.get(self.url, params={'temperature': '99K'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(liquid))

    def test_celsius_liquid_min(self):
        response = requests.get(self.url, params={'temperature': '1K'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(liquid))

    def test_celsius_max_ice(self):
        # Range function was not used correctly, max value for ice(0) is absent
        response = requests.get(self.url, params={'temperature': '0K'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))

    def test_celsius_absolutely_zero_ice(self):
        # Incorrect handling of float values float
        response = requests.get(self.url, params={'temperature': '-273.15K'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))

    def test_celsius_min_ice(self):
        response = requests.get(self.url, params={'temperature': '-999999K'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))

    def test_celsius_value_below_border(self):
        # Incorrect handling of negative values
        response = requests.get(self.url, params={'temperature': '-1000000K'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))


class TestFahrenheitFunctionality:
    def setup_class(self):
        self.host = os.environ.get('TEST_HOST', 'localhost:8888')
        self.command = 'temperature_check'
        self.url = 'http://{}/{}'.format(self.host, self.command)

    # Check work Fahrenheit scale

    def test_fahrenheit_max(self):
        # Range function was not used correctly, max value is absent
        response = requests.get(self.url, params={'temperature': '9999F'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(steam))

    def test_fahrenheit_value_above_border(self):
        # Incorrect processing of values above the boundary
        response = requests.get(self.url, params={'temperature': '100000F'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(steam))

    def test_fahrenheit_steam_min(self):
        # The scale does not work completely
        response = requests.get(self.url, params={'temperature': '212F'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(steam))

    def test_fahrenheit_max_liquid(self):
        # The scale does not work completely
        response = requests.get(self.url, params={'temperature': '211F'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(liquid))

    def test_fahrenheit_liquid_min(self):
        # The scale does not work completely
        response = requests.get(self.url, params={'temperature': '33F'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(liquid))

    def test_fahrenheit_max_ice(self):
        # The scale does not work completely
        response = requests.get(self.url, params={'temperature': '32F'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))

    def test_fahrenheit_absolutely_zero_ice(self):
        # Incorrect handling of float values float
        response = requests.get(self.url, params={'temperature': '−459.67F'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))

    def test_fahrenheit_min_ice(self):
        # The scale does not work completely
        response = requests.get(self.url, params={'temperature': '-9999F'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))

    def test_fahrenheit_value_below_border(self):
        # The scale does not work completely
        response = requests.get(self.url, params={'temperature': '-1000000F'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(ice))

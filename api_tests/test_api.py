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
- Не верно реализованны возможности функции Range(есть выпавшие граничные значения).
- Не верная обработка отрицательных значений, если не указан параметр шкалы.
- Некорректная обработка значений выше(ниже) граничных. response = 200 and status = unknown
- Неправильные теги для шкал Kelvin и Celsius.
- Неверная обработка значений с длинной строки более 11. 
- Неверная обработка значений со знаком '+'.
- Неверная обработка десятичных значений.
- Неверно обрабатывает значение None.
- Неверная обработка значений в которых шкала с маленькой буквы.
- Неверная обработка метод POST HTTP протокола.
- Если в параметре передавать числовое значение без указания тега температурной шкалы, то по умолчанию API считает, что
запрос идет в градусах цельсия. 
- Сервер не работает со шкалой Fahrenheit.
- Неверная обработка значений начинающихся с 0.
- Неверная обработка значения None
- Для шкалы Celsius минимальное значение может быть -273,15, а используется -999999
- Для шкалы Fahrenheit минимальное значение может быть −459,67, а используется -9999
"""


class TestBaseClass:
    command = None
    url = None
    host = None

    def setup_method(self):
        self.host = os.environ.get('TEST_HOST', 'localhost:8888')
        self.command = 'temperature_check'
        self.url = 'http://{}/{}'.format(self.host, self.command)


class TestServerFunctionality(TestBaseClass):
    """
    Check negative and basic value
    """
    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('9999999999', 400, invalid_params),      # Incorrect processing of values above the boundary
                                 ('99999999999', 400, long_string_error),  # test 11 signs - correct
                                 ('999999999999', 400, long_string_error)  # Incorrect handling of values from a long string greater than 11
                             ])
    def test_string_length(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('A', 400, invalid_params),
                                 ('', 400, invalid_params),
                                 (' ', 400, invalid_params),
                                 (None, 400, invalid_params),       # Incorrect handling "None" values
                                 ('C', 400, invalid_params),
                                 ('+10', 400, invalid_params),      # Incorrect handling with sign + values
                                 ('10.5', 400, invalid_params),     # Incorrect handling float values
                                 ('10с', 400, invalid_params),      # Incorrect handling small letter values
                                 ('10 C', 400, invalid_params),
                                 ('«»‘~!@#$%^&*()?>,./\<][ /*<!—«»♣☺♂', 400, invalid_params),
                                 ('select*', 400, invalid_params),
                                 ('<script>alert("XSS1")</script>', 400, invalid_params),
                                 ('DROP TABLE temperature', 400, invalid_params),
                                 ('< form % 20 action =»http: // live.hh.ru» > < input % 20 type =»submit» > < / form >', 400, invalid_params),
                                 ('010', 400, invalid_params),      # Incorrect handling 0 values
                                 (' \'10\' ', 400, invalid_params)
                             ])
    def test_bad_params(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.text), contains_string(condition))

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


class TestDefaultFunctionality(TestBaseClass):
    """
    Check work with default value == Celsius
    """
    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('999999', 200, steam),            # Range function was not used correctly, max value is absent
                                 ('1000000', 400, invalid_params),  # Incorrect processing values above the boundary
                                 ('100', 200, steam)                # Min steam - test correct
                             ])
    def test_default_steam_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), contains_string(condition))

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('99', 200, liquid),               # Range function was not used correctly, max value for liquid(99) is absent
                                 ('1', 200, liquid)                 # Min liquid - test correct
                             ])
    def test_default_liquid_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('0', 200, ice),                   # Range function was not used correctly, max value for ice(0) is absent
                                 ('-999999', 200, ice),             # Incorrect handling negative values
                                 ('-1000000', 400, invalid_params)  # Incorrect handling negative values
                             ])
    def test_default_ice_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))


class TestKelvinFunctionality(TestBaseClass):
    """
    We know that the tags for the Kelvin and Celsius scales are incorrect
    so we will check Kelvin that the boundary values work correctly with the wrong parameter C.
    """
    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('999C', 200, steam),              # Range function was not used correctly, max value is absent
                                 ('1000C', 400, invalid_params),    # Incorrect processing values above the boundary
                                 ('373.15C', 200, steam),           # Incorrect handling float values
                                 ('374C', 200, steam)               # Response steam - test correct
                             ])
    def test_kelvin_steam_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('373.14C', 200, liquid),          # Incorrect handling float values
                                 ('273.16C', 200, liquid),          # Incorrect handling float values
                                 ('274C', 200, liquid)              # Response liquid - test correct
                             ])
    def test_kelvin_liquid_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('273.15C', 200, ice),             # Incorrect handling float values
                                 ('0C', 200, ice),                  # Absolute zero - test correct
                                 ('-1C', 400, invalid_params)       # Incorrect processing values above the boundary
                             ])
    def test_kelvin_ice_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))


class TestCelsiusFunctionality(TestBaseClass):
    """
    We know that the tags for the Kelvin and Celsius scales are incorrect
    so we will check Celsius that the boundary values work correctly with the wrong parameter K.
    """
    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('999999K', 200, steam),           # Range function was not used correctly, max value is absent
                                 ('1000000K', 400, invalid_params), # Incorrect processing values above the boundary
                                 ('100K', 200, steam)               # Response steam - test correct
                             ])
    def test_celsius_steam_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('99K', 200, liquid),              # Range function was not used correctly, max value for liquid(99) is absent
                                 ('1K', 200, liquid)                # Min liquid - test correct
                             ])
    def test_celsius_liquid_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('0K', 200, ice),                  # Range function was not used correctly, max value for ice(0) is absent
                                 ('-273.15K', 200, ice),            # Incorrect handling float values
                                 ('-999999K', 200, ice),            # Min ice - test correct
                                 ('-1000000K', 400, invalid_params) # Incorrect processing values above the boundary
                             ])
    def test_celsius_ice_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))


class TestFahrenheitFunctionality(TestBaseClass):
    """
    Check work Fahrenheit scale
    """
    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('9999F', 200, steam),             # Range function was not used correctly, max value is absent
                                 ('100000F', 400, invalid_params),  # Incorrect processing values above the boundary
                                 ('212F', 200, steam)               # The scale does not work completely
                             ])
    def test_fahrenheit_steam_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('211F', 200, liquid),             # The scale does not work completely
                                 ('33F', 200, liquid)               # The scale does not work completely
                             ])
    def test_fahrenheit_liquid_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': '211F'})
        assert_that(response.status_code, equal_to(200))
        assert_that(str(response.content), equal_to(liquid))

    @pytest.mark.parametrize("default_temp, expected_response_code, condition",
                             [
                                 ('32F', 200, ice),                 # The scale does not work completely
                                 ('−459.67F', 200, ice),            # Incorrect handling float values
                                 ('-9999F', 200, ice),              # The scale does not work completely
                                 ('-10000F', 400, invalid_params)   # The scale does not work completely
                             ])
    def test_fahrenheit_ice_value(self, default_temp, expected_response_code, condition):
        response = requests.get(self.url, params={'temperature': default_temp})
        assert_that(response.status_code, equal_to(expected_response_code))
        assert_that(str(response.content), equal_to(condition))

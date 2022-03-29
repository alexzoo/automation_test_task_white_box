import pytest
import requests

BASE_URL = 'http://localhost:8888/temperature_check'
STEAM = 'steam'
LIQUID = 'liquid'
ICE = 'ice'


class TestDefaultValue:

    @pytest.mark.parametrize('temperature', [-274, -273, 0, 1])
    def test_ice(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': temperature})
        assert r.status_code == 200
        assert r.text == ICE

    @pytest.mark.parametrize('temperature', [0, 99, 100])
    def test_liquid(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': temperature})
        assert r.status_code == 200
        assert r.text == LIQUID

    @pytest.mark.parametrize('temperature', [99, 100, 9999999, 1000000])
    def test_steam(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': temperature})
        assert r.status_code == 200
        assert r.text == STEAM


class TestCelsius:

    @pytest.mark.parametrize('temperature', [-274, -273, 0, 1])
    def test_ice(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': f'{temperature}K'})
        assert r.status_code == 200
        assert r.text == ICE

    @pytest.mark.parametrize('temperature', [0, 99, 100])
    def test_liquid(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': f'{temperature}K'})
        assert r.status_code == 200
        assert r.text == LIQUID

    @pytest.mark.parametrize('temperature', [99, 100, 9999999, 1000000])
    def test_steam(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': f'{temperature}K'})
        assert r.status_code == 200
        assert r.text == STEAM


class TestKelvin:

    @pytest.mark.parametrize('temperature', [-1, 0, 1, 273, 274])
    def test_ice(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': f'{temperature}C'})
        assert r.status_code == 200
        assert r.text == ICE

    @pytest.mark.parametrize('temperature', [273, 274, 275, 372, 373, 374])
    def test_liquid(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': f'{temperature}C'})
        assert r.status_code == 200
        assert r.text == LIQUID

    @pytest.mark.parametrize('temperature', [372, 373, 374, 998, 999, 1000])
    def test_steam(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': f'{temperature}C'})
        assert r.status_code == 200
        assert r.text == STEAM


class TestFahrenheit:

    @pytest.mark.parametrize('temperature', [-10000, -9999, -9998, 32, 33, 34])
    def test_ice(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': f'{temperature}F'})
        assert r.status_code == 200
        assert r.text == ICE

    @pytest.mark.parametrize('temperature', [32, 33, 34, 210, 211, 212])
    def test_liquid(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': f'{temperature}F'})
        assert r.status_code == 200
        assert r.text == LIQUID

    @pytest.mark.parametrize('temperature', [211, 212, 213, 9998, 9999, 10000])
    def test_steam(self, temperature):
        r = requests.get(BASE_URL, params={'temperature': f'{temperature}F'})
        assert r.status_code == 200
        assert r.text == STEAM


class TestServiceFunctionality:

    r = requests.post(BASE_URL, params={'temperature': 0})
    r2 = requests.delete(BASE_URL, params={'temperature': 0})



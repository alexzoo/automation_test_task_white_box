import requests

BASE_URL = 'http://localhost:8888/temperature_check?temperature='


class TestTemperature:

    def test_zero(self):
        r = requests.get(BASE_URL + str(0))
        assert r.status_code == 200
        assert r.text == 'unknown'

    def test_on_99(self):
        r = requests.get(BASE_URL + str(0))
        assert r.status_code == 200
        assert r.text == 'unknown'

    def test_on_1(self):
        r = requests.get(BASE_URL + str(1))
        assert r.status_code == 200
        assert r.text == 'liquid'

    def test_on_50(self):
        r = requests.get(BASE_URL + str(1))
        assert r.status_code == 200
        assert r.text == 'liquid'

    def test_on_100(self):
        r = requests.get(BASE_URL + str(100))
        assert r.status_code == 200
        assert r.text == 'steam'

    def test_on_150(self):
        r = requests.get(BASE_URL + str(100))
        assert r.status_code == 200
        assert r.text == 'steam'



import unittest
from ddns_domain_updater.public_ip_getter import GooglePublicIpGetter, PublicIPGetterError


class ResponseMock:
    def __init__(self, status_code: int, text: str):
        self._status_code = status_code
        self._text = text

    @property
    def text(self) -> str:
        return self._text

    @property
    def status_code(self) -> int:
        return self._status_code


class TestGooglePublicIpGetter(unittest.TestCase):
    def test_getter_uses_correct_address(self):
        def get(actual: str):
            expected = GooglePublicIpGetter.url
            self.assertEqual(expected, actual)
            return ResponseMock(status_code=200, text='whatever')

        pig = GooglePublicIpGetter(getter=get)
        pig.get_current_ip()

    def test_get_current_ip_raises_error_if_get_fails(self):
        pig = GooglePublicIpGetter(getter=lambda x: ResponseMock(status_code=400, text='whatever'))
        self.assertRaises(PublicIPGetterError, pig.get_current_ip)

    def test_get_current_ip_returns_getter_response_if_get_succeeds(self):
        get_response = 'whatever'
        pig = GooglePublicIpGetter(getter=lambda x: ResponseMock(status_code=200, text=get_response))
        resp = pig.get_current_ip()
        self.assertEqual(get_response, resp)

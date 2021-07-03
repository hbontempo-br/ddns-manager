import unittest
from ddns_manager.public_ip_getter import GooglePublicIpGetter, PublicIPGetterError


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
        def req(method: str, url: str):
            expected = GooglePublicIpGetter.base_url
            self.assertEqual("get", method)
            self.assertEqual(expected, url)
            return ResponseMock(status_code=200, text="whatever")

        pig = GooglePublicIpGetter(req=req)
        pig.get_current_ip()

    def test_get_current_ip_raises_error_if_get_fails(self):
        pig = GooglePublicIpGetter(
            req=lambda method, url: ResponseMock(status_code=400, text="whatever")
        )
        self.assertRaises(PublicIPGetterError, pig.get_current_ip)

    def test_get_current_ip_returns_getter_response_if_get_succeeds(self):
        get_response = "whatever"
        pig = GooglePublicIpGetter(
            req=lambda method, url: ResponseMock(status_code=200, text=get_response)
        )
        resp = pig.get_current_ip()
        self.assertEqual(get_response, resp)

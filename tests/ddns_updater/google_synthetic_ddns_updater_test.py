import unittest
from ddns_manager.ddns_updater import DDNSUpdaterError, GoogleSyntheticDDNSUpdater


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


class TestGoogleSyntheticDDNSUpdater(unittest.TestCase):
    def test_getter_uses_correct_address(self):
        ip = "1.2.3.4"
        hostname = "hott.name"
        username = "username"
        password = "password"

        def req(method: str, url: str, params: dict):
            expected_url = (
                f"https://{username}:{password}@{GoogleSyntheticDDNSUpdater.base_url}"
            )
            expectd_param = {"hostname": hostname, "myip": ip}
            self.assertEqual("post", method)
            self.assertEqual(expected_url, url)
            self.assertDictEqual(expectd_param, params)
            return ResponseMock(status_code=200, text="good")

        du = GoogleSyntheticDDNSUpdater(
            username=username, password=password, hostname=hostname, req=req
        )
        du.update_ddns_record(ip)

    def test_get_current_ip_raises_error_if_post_fails(self):
        invalid_status_code = 400
        du = GoogleSyntheticDDNSUpdater(
            username="username",
            password="password",
            hostname="hott.name",
            req=lambda method, url, params: ResponseMock(
                status_code=invalid_status_code, text="good"
            ),
        )

        self.assertRaises(DDNSUpdaterError, du.update_ddns_record, "1.2.3.4")

    def test_get_current_ip_raises_error_if_post_return_not_success(self):
        invalid_response = "whatever"
        du = GoogleSyntheticDDNSUpdater(
            username="username",
            password="password",
            hostname="hott.name",
            req=lambda method, url, params: ResponseMock(
                status_code=200, text=invalid_response
            ),
        )

        self.assertRaises(DDNSUpdaterError, du.update_ddns_record, "1.2.3.4")

    def test_get_current_ip_not_raises_error_if_post_succeeds(self):
        valid_response = "good"
        du = GoogleSyntheticDDNSUpdater(
            username="username",
            password="password",
            hostname="hott.name",
            req=lambda method, url, params: ResponseMock(
                status_code=200, text=valid_response
            ),
        )

        self.assertIsNone(du.update_ddns_record("1.2.3.4"))

        valid_response = "nochg"
        du = GoogleSyntheticDDNSUpdater(
            username="username",
            password="password",
            hostname="hott.name",
            req=lambda method, url, params: ResponseMock(
                status_code=200, text=valid_response
            ),
        )

        self.assertIsNone(du.update_ddns_record("1.2.3.4"))

import pytest
import requests
import allure
from endpoints.records_endpoints import Record


class BaseApiTest:

    @pytest.fixture(autouse=True)
    def setup_method(self, backend_url):
        with allure.step("Initialize test session and record endpoint"):
            self.session = requests.Session()
            self.record = Record()
            self.backend_url = backend_url

        yield

        with allure.step("Close session"):
            self.session.close()
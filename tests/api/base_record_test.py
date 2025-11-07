import pytest
import requests
import allure
from db_helper import DatabaseHelper
from endpoints.records_endpoints import Record
from conftest import COLLECTION_NAME


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

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self):
        with allure.step("Setup test class"):
            allure.attach(
                "Test suite initialized",
                name="Class Setup",
                attachment_type=allure.attachment_type.TEXT
            )
        yield
        with allure.step("Teardown test class"):
            allure.attach(
                "Test suite completed",
                name="Class Teardown",
                attachment_type=allure.attachment_type.TEXT
            )

    def create_test_record(self, payload):
        with allure.step(f"Create record with payload: {payload}"):
            record_id = self.record.create_record(payload, self.session, self.backend_url)
            allure.attach(
                str(record_id),
                name="Created Record ID",
                attachment_type=allure.attachment_type.TEXT
            )
            return record_id


    def verify_record_in_db(self, db_connection, record_id):
        with allure.step("Verify record exists in database"):
            db_helper = DatabaseHelper(db_connection, COLLECTION_NAME, self.backend_url)
            db_helper.verify_record_exists(record_id)
            allure.attach(
                str(record_id),
                name="Verified Record ID",
                attachment_type=allure.attachment_type.TEXT
            )

    def attach_response(self, name="Response"):
        with allure.step(f"Attach {name} to report"):
            allure.attach(
                str(self.record.response_json),
                name=name,
                attachment_type=allure.attachment_type.JSON
            )
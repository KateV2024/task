import pytest
import allure
from conftest import db_collection, backend_url, db_connection, COLLECTION_NAME
from db_helper import DatabaseHelper
from payload import valid_payload
from tests.api.base_record_test import BaseApiTest


@allure.epic("Records")
@allure.feature("Record Management API")
@allure.tag("api", "records", "positive")
@allure.link("Jira-101")
class TestRecordsPositive(BaseApiTest):

    @allure.story("Create record with valid input")
    @allure.description("This test covers the scenario when a record is created with valid input.")
    @allure.tag("POST")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_record_with_valid_input(self, db_connection, db_collection, backend_url):
        payload = valid_payload
        db = DatabaseHelper(db_connection, COLLECTION_NAME, backend_url)

        with allure.step("Create record with valid payload"):
            self.record.create_record(payload, self.session, self.backend_url)

        with allure.step("Verify response status code is 201"):
            self.record.check_status_code(201), "New record is created"

        with allure.step("Verify record exists in database"):
            record_id = self.record.get_record_id()
            db.return_record_details(record_id)

    @allure.story("Fetch all records")
    @allure.description("This test covers the scenario when user fetches all records.")
    @allure.tag("GET")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_all_records(self):
        with allure.step("Fetch all records"):
            self.record.get_records(self.session, self.backend_url)

        with allure.step("Verify response status code is 200"):
            self.record.check_status_code(200), "All created records are fetched"

    @allure.story("Delete record")
    @allure.description("This test covers the scenario when user deletes a record.")
    @allure.tag("DELETE")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_delete_record(self, db_connection, db_collection, backend_url):
        payload = valid_payload
        db = DatabaseHelper(db_connection, COLLECTION_NAME, backend_url)

        with allure.step("Create a new record to delete"):
            record_id = self.record.create_record(payload, self.session, self.backend_url)

        with allure.step("Delete the record"):
            self.record.delete_record(record_id, self.session, self.backend_url)

        with allure.step("Verify record deletion response is 200"):
            self.record.check_status_code(200), "Record is deleted"

        with allure.step("Verify record deletion response is 200"):
            db.check_record_is_deleted(record_id), "Record is not found in DB"
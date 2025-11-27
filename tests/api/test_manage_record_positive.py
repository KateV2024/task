import allure
from conftest import db_collection, backend_url, db_connection, COLLECTION_NAME
from db_helper import DatabaseHelper
from payload import valid_payload
from tests.api.base_session import BaseApiTest
from helpers.consts import Const, Feature, Tags, Epic


@allure.epic(Epic.RECORDS)
@allure.feature(Feature.RECORD_MANAGEMENT_API)
@allure.tag(Tags.API,
            Tags.POST,
            Tags.CREATE_RECORD,
            Tags.GET,
            Tags.GET_RECORD_DETAILS,
            Tags.DELETE,
            Tags.DELETE_RECORD,
            Tags.DATABASE,
            Tags.POSITIVE
            )
class TestRecordsPositive(BaseApiTest):

    @allure.story("Create record with valid input")
    @allure.description("This test covers the scenario when a record is created with valid input.")
    @allure.severity(Const.CRITICAL)
    def test_create_record_with_valid_input(self, db_connection,db_collection, backend_url):
        payload = valid_payload
        db = DatabaseHelper(db_connection, COLLECTION_NAME, backend_url)

        with allure.step("Create record with valid payload"):
            self.record.create_record(payload, self.session, self.backend_url)
            allure.attach(
                str(valid_payload),
                name="New Record is created via backend",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Verify response status code is 201"):
            self.record.verify_status_code(201), "New record is created"

        with allure.step("Get record details from database"):
            record_id = self.record.get_record_id()
            db.find_record_by_id(record_id)

    @allure.story("Fetch all records")
    @allure.description("This test covers the scenario when user fetches all records.")
    @allure.severity(Const.CRITICAL)
    def test_get_all_records(self):
        with allure.step("Fetch all records"):
            self.record.get_records(self.session, self.backend_url)

        with allure.step("Verify response status code is 200"):
            self.record.verify_status_code(200), "All created records are fetched"
            allure.attach(
                self.record.response.text,
                name="Get all records via API",
                attachment_type=allure.attachment_type.JSON
            )

    @allure.story("Delete record")
    @allure.description("This test covers the scenario when user deletes a record.")
    @allure.severity(Const.NORMAL)
    def test_delete_record(self, db_connection, db_collection, backend_url):
        payload = valid_payload
        db = DatabaseHelper(db_connection, COLLECTION_NAME, backend_url)

        with allure.step("Create a new record to delete and get the record id"):
            self.record.create_record(payload, self.session, self.backend_url)
            record_id = self.record.get_record_id()

        with allure.step("Delete the record"):
            self.record.delete_record(record_id, self.session, self.backend_url)
            self.record.verify_status_code(200), "Record is deleted"

        with allure.step("Verify record deletion in db"):
            db.verify_record_is_deleted(record_id), "Record is not found in DB"


import pytest
import requests
import allure
from db_helper import DatabaseHelper
from endpoints.records_endpoints import Record
from payload import valid_payload
from conftest import db_connection, backend_url, COLLECTION_NAME


@allure.feature("Test Records API")
@allure.story("Create record with invalid input")
@pytest.mark.parametrize("payload", [
    ({"title": '', "description": '56588'}),  # Empty title
    ({"title": '567', "description": ''}),    # Empty description
    ({"title": '', "description": ''}),       # Both fields empty
])

def test_create_record_with_invalid_input(backend_url, payload):
    session = requests.Session()
    new_record = Record()

    with allure.step("Attempt to create record with payload"):
        new_record.create_record(payload, session, backend_url)

    with allure.step("Verify response status code is 400"):
        new_record.check_response_is_400(), "Failed to create record"


@allure.feature("Test Records API")
@allure.story("Create record with valid input")
def test_create_record_with_valid_input(backend_url, db_connection):
    session = requests.Session()
    new_record = Record()
    payload = valid_payload

    with allure.step("Create record with payload"):
        new_record.create_record(payload, session, backend_url)

    with allure.step("Verify response status code is 201"):
        new_record.check_response_is_201(), "New record is created"

    with allure.step("Verify record exists in database"):
        db_helper = DatabaseHelper(db_connection, COLLECTION_NAME, backend_url)
        record_id = new_record.get_record_id()
        db_helper.verify_record_exists(record_id)
        allure.attach(str(record_id), name="Record ID", attachment_type=allure.attachment_type.TEXT)


@allure.feature("Test Records API")
@allure.story("Get all records")
def test_get_all_records(backend_url):
    session = requests.Session()
    new_record = Record()

    with allure.step("Fetch all records"):
        new_record.get_records(session, backend_url)

    with allure.step("Verify response status code is 200"):
        assert new_record.check_response_is_200(), "All created records are fetched"

    with allure.step("Attach response body to report"):
        allure.attach(str(new_record.response_json), name="All Records", attachment_type=allure.attachment_type.JSON)


@allure.feature("Test Records API")
@allure.story("Delete a record")
def test_delete_record(backend_url):
    session = requests.Session()
    new_record = Record()
    payload = valid_payload

    with allure.step("Create a new record to delete"):
        record_id = new_record.create_record(payload, session, backend_url)

    with allure.step("Delete the record"):
        new_record.delete_record(session, backend_url, record_id)

    with allure.step("Verify record deletion response is 200"):
        assert new_record.check_response_is_200(), "Record is deleted"

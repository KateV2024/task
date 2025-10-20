from pages.home_page import HomePage
from pages.records_page import RecordsPage
from conftest import COLLECTION_NAME
from payload import int_payload
from db_helper import DatabaseHelper
from endpoints.records_endpoints import Record
import allure
import pytest
import requests


@allure.title("Full Record Lifecycle: UI + API + DB Verification")
@allure.description("This test covers the full lifecycle of a record: create via API, verify via UI, and delete with DB validation.")
@pytest.mark.smoke
def test_full_record_cycle(browser_context, base_url, db_connection, db_collection, backend_url):
    page = browser_context
    session = requests.Session()
    home = HomePage(page, base_url)
    record = RecordsPage(page, base_url)
    db_helper = DatabaseHelper(db_connection, COLLECTION_NAME, backend_url)
    title = int_payload.get("title")
    description = int_payload.get("description")

    with allure.step("Open Home page and navigate to Records"):
        home.open_url(base_url)
        home.get_home_page()
        home.click_go_to_records()
        record.check_user_is_on_records_list()

    with allure.step("Create a new record via API"):
        new_record = Record()
        record_id = new_record.create_record(int_payload, session, backend_url)  # Create a record via API
        allure.attach(
            str(int_payload),
            name="New Record",
            attachment_type=allure.attachment_type.JSON
        )
        new_record.check_response_is_201(), "New record is created"

    with allure.step("Verify new record appears in the UI table"):
        page.reload()
        record.check_user_is_on_records_list()
        assert record.check_new_title_in_table(title)
        assert record.check_new_desc_in_table(description)

    with allure.step("Delete the record via UI and validate in DB"):
        record.click_delete_record(title)
        deleted_db_record = db_helper.verify_record_exists(record_id)
        allure.attach(
            "Record is not found in DB",
            name="Record is deleted",
            attachment_type=allure.attachment_type.TEXT
        )
        assert deleted_db_record is None, "Record is deleted from DB"
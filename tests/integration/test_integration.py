from pages.home_page import HomePage
from pages.records_page import RecordsPage
from conftest import COLLECTION_NAME
from payload import valid_payload
from db_helper import DatabaseHelper
from endpoints.records_endpoints import Record
from settings import Timeout
import allure
import pytest
import requests


@allure.epic("Records")
@allure.feature("Record Management with API, UI, DB check ")
@allure.tag("api", "ui", "db", "records", "positive")
@allure.link("Jira-121")
@allure.story("Create Record via API, Verify and Delete via UI, Validate in DB")
@allure.description("This test covers the full lifecycle of a record: create via API, verify and delete via UI, check in db.")
@allure.tag("integration")
@allure.severity(allure.severity_level.CRITICAL)
def test_full_record_cycle(browser_context, base_url, db_connection, backend_url):
    page = browser_context
    session = requests.Session()
    home = HomePage(page, base_url)
    record = RecordsPage(page, base_url)
    db_helper = DatabaseHelper(db_connection, COLLECTION_NAME, backend_url)

    with allure.step("Create a new record via API"):
        new_record = Record()
        record_id = new_record.create_record(valid_payload, session, backend_url)  # Create a record via API
        new_record.check_status_code(201), "New record is created"
        allure.attach(
            str(valid_payload),
            name="New Record is created via API",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("User opens Home page and navigates to Records"):
        home.open_url(base_url)
        home.click_go_to_records()

    with allure.step("User verifies a new record appears in the UI table"):
        page.reload()
        record.check_new_record_btn()
        our_title = valid_payload["title"]
        our_desc = valid_payload["description"]
        record.check_new_title_in_table(our_title)
        record.check_new_desc_in_table(our_desc)
        allure.attach(
            str(valid_payload),
            name="New Record is displayed on UI",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("User deletes the record via UI and check record is deleted from DB"):
        record.click_delete_record(our_desc)
        record.check_record_is_deleted(our_title)
        allure.attach(
            "Record is deleted from DB",
            name="Record is deleted",
            attachment_type=allure.attachment_type.TEXT
        )
        db_helper.check_record_is_deleted(record_id)

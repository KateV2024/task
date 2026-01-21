from pages.home_page import HomePage
from pages.records_page import RecordsPage
from conftest import COLLECTION_NAME
from payload import valid_payload
from db_helper import DatabaseHelper
from endpoints.records_endpoints import Record
from helpers.consts import Const, Feature, Tags, Epic
import allure
import requests


@allure.epic(Epic.RECORDS)
@allure.feature(Feature.RECORD_MANAGEMENT_INTEGRATION)
@allure.tag(Tags.API,
            Tags.UI,
            Tags.POST,
            Tags.CREATE_RECORD,
            Tags.GET_RECORD_DETAILS,
            Tags.DELETE_RECORD,
            Tags.DATABASE,
            Tags.INTEGRATION,
            Tags.POSITIVE
            )

class TestFullIntegrationRecordLifeCycle:

    @allure.story("Create Record via API, Verify and Delete via UI, Validate in DB")
    @allure.description("Test full record lifecycle: create via API, verify, delete via UI, check in db.")
    @allure.severity(Const.CRITICAL)
    def test_full_record_cycle(self, browser_context, base_url, db_connection, backend_url):
        page = browser_context
        session = requests.Session()
        home = HomePage(page, base_url)
        record = RecordsPage(page, base_url)
        db_helper = DatabaseHelper(db_connection, COLLECTION_NAME, backend_url)

        with allure.step("Create a new record via API"):
            new_record = Record()
            new_record.create_record(valid_payload, session, backend_url)  # Create a record via API
            record_id = new_record.get_record_id()
            new_record.verify_status_code(201), "New record is created"
            allure.attach(
                str(valid_payload),
                name="New Record is created via API",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("User opens Home page and navigates to Records"):
            home.open_page()
            home.click_go_to_records()

        with allure.step("User verifies a new record appears in the UI table"):
            page.reload()
            record.get_new_record_btn()
            our_title = valid_payload["title"]
            our_desc = valid_payload["description"]
            record.get_new_title_in_table(our_title)
            record.get_new_desc_in_table(our_desc)
            allure.attach(
                str(valid_payload),
                name="New Record is displayed on UI",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("User deletes the record via UI and check record is deleted from DB"):
            record.delete_record_by_title(our_title)
            record.verify_record_is_deleted(our_title)
            allure.attach(
                str(valid_payload),
                name="Record is deleted",
                attachment_type=allure.attachment_type.TEXT
            )
            db_helper.verify_record_is_deleted(record_id)

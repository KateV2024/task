import allure
from pages.home_page import HomePage
from pages.records_page import RecordsPage
from payload import valid_payload


@allure.epic("Records")
@allure.feature("Records Management via UI")
@allure.tag("ui", "records", "positive", "new record")
@allure.link("Jira-112")
@allure.feature("Records")
@allure.story("User creates a new record, verifies it and deletes it")
class TestFullRecordLifecycle:

    @allure.story("User creates, verifies and deletes a newly added record")
    @allure.description("This test covers the scenario when user creates, verifies and deletes a newly added record")
    @allure.tag("create record", "verify record", "delete record", "verify deletion")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_record_full_lifecycle(self, browser_context, base_url, locale):
        # Do not use class and methods from tests
        page = browser_context
        home = HomePage(page, base_url)
        record = RecordsPage(page, base_url)

        with allure.step("Go to Records page"):
            home.open_page()
            home.click_go_to_records()

        with allure.step("Verify user is on Records list page and sees a 'Add new record' button"):
            record.check_new_record_btn()

        with allure.step("User creates a new record"):
            record.create_new_record(valid_payload["title"], valid_payload["description"])

        with allure.step("Verify new record is added"):
            record.check_new_title_in_table(valid_payload["title"])
            record.check_new_desc_in_table(valid_payload["description"])

        with allure.step("User deletes the newly added record"):
            record.click_delete_record(valid_payload["title"])

        with allure.step("User verifies the record is deleted"):
            record.check_record_is_deleted(valid_payload["title"])

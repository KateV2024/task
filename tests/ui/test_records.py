import allure
from pages.home_page import HomePage
from pages.records_page import RecordsPage
from payload import new_payload


@allure.feature("Operations with Records")
@allure.story("User creates, verifies and deletes a newly added record")
def test_user_deletes_new_record(browser_context, base_url, locale):
    page = browser_context
    home = HomePage(page, base_url)
    record = RecordsPage(page, base_url)
    new_title = new_payload.get("title")
    new_description = new_payload.get("description")

    with allure.step("Open Home page"):
        home.open_url(base_url)

    with allure.step("Verify user is on Home page"):
        home.get_home_page()

    with allure.step("Go to Records page"):
        home.click_go_to_records()

    with allure.step("Verify user is on Records list page"):
        record.check_user_is_on_records_list()

    with allure.step("Add a new record"):
        record.click_add_new_record()
        record.go_to_new_record_title()
        record.enter_new_record_title(new_title)
        record.go_to_new_record_description()
        record.enter_new_record_description(new_description)
        record.click_save_record()

    with allure.step("Verify new record is added"):
        record.check_new_title_in_table(new_title)
        record.check_new_desc_in_table(new_description)

    with allure.step("Delete the newly added record"):
        record.click_delete_record(new_title)
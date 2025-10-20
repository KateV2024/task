import allure
from pages.home_page import HomePage


@allure.feature("Navigation")
@allure.story("User navigates to Records page from Home page")
def test_user_moves_to_records_page(browser_context, base_url, locale):
    page = browser_context
    home = HomePage(page, base_url)

    with allure.step("Open Home page"):
        home.open_url(base_url)

    with allure.step("Verify user is on Home page"):
        home.get_home_page()

    with allure.step("Check 'Go to Records' button exists"):
        home.check_go_to_records_btn_exist()

    with allure.step("Click 'Go to Records' button"):
        home.click_go_to_records()


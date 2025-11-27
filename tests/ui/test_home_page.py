import allure
from pages.home_page import HomePage


@allure.epic("Records")
@allure.feature("Records Management via UI")
@allure.tag("ui", "records", "positive")
@allure.link("Jira-111")
@allure.feature("Navigation")
@allure.story("User navigates to Records page from Home page")
class TestNavigationToRecordsPage:

    @allure.story("Navigation to Record Page")
    @allure.description("This test covers the scenario when user navigates to Records page from Home page")
    @allure.tag("home page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_moves_to_records_page(self, browser_context, base_url, locale):
        page = browser_context
        home = HomePage(page, base_url)

        with allure.step("User opens Home page"):
            home.open_page()

        with allure.step("User clicks 'Go to Records' button"):
            home.click_go_to_records()

        with allure.step("Verify user is on page with records"):
            assert "records" in page.url, "User is not on Records page"

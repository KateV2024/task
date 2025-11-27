import allure
from pages.home_page import HomePage
from helpers.consts import Const, Feature, Tags, Epic


@allure.epic(Epic.RECORDS)
@allure.feature(Feature.RECORD_MANAGEMENT_UI)
@allure.tag(Tags.UI,
            Tags.POSITIVE,
            Tags.HOME_PAGE
            )

class TestNavigationToRecordsPage:

    @allure.story("Navigation to Record Page")
    @allure.description("This test covers the scenario when user navigates to Records page from Home page")
    @allure.severity(Const.BLOCKER)
    def test_user_moves_to_records_page(self, browser_context, base_url, locale):
        page = browser_context
        home = HomePage(page, base_url)

        with allure.step("User opens Home page"):
            home.open_page()

        with allure.step("User clicks 'Go to Records' button"):
            home.click_go_to_records()

        with allure.step("Verify user is on page with records"):
            assert "records" in page.url, "User is not on Records page"

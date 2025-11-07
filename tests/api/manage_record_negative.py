import pytest
import allure
from tests.api.base_record_test import BaseApiTest


@allure.epic("Records")
@allure.feature("Record Management API")
@allure.tag("api", "records", "negative")
@allure.link("Jira-101")
class TestRecordsNegative(BaseApiTest):

    @pytest.mark.parametrize("invalid_payload", [
        ({"title": '', "description": '56588'}),  # Empty title
        ({"title": '567', "description": ''}),    # Empty description
        ({"title": '', "description": ''}),       # Both fields empty
])

    @allure.story("Create record with invalid input")
    @allure.description("This test covers the scenario when a record should not be created with invalid input.")
    @allure.tag("POST")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_create_record_with_invalid_input(self, invalid_payload):
        payload = invalid_payload

        with allure.step("Attempt to create record with payload"):
            self.record.create_record(payload, self.session, self.backend_url)

        with allure.step("Verify response status code is 400"):
            self.record.check_status_code(400), "Failed to create record"

        # assert self.response.status_code == 400, "Failed to create record"
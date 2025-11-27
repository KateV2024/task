import pytest
import allure
from tests.api.base_session import BaseApiTest
from helpers.consts import Const, Feature, Tags, Epic


@allure.epic(Epic.RECORDS)
@allure.feature(Feature.RECORD_MANAGEMENT_API)
@allure.tag(Tags.API,
            Tags.POST,
            Tags.CREATE_RECORD,
            Tags.NEGATIVE
            )
class TestRecordsNegative(BaseApiTest):

    @pytest.mark.parametrize("invalid_payload", [
        ({"title": '', "description": '56588'}),  # Empty title
        ({"title": '567', "description": ''}),    # Empty description
        ({"title": '', "description": ''}),       # Both fields empty
])

    @allure.story("Create record with invalid input")
    @allure.description("This test covers the scenario when a record should not be created with invalid input.")
    @allure.severity(Const.NORMAL)
    def test_create_record_with_invalid_input(self, invalid_payload):
        payload = invalid_payload

        with allure.step("Attempt to create record with payload"):
            self.record.create_record(payload, self.session, self.backend_url)
            self.record.verify_status_code(400)
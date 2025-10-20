from pages.base_page import BasePage
from playwright.sync_api import expect


class RecordsPage(BasePage):
    RECORDS_LIST_HEADING = "heading"
    RECORDS_LIST_TEXT = "Record List"
    NEW_RECORD_BUTTON = "button"
    NEW_RECORD_TEXT = "Add Record"
    NEW_TITLE_FIELD = "textbox"
    NEW_TITLE_INPUT = "Title"
    NEW_DESC_FIELD = "textbox"
    NEW_DESC_INPUT = "Description"
    SAVE_BUTTON = "button"
    SAVE_TEXT = "Save"
    DELETE_BUTTON = "button"
    DELETE_TEXT = "Delete"


    def check_user_is_on_records_list(self):
        expect(self.page.get_by_role(self.RECORDS_LIST_HEADING, name = self.RECORDS_LIST_TEXT)).to_be_visible()

    def check_new_record_btn(self):
        return self.get_by_role(self.NEW_RECORD_BUTTON, name = self.NEW_RECORD_TEXT)

    def click_add_new_record(self):
        self.check_new_record_btn().click()

    def go_to_new_record_title(self):
        self.get_by_role(self.NEW_TITLE_FIELD, name = self.NEW_TITLE_INPUT).click()

    def enter_new_record_title(self, title):
        return self.get_by_role(self.NEW_TITLE_FIELD, name = self.NEW_TITLE_INPUT).fill(title)

    def go_to_new_record_description(self):
        self.get_by_role(self.NEW_DESC_FIELD, name=self.NEW_DESC_INPUT).click()

    def enter_new_record_description(self, description):
        return self.get_by_role(self.NEW_DESC_FIELD, name=self.NEW_DESC_INPUT).fill(description)

    def click_save_record(self):
        self.get_by_role(self.SAVE_BUTTON, name=self.SAVE_TEXT).click()

    def _row_by_exact_text(self, text):
        table = self.page.get_by_role("table")
        cell = table.get_by_role("cell", name=text, exact=True).first
        row = cell.locator("xpath=ancestor::tr[1]")
        return row

    def check_new_title_in_table(self, title):
        row = self._row_by_exact_text(title)
        expect(row).to_be_visible(timeout=10000)
        return True

    def check_new_desc_in_table(self, description):
        row = self._row_by_exact_text(description)
        expect(row).to_be_visible(timeout=10000)
        return True

    def click_delete_record(self, title):
        row = self._row_by_exact_text(title)
        row.get_by_role(self.DELETE_BUTTON, name=self.DELETE_TEXT).click()


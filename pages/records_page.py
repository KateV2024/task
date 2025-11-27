from pages.base_page import BasePage
from playwright.sync_api import expect
from pages.locators.locators_records_page import RecordsPageConstants as r_const
from settings import Timeout


class RecordsPage(BasePage):

    def check_new_record_btn(self):
        new_record_btn = self.get_by_role(r_const.NEW_RECORD_BUTTON, name = r_const.NEW_RECORD_TEXT)
        new_record_btn.wait_for(state="visible", timeout=Timeout.Medium)
        return new_record_btn

    def click_add_new_record(self):
        self.page.wait_for_timeout(Timeout.Medium)
        self.check_new_record_btn().click()

    def click_new_record_title_field(self):
        self.get_by_role(r_const.NEW_TITLE_FIELD, name = r_const.NEW_TITLE_INPUT).click()

    def enter_new_record_title(self, title):
        return self.get_by_role(r_const.NEW_TITLE_FIELD, name = r_const.NEW_TITLE_INPUT).fill(title)

    def click_new_record_description_field(self):
        self.get_by_role(r_const.NEW_DESC_FIELD, name=r_const.NEW_DESC_INPUT).click()

    def enter_new_record_description(self, description):
        return self.get_by_role(r_const.NEW_DESC_FIELD, name=r_const.NEW_DESC_INPUT).fill(description)

    def click_save_record(self):
        self.get_by_role(r_const.SAVE_BUTTON, name=r_const.SAVE_TEXT).click()

    def create_new_record(self, title, description):
         self.click_add_new_record()
         self.click_new_record_title_field()
         self.enter_new_record_title(title)
         self.click_new_record_description_field()
         self.enter_new_record_description(description)
         self.click_save_record()

    def check_new_title_in_table(self, title):
        row = self._row_by_exact_text(title)
        expect(row).to_be_visible(timeout=Timeout.Long)
        return row

    def check_new_desc_in_table(self, description):
        row = self._row_by_exact_text(description)
        expect(row).to_be_visible(timeout=Timeout.Long)
        return row

    def click_delete_record(self, title):
        row = self._row_by_exact_text(title)
        row.get_by_role(r_const.DELETE_BUTTON, name=r_const.DELETE_TEXT).click()

    def check_record_is_deleted(self, title):
        row = self._row_by_exact_text(title)
        expect(row).not_to_be_visible(timeout=Timeout.Long)

    # Do not forget that private methods are at the end or the beginning of the class
    def _row_by_exact_text(self, text):
        table = self.page.get_by_role(r_const.TABLE_ROLE)
        cell = table.get_by_role(r_const.CELL_ROLE, name=text, exact=True).first
        row = cell.locator(r_const.ROW_XPATH)
        return row


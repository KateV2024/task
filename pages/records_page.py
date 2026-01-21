from pages.base_page import BasePage
from playwright.sync_api import expect
from pages.locators.locators_records_page import RecordsPageConstants as r_const
from pages.locators.base_locators import ButtonLocators as btn
from pages.locators.base_locators import TextLocators as tb
from pages.locators.locators_records_page import TableLocators as tbl
from settings import Timeout


class RecordsPage(BasePage):

    def get_new_record_btn(self):
        new_record_btn = self.get_by_role(btn.BUTTON, name=r_const.NEW_RECORD_TEXT)
        new_record_btn.wait_for(state="visible")
        return new_record_btn

    def click_add_new_record(self):
        self.get_new_record_btn().click()

    def click_new_record_title_field(self):
        self.get_by_role(tb.TEXTBOX, name = r_const.NEW_TITLE_INPUT).click()

    def enter_new_record_title(self, title):
        return self.get_by_role(tb.TEXTBOX, name = r_const.NEW_TITLE_INPUT).fill(title)

    def click_new_record_description_field(self):
        self.get_by_role(tb.TEXTBOX, name=r_const.NEW_DESC_INPUT).click()

    def enter_new_record_description(self, description):
        return self.get_by_role(tb.TEXTBOX, name=r_const.NEW_DESC_INPUT).fill(description)

    def click_save_record(self):
        self.get_by_role(btn.BUTTON, name=r_const.SAVE_TEXT).click()

    def create_new_record(self, title, description):
        self.click_add_new_record()
        self.click_new_record_title_field()
        self.enter_new_record_title(title)
        self.click_new_record_description_field()
        self.enter_new_record_description(description)
        self.click_save_record()

    def get_row_by_text(self, text, field_type="title"):
        try:
            row = self._row_by_exact_text(text)
            expect(row).to_be_visible(timeout=Timeout.Long)
            return row
        except Exception as e:
            raise AssertionError(f"Row with {field_type} '{text}' not found: {str(e)}")

    def get_new_title_in_table(self, title):
         return self.get_row_by_text(title, field_type="title")

    def get_new_desc_in_table(self, description):
        return self.get_row_by_text(description, field_type="description")

    def _row_by_exact_text(self, text):
        table = self.page.get_by_role(tbl.TABLE)
        cell = table.get_by_role(tbl.CELL, name=text, exact=True).first
        row = cell.locator(tbl.ROW)
        return row

    def delete_record_by_title(self, text):
        row = self._row_by_exact_text(text)
        delete_btn = row.get_by_role(btn.BUTTON, name=r_const.DELETE_TEXT)
        delete_btn.click()

    def verify_record_is_deleted(self, title):
        try:
            row = self._row_by_exact_text(title)
            expect(row).not_to_be_visible(timeout=Timeout.Long)
        except AssertionError:
            pass
        except Exception as e:
            raise Exception(f"Failed to verify deletion of record '{title}': {str(e)}")


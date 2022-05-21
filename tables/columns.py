from typing import List

from django.template.loader import render_to_string

from tables.buttons import Button
from tables.rows import Row, LendingRow


class Column:
    @staticmethod
    def get_header():
        return ""

    def render(self, row: Row, perms=None):
        return ""


class BookCodeColumn(Column):
    @staticmethod
    def get_header():
        return "Book Code"

    def render(self, row: Row, perms=None):
        return row.get_item().book_code + " " + row.get_item().book_code_extension


class RecodeColumn(Column):
    @staticmethod
    def get_header():
        return ""

    def render(self, row: Row, perms=None):
        recode = row.get_item().get_recode()

        if recode:
            extension = recode.book_code_extension or ""
            if extension:
                extension = "(" + extension + ")"
            return "Recode to: " + recode.book_code + extension
        else:
            return ""


class TitleColumn(Column):
    @staticmethod
    def get_header():
        return "Title"

    def render(self, row: Row, perms=None):
        return render_to_string("columns/title_column.html", {"item": row.get_item()})


class AllAuthorsColumn(Column):
    @staticmethod
    def get_header():
        return "Authors"

    def render(self, row: Row, perms=None):
        strstr = ""
        for author in row.get_item().publication.get_authors():
            strstr += render_to_string("creator_single_line_description.html", {"author": author}) + "<br>"
        return strstr


class LentByColumn(Column):
    @staticmethod
    def get_header():
        return "Member"

    def render(self, row: LendingRow, perms=None):
        return render_to_string("columns/member_column.html", {"member": row.lending.member})


class HandinDate(Column):
    @staticmethod
    def get_header():
        return "Handin Date"

    def render(self, row: LendingRow, perms=None):
        return render_to_string("columns/handin_date.html", {"lending": row.lending})


class FineColumn(Column):
    @staticmethod
    def get_header():
        return "Fine"

    def render(self, row: LendingRow, perms=None):
        return render_to_string("columns/fine_column.html", {"lending": row.lending})


class ButtonsColumn(Column):
    def __init__(self, buttons: List[Button], title: str):
        self.buttons = buttons
        self.title = title

    def get_header(self):
        return self.title

    def render(self, row: LendingRow, perms=None):
        strstr = ""
        for button in self.buttons:
            strstr += button.render(row, perms)
        return strstr

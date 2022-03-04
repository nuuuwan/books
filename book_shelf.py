from _constants import UNKNOWN_SHELF_ROW
from DEWEY_TO_SHELF_ROW import DEWEY_TO_SHELF_ROW


def get_shelf_row(book):
    for dewey_n, shelf_row in DEWEY_TO_SHELF_ROW.items():
        n = len(dewey_n)
        if dewey_n == book.dewey_n(n):
            return shelf_row
    return UNKNOWN_SHELF_ROW

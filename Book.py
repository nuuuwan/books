from _constants import UNKNOWN_DEWEY, UNKNOWN_SHELF_ROW
from DEWEY_TO_SHELF_ROW import DEWEY_TO_SHELF_ROW


def normalize_dewey(raw_dewey):
    raw_dewey = raw_dewey.replace("/", "").strip()
    try:
        dewey_f = 1000 * (float)(raw_dewey)
        return '%03d.%03d' % (dewey_f / 1000, dewey_f % 1000)
    except ValueError:
        return UNKNOWN_DEWEY


class Book:
    def __init__(self, dewey, author, title, isbn):
        self.dewey = normalize_dewey(dewey)
        self.author = author
        self.title = title
        self.isbn = isbn

    def dewey_n(self, n):
        return self.dewey[:n]

    @property
    def author_in_ref_order(self):
        *first_names, last_name = self.author.split(' ')
        return last_name.upper() + ', ' + ' '.join(first_names)

    @property
    def shelf_row(self):
        for dewey_n, shelf_row in DEWEY_TO_SHELF_ROW.items():
            n = len(dewey_n)
            if dewey_n == self.dewey_n(n):
                return shelf_row

        return UNKNOWN_SHELF_ROW

    @property
    def sort_key(self):
        return (
            self.shelf_row +
            self.dewey +
            self.author_in_ref_order +
            self.title)

    @property
    def dewey_norm(self):
        return f'{self.dewey[:3]}.{self.dewey[3:]}'

    @staticmethod
    def buildFromCLZDatum(d):
        return Book(
            d['Dewey'],
            d['Author'],
            d['Title'],
            d['ISBN'],
        )

    def __str__(self):
        return f'{self.dewey_norm} [{self.author_in_ref_order}] {self.title}'

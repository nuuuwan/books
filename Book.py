from _constants import UNKNOWN_DEWEY


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

    @property
    def author_in_ref_order(self):
        *first_names, last_name = self.author.split(' ')
        return last_name.upper() + ', ' + ' '.join(first_names)

    @property
    def sort_key(self):
        return (
            self.dewey +
            self.author_in_ref_order +
            self.title)

    @property
    def dewey_int_str(self):
        return self.dewey[:3] + self.dewey[4:]

    def dewey_n(self, n):
        return self.dewey_int_str[:n]

    @staticmethod
    def buildFromCLZDatum(d):
        return Book(
            d['Dewey'],
            d['Author'],
            d['Title'],
            d['ISBN'],
        )

    def __str__(self):
        return f'{self.dewey} [{self.author_in_ref_order}] {self.title}'

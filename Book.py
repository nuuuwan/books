from _constants import UNKNOWN_DEWEY

DELIM_AUTHOR_LIST = '|'
DELIM_AUTHOR_LIST_WITH_SPACES = ' | '


def normalize_dewey(raw_dewey):
    raw_dewey = raw_dewey.replace("/", "").strip()
    try:
        dewey_f = 1000 * (float)(raw_dewey)
        return '%03d.%03d' % (dewey_f / 1000, dewey_f % 1000)
    except ValueError:
        return UNKNOWN_DEWEY


class Book:
    def __init__(self, dewey, author_list, title, isbn):
        self.dewey = normalize_dewey(dewey)
        self.author_list = author_list
        self.title = title
        self.isbn = isbn


    @property
    def author_in_ref_order_list(self):
        author_in_ref_order_list = []
        for author in self.author_list:
            *first_names, last_name = author.split(' ')
            author_in_ref_order = (
                last_name.upper() + ', ' + ' '.join(first_names))
            author_in_ref_order_list.append(author_in_ref_order)
        return author_in_ref_order_list

    @property
    def authors_in_ref_order(self):
        return DELIM_AUTHOR_LIST_WITH_SPACES.join(self.author_in_ref_order_list)
    

    @property
    def sort_key(self):
        return (
            self.dewey +
            self.authors_in_ref_order +
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
            list(map(
                lambda author: author.strip(),
                d['Author'].split(DELIM_AUTHOR_LIST),
            )),
            d['Title'],
            d['ISBN'],
        )

    def __str__(self):
        return f'{self.dewey} [{self.authors_in_ref_order}] {self.title}'

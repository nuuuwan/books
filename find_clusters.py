import os

from utils import tsv

N_SHELF_ROWS = 18
BOOK_DATA_FILE = os.path.join(
    '/Users/nuwan.senaratna/Dropbox',
    '_BOOKS',
    'NUWANS_BOOKS.clz.csv',
)

DEWEY1_TO_ROWS = {
    # shelf 1
    '0xx': 2,
    '1xx': 2,
    # shelf 2
    '2xx': 1,
    '3xx': 3,
    '4xx': 1,
    # shelf 3
    '5xx': 1,
    '6xx': 1,
    '7xx': 3,
    # shelf 3
    '8xx': 4,
    '9xx': 1,
}


def parse_dewey(s):
    s = s.replace('/', '')
    try:
        return '%06d' % ((float)(s) * 1000)
    except Exception:
        return '000000'


def get_book_list():
    return sorted(list(map(
        lambda d: dict(dewey=parse_dewey(d['Dewey'])),
        tsv.read(BOOK_DATA_FILE, delimiter=','),
    )), key=lambda d: d['dewey'])


def get_dewey1_to_rows():
    book_list = get_book_list()

    n = len(book_list)
    dewey_to_n = {}
    for d in book_list:
        dewey = d['dewey']
        dewey = dewey[:1] + 'xx'
        dewey_to_n[dewey] = dewey_to_n.get(dewey, 0) + 1

    dewey_to_rows = {}
    rem_rows = N_SHELF_ROWS
    dewey_to_rem_rows_f = {}
    for dewey, n_dewey in sorted(
            dewey_to_n.items(), key=lambda item: item[0]):
        rows_f = n_dewey * 1.0 * N_SHELF_ROWS / n
        rows = (int)(rows_f)
        dewey_to_rows[dewey] = rows
        dewey_to_rem_rows_f[dewey] = (rows_f - rows)
        rem_rows -= rows

    for dewey, __ in sorted(
            dewey_to_rem_rows_f.items(), key=lambda item: -item[1]):
        if rem_rows > 0:
            dewey_to_rows[dewey] += 1
            rem_rows -= 1
        else:
            break

    return dewey_to_rows


def get_dewey4_to_rows():
    book_list = get_book_list()
    n = len(book_list)
    dewey_to_n = {}
    for d in book_list:
        dewey = d['dewey'][:4]
        dewey_to_n[dewey] = dewey_to_n.get(dewey, 0) + 1

    books_per_row = n / N_SHELF_ROWS
    books_in_cur_row = 0
    prev_dewey1 = None
    for dewey, n_dewey in dewey_to_n.items():
        dewey1 = dewey[:1]
        if dewey1 != prev_dewey1:
            books_in_cur_row = 0
            print('-' * 32)

        books_in_cur_row += n_dewey
        print(dewey[:3] + '.' + dewey[3:], n_dewey, books_in_cur_row)

        if books_in_cur_row > books_per_row:
            books_in_cur_row = 0
            print('-' * 32)

        prev_dewey1 = dewey1

    return None


def run():
    get_dewey4_to_rows()


if __name__ == '__main__':
    run()

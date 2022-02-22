import os

from utils import tsv

MAX_X = 2
N_SHELF_ROWS = 16


def parse_dewey(s):
    s = s.replace('/', '')
    try:
        return '%03d' % (float)(s)
    except Exception:
        return '000'


def run(book_data_file):
    data_list = list(map(
        lambda d: dict(dewey=parse_dewey(d['Dewey'])),
        tsv.read(book_data_file, delimiter=','),
    ))
    n = len(data_list)
    dewey_x_to_n = {}
    for d in data_list:
        dewey = d['dewey']
        for i in range(0, MAX_X):
            dewey_x = str(dewey)[:i + 1] + ('-' * (2 - i))
            dewey_x_to_n[dewey_x] = dewey_x_to_n.get(dewey_x, 0) + 1

    for dewey_x, n_x in sorted(dewey_x_to_n.items(), key=lambda item: item[0]):
        p = n_x / n
        shelf_rows = p * N_SHELF_ROWS
        i = 2 - (len(dewey_x) - len(dewey_x.replace('-', '')))
        dewey_x = dewey_x.replace('-', 'x')
        print(i * '\t', f'{dewey_x}: {n_x} ({p:.0%}, {shelf_rows:.1f} rows)')


if __name__ == '__main__':
    BOOK_DATA_FILE = os.path.join(
        '/Users/nuwan.senaratna/Dropbox',
        '_BOOKS',
        'NUWANS_BOOKS.clz.csv',
    )
    run(BOOK_DATA_FILE)

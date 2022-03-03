import os

from utils import tsv

from Book import Book

BOOK_DATA_FILE = os.path.join(
    '/Users/nuwan.senaratna/Dropbox',
    '_BOOKS',
    'NUWANS_BOOKS.clz.csv',
)


class BookList:
    def __init__(self):
        self.__book_list__ = list(map(
            Book.buildFromCLZDatum,
            tsv.read(BOOK_DATA_FILE, delimiter=','),
        ))

    def __len__(self):
        return len(self.__book_list__)

    def __str__(self):
        return f'BookList({len(self)} books)'


if __name__ == '__main__':
    book_list = BookList()
    print(book_list)

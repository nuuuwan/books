from textwrap import wrap

from utils import filex, tsv

from _constants import BOOK_DATA_FILE
from Book import Book
from ddc import get_dewey2_description


class BookList:
    def __init__(self):
        self.__book_list__ = list(map(
            Book.buildFromCLZDatum,
            tsv.read(BOOK_DATA_FILE, delimiter=','),
        ))

    @property
    def book_list(self):
        return self.__book_list__

    def __len__(self):
        return len(self.__book_list__)

    def __str__(self):
        return '\n'.join(list(map(
            str,
            self.book_list,
        )))

    def __iter__(self):
        for book in self.book_list:
            yield book

    def get_shelf_row_to_books(self):
        shelf_row_to_books = {}
        for book in self:
            shelf_row = book.shelf_row
            if shelf_row not in shelf_row_to_books:
                shelf_row_to_books[shelf_row] = []
            shelf_row_to_books[shelf_row].append(book)

        return shelf_row_to_books

    def get_shelf_layout(self):
        lines = []
        shelf_row_to_books = self.get_shelf_row_to_books()
        sorted_shelf_row_and_books = sorted(
            shelf_row_to_books.items(), key=lambda x: x[0])
        for shelf_row, books in sorted_shelf_row_and_books:
            lines.append('-' * 32)
            lines.append(f'SHELF {shelf_row[0]}, ROW {shelf_row[-1]}')
            lines.append(get_dewey2_description(books))
            lines.append('-' * 32)
            books = sorted(books, key=lambda book: book.sort_key)
            for book in books:
                lines.append(
                    '\n'.join(
                        wrap(
                            str(book),
                            width=64,
                            initial_indent='\t',
                            subsequent_indent='\t\t')))
        return '\n'.join(lines)

    def store_shelf_layout(self, file_name):
        filex.write(file_name, self.get_shelf_layout())
        print(f'Wrote {file_name}')


if __name__ == '__main__':
    book_list = BookList()
    book_list.store_shelf_layout('/tmp/books.shelf_layout.txt')

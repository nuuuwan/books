import sys
from textwrap import wrap

from fuzzywuzzy import fuzz
from utils import filex, tsv

from _constants import BOOK_DATA_FILE
from _utils import get_count
from Book import Book
from book_shelf import get_shelf_row
from ddc import get_dewey_description
from oclc import search_by_isbn

MIN_SIMILARITY = 80


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
            shelf_row = get_shelf_row(book)
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
            print(f'Adding {len(books)} books to {shelf_row}')
            lines.append('-' * 32)
            lines.append(f'SHELF {shelf_row[0]}, ROW {shelf_row[-1]}')
            lines.append(get_dewey_description(books))
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

    def get_author_to_count(self):
        return get_count(self, lambda book: book.author_in_ref_order_list)

    def get_similar_author_pairs(self):
        author_to_count = book_list.get_author_to_count()
        author_list = sorted(list(author_to_count.keys()))
        n = len(author_list)
        similar_author_pairs = []
        for i1 in range(0, n - 1):
            author1 = author_list[i1]
            for i2 in range(i1 + 1, n):
                author2 = author_list[i2]
                similarity = fuzz.ratio(author1, author2)
                if MIN_SIMILARITY <= similarity:
                    similar_author_pairs.append([author1, author2])
        return similar_author_pairs

    def analyze(self, start, display_limit=5):
        i_display = 0
        n = len(self)
        for i_book, book in enumerate(self.book_list[start:]):
            isbn = book.isbn
            if isbn in ['9780761964810']: continue
            summary_list = search_by_isbn(isbn)

            if summary_list:
                summary_title = summary_list[0].get('Title', '')
                title_similarity = fuzz.ratio(
                    book.title.lower(),
                    summary_title.lower(),
                )
                if title_similarity < 70:
                    print('-' * 32)
                    print(i_display+ 1, ')', i_book + start + 1, 'of', n)
                    print(isbn)
                    print(book)
                    print('title_similarity = ', title_similarity)
                    print('\t - ', book.title)
                    print('\t + ', summary_title)
                    i_display += 1
                    if i_display >= display_limit:
                        break


if __name__ == '__main__':
    start = (int)(sys.argv[1])
    book_list = BookList()
    book_list.analyze(start=start)

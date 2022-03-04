import os
import sys

from bs4 import BeautifulSoup
from utils import www

from _utils import log
from books.Book import UNKNOWN_DEWEY, Book

MAX_BOOKS_TO_SEARCH = 1
DELIM_AUTHOR_LIST = ';'


def parse_oclc_author(author):
    return list(map(
        lambda author: author.strip(),
        author.split(DELIM_AUTHOR_LIST),
    ))


def get_url_for_isbn(isbn):
    return os.path.join(
        'http://classify.oclc.org',
        'classify2',
        f'ClassifyDemo?search-standnum-txt={isbn}'
    )


def parse_page(isbn, url):
    log.debug(f'Searching {url}...')
    html = www.read(url)
    soup = BeautifulSoup(html, 'html.parser')

    # summary
    dl = soup.find('dl')
    summary = {}
    latest_key = None
    for child in dl:
        if child.name == 'dt':
            latest_key = child.text[:-1]
        elif child.name == 'dd':
            summary[latest_key] = child.text

    # ddc
    table = soup.find('table', {'id': 'classSummaryData'})
    if table.find('thead').find('tr').find('th').text[:3] == 'DDC':
        most_common_dewey = table.find('tbody').find(
            'tr').find_all('td')[1].text
        summary['most_common_dewey'] = most_common_dewey

    return Book(
        title=summary['Title'],
        author_list=parse_oclc_author(summary['Author']),
        dewey=summary.get('most_common_dewey', UNKNOWN_DEWEY),
        isbn=isbn,
    )


def parse_index(isbn):
    url = get_url_for_isbn(isbn)
    html = www.read(url)
    soup = BeautifulSoup(html, 'html.parser')
    table_results = soup.find('table', {'id': 'results-table'})
    url_list = []
    for tr in table_results.find('tbody').find_all('tr'):
        first_td = tr.find('td')
        a = first_td.find('a')
        url_list.append(os.path.join(
            'http://classify.oclc.org',
            a['href'][1:],
        ))
    return url_list


def search_by_isbn(isbn):
    url_list = parse_index(isbn)
    book_list = []
    for url in url_list[:MAX_BOOKS_TO_SEARCH]:
        book_list.append(parse_page(isbn, url))
    return book_list


if __name__ == '__main__':
    isbn = sys.argv[1]
    for book in search_by_isbn(isbn):
        log.info(book)

import os
import sys

from bs4 import BeautifulSoup
from utils import www

from _utils import log
from books.Book import normalize_dewey

MAX_BOOKS_TO_SEARCH = 3
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
    dewey_list = []
    for tr in table.find('tbody').find_all('tr'):
        th_list = tr.find_all('th')
        if th_list:
            if 'DDC' not in th_list[0]:
                break
        td_list = tr.find_all('td')
        if td_list:
            dewey_list.append(normalize_dewey(td_list[1].text))

    summary['dewey_list'] = list(set(dewey_list))
    return summary


def parse_index(isbn):
    url = get_url_for_isbn(isbn)
    html = www.read(url)
    soup = BeautifulSoup(html, 'html.parser')
    table_results = soup.find('table', {'id': 'results-table'})
    if not table_results:
        return []

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
    summary_list = []
    for url in url_list[:MAX_BOOKS_TO_SEARCH]:
        summary_list.append(parse_page(isbn, url))
    return summary_list


if __name__ == '__main__':
    isbn = sys.argv[1]
    for summary in search_by_isbn(isbn):
        log.info(summary)

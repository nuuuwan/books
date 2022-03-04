from utils import tsv

DDC_FILE = 'ddc.csv'


def get_ddc_data_list():
    return tsv.read(DDC_FILE, delimiter=',')


def get_dewey_index():
    data_list = tsv.read(DDC_FILE, delimiter=',')
    return dict(list(map(
        lambda d: [d['Code'].replace('x', ''), d['Name']],
        data_list,
    )))


def get_dewey_description(books):
    dewey_index = get_dewey_index()
    dewey_set = set()
    for book in books:
        dewey_set.update([book.dewey_n(1), book.dewey_n(2)])
    return '\n'.join(map(
        lambda dewey2: dewey2 + ' ' + dewey_index[dewey2],
        sorted(dewey_set),
    ))

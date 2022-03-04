from utils import tsv

DDC_FILE = 'ddc.csv'


def get_ddc_data_list():
    return tsv.read(DDC_FILE, delimiter=',')


def get_dewey2_index():
    data_list = tsv.read(DDC_FILE, delimiter=',')
    dewey3_data_list = list(filter(
        lambda d: d['Code'][1] != 'x' and d['Code'][2] == 'x',
        data_list,
    ))
    return dict(list(map(
        lambda d: [d['Code'][:2], d['Name']],
        dewey3_data_list,
    )))


def get_dewey2_description(books):
    dewey2_index = get_dewey2_index()
    dewey2_set = set()
    for book in books:
        dewey2 = book.dewey_n(2)
        dewey2_set.add(dewey2)
    return '\n'.join(map(
        lambda dewey2: dewey2 + 'x ' + dewey2_index[dewey2],
        sorted(dewey2_set),
    ))


if __name__ == '__main__':
    print(get_dewey2_index())

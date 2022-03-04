from utils import tsv

DDC_FILE = 'ddc.csv'
N_DESCRIPTION = 2


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
    dewey_to_count = {}
    for book in books:
        deweys = [book.dewey_n(i + 1) for i in range(0, N_DESCRIPTION)]
        for dewey in deweys:
            dewey_to_count[dewey] = dewey_to_count.get(dewey, 0) + 1

    return '\n'.join(map(
        lambda item: item[0] + ' ' + dewey_index[item[0]] + ' (' + str(item[1]) + ')',
        sorted(dewey_to_count.items(), key=lambda item: item[0]),
    ))

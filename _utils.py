from utils import logx

log = logx.get_logger('books')


def get_count(iter, func_get_keys):
    key_to_count = {}
    for item in iter:
        keys = func_get_keys(item)
        for key in keys:
            key_to_count[key] = key_to_count.get(key, 0) + 1
    return key_to_count

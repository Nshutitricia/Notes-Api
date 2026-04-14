from typing import Tuple


def find_item(items, cb) -> Tuple[dict, int]:
    for idx, item in enumerate(items):
        if cb(item):
            return item , idx
    return {} , -1

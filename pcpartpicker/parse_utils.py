import base64
import json
import re
from decimal import Decimal
from multiprocessing import Pool
from typing import Tuple, Dict

import lz4.frame
from dacite import from_dict, Config
from moneyed import Money

from .mappings import part_classes


def dataclass_from_dict(datatype, dictionary: dict):
    result = {}
    for field, data in dictionary.items():
        if isinstance(data, list):
            if not len(data) == 2 or not isinstance(data[0], str) or not isinstance(data[1], str):
                raise RuntimeError
            money = Money(Decimal(data[0]), data[1])
            result.update({field: money})
        else:
            result.update({field: data})
    dataclass = from_dict(datatype, result, config=Config(check_types=False))
    return dataclass


def deserialize_part_data(part_data: Tuple[str, str]) -> list:
    body = re.findall('<body>(.*?)</body>', part_data[1], re.DOTALL)[0].strip().lstrip()
    byte_str = base64.urlsafe_b64decode(body)
    deserialized_parts = json.loads(lz4.frame.decompress(byte_str))
    return [dataclass_from_dict(part_classes[part_data[0]], item) for item in deserialized_parts]


def parse(part_dict: Dict[str, str], multithreading: bool = True) -> Dict[str, list]:
    if multithreading:
        with Pool() as pool:
            results = pool.map(deserialize_part_data, (item for item in part_dict.items()))
    else:
        results = [deserialize_part_data(item) for item in part_dict.items()]
    return dict(zip(part_dict.keys(), results))

import json
from typing import Optional


def scale_cross_lines(file_name: str, width: int, height: int) -> (list[int], list[int]):
    """
    Scale enter and exit cross-lines.
    :param file_name: Name of a json file with detections and configurations settings.
    :param width: Height to scale.
    :param height: Width to scale.
    :return:
        List of scaled coordinates for enter cross-line,
        List of scaled coordinates for exit cross-line,
    """

    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Cross-lines in the original json file represented as a single-element list so take a first element.
    cross_lines = find_data_in_dictionary(data, 'cross_lines')[0]
    # Height & width scaling.
    cross_line_width, cross_line_height = cross_lines['box']

    scaled_width = width / cross_line_width
    scaled_height = height / cross_line_height

    # Scale exit & enter cross-lines.
    ext_line = [
        int(x * scaled_width) if i % 2 == 0
        else int(x * scaled_height)
        for i, x in enumerate(cross_lines['ext_line'])
    ]

    int_line = [
        int(x * scaled_width) if i % 2 == 0
        else int(x * scaled_height)
        for i, x in enumerate(cross_lines['int_line'])
    ]

    return int_line, ext_line


def find_data_in_dictionary(data: dict, key: str) -> Optional[dict]:
    """
    Recursively iterate over dict and find cross-lines data.
    :return:
    :param data: Dictionary with data.
    :param key: Key to find required data.
    :return: Dictionary with data by key.
    """
    if not isinstance(data, dict):
        return None

    required_data = None
    for k, v in data.items():
        if k == key:
            return data[k]

        if isinstance(v, dict):
            result = find_data_in_dictionary(data[k], key)
            if result is not None:
                required_data = result

    return required_data

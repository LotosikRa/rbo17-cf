from .algo import calculate


def parse_string_to_array(string):
    array = []
    strs_array = string.split(' ')
    for pair in strs_array:
        x, y = pair.split(',')
        x, y = int(x), int(y)
        assert x >= 0
        assert y >= 0
        array.append((x, y))
    return array

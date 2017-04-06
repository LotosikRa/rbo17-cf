from app import calculate, examples as e, parse_string_to_array as psta


if __name__ == '__main__':
    assert calculate(psta(e.sample1)) == 6
    assert calculate(psta(e.sample2)) == 4
    assert calculate(psta(e.sample3)) == 4
    assert calculate(psta(e.sample4)) == 10
    print('Tests completed.')

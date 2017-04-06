from app import calculate, examples as e, parse_string_to_array


if __name__ == '__main__':
    assert calculate(parse_string_to_array(e.sample_checkers1)) == 6
    assert calculate(parse_string_to_array(e.sample_checkers2)) == 4
    assert calculate(parse_string_to_array(e.sample_checkers3)) == 4
    assert calculate(parse_string_to_array(e.sample_checkers4)) == 10
    print('Tests completed.')

from app import algo, examples
from app.cli_tools import parse_string_to_array


def run_sample(sample_string: str, goal: int):
    return algo.calculate(parse_string_to_array(sample_string), goal)


def print_test_result(text: str, string, goal, expected, result):
    message = '{text} for: string_form="{string}"\n\tgoal={goal}\texpected={expected}\tresult={result}'
    print(message.format(**locals()))


def test_samples(verbose=True, raise_immidiately=False):
    if not verbose and not raise_immidiately:
        raise RuntimeError('Wrong arguments.')
    for string, expected, goal in examples.samples:
        result = run_sample(string, goal)
        text = '!!! unknown behavior'
        try:
            assert result == expected
        except AssertionError:
            text = '!!! Wrong test result'
            if raise_immidiately:
                raise
        else:
            text = '... Successful test'
        finally:
            if verbose:
                print_test_result(text, string, expected, goal, result)


if __name__ == '__main__':
    print('=' * 20, 'Starting tests', '=' * 20)
    test_samples()
    print('=' * 20, 'Tests completed', '=' * 20)

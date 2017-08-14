import pytest

import tests
from app import algo, examples
from app.cli_tools import parse_string_to_array


@pytest.mark.parametrize('array, expected, goal',
                         [(parse_string_to_array(s), e, g) for s, e, g in examples.samples],
                         ids=[str(i) for i in range(1, len(examples.samples) + 1)])
def test_sample_benchmark(array: list, expected: int, goal: int, benchmark):
    res = benchmark(algo.calculate, array, goal)
    assert res == expected


def test_all_samples():
    tests.test_samples(verbose=False, raise_immidiately=True)

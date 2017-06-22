from app import algo, examples as e, parse_string_to_array as psta


try:
    import pytest
except ImportError:
    pass
else:
    @pytest.mark.parametrize('array, expected, goal', [(psta(s), e, g) for s, e, g in e.samples],
                             ids=[str(i) for i in range(1, len(e.samples) + 1)])
    def test_sample(array: list, expected: int, goal: int, benchmark):
        assert benchmark(algo.calculate, array, goal) == expected
finally:
    if __name__ == '__main__':
        assert algo.calculate(psta(e.sample1), 4) == 6
        assert algo.calculate(psta(e.sample2), 4) == 4
        assert algo.calculate(psta(e.sample3), 4) == 4
        assert algo.calculate(psta(e.sample4), 4) == 10
        print('Tests completed.')

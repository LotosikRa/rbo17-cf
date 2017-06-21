from app import algo, examples as e, parse_string_to_array as psta


try:
    import pytest
except ImportError:
    pass
else:
    @pytest.mark.parametrize('array, expected', [(psta(s), e) for s, e in e.samples],
                             ids=[str(i) for i in range(1, len(e.samples) + 1)])
    def test_sample(array: list, expected: int, benchmark):
        assert benchmark(algo.calculate, array, goal=4) == expected
finally:
    if __name__ == '__main__':
        assert algo.calculate(psta(e.sample1)) == 6
        assert algo.calculate(psta(e.sample2)) == 4
        assert algo.calculate(psta(e.sample3)) == 4
        assert algo.calculate(psta(e.sample4)) == 10
        print('Tests completed.')

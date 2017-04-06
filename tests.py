from app import calculate, examples as e


if __name__ == '__main__':
    assert calculate(e.sample_checkers1) == 6
    assert calculate(e.sample_checkers2) == 4
    assert calculate(e.sample_checkers3) == 4

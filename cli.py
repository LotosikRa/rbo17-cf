""" This module runs algorithm with CLI. """
from app import calculate
from settings import CHECKERS, COLUMNS, ROWS, GOAL


def get_user_input():
    """
    Example of input values:
    1. 15
    2. 15
    3. 12
    4. 4
    5. 0,0 0,9 4,0 4,3 4,6 4,9 8,0 8,3 8,6 8,9 12,0 12,9
    :return: tuple with arguments for `calculate`
    """
    print("""This is how coordinates looks like:
    +---+---+-
    |0,0|1,0|
    +---+---+-
    |0,1|1,1|
    +---+---+-
    |   |   |
    """)
    if input('Use defaults? (Y, *): ') != 'Y':
        goal = input('Enter how many checkers must in one line: ')
        cols = input('Enter number of the columns: ')
        rows = input('Enter number of the rows: ')
        total = input('Enter total number of the checkers: ')
    else:
        cols = COLUMNS
        total = CHECKERS
        rows = ROWS
        goal = GOAL
    string = input('Enter coordinates of each checker in the format `2,3 5,10`: ')
    try:
        for item in [cols, rows, total, goal]:
            item = int(item)
            assert item > 0
        array = []
        strs_array = string.split(' ')
        for pair in strs_array:
            x, y = pair.split(',')
            x, y = int(x), int(y)
            assert x >= 0
            assert y >= 0
            array.append((x, y))
        indata = array, goal, cols, rows, total
        print('You have entered (in order)..: {}'.format(str(indata[1:])))
        print('Entered checkers: {}'.format(str(indata[0])))
        return indata
    except Exception as e:
        print(e)
        print('Check enter values.')


def main():
    print('Hello World!')
    while input('Press `Y` to continue: ') in ['Y', '']:
        indata = get_user_input()
        try:
            outdata = calculate(*indata)
        except Exception as e:
            print(e)
        else:
            print('You have `{}` points!'.format(outdata))
    else:
        print('Goodbye!')


if __name__ == '__main__':
    main()

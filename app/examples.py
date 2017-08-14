""" Module wih examples. """
from app import parse_string_to_array
from settings import COLUMNS, ROWS


# constants
exist = 'X'
not_exist = ' '


# helper function
def get_array(tuples_array):
    # create example
    example = []
    for x in range(ROWS):
        example.append([])
        for y in range(COLUMNS):
            example[x].append(not_exist)

    for x, y in tuples_array:  # for better graphical reproduction
        example[x][y] = exist

    return example


# example of checkers array
sample1 = '0,0 0,9 4,0 4,3 4,6 4,9 8,0 8,3 8,6 8,9 12,0 12,9'
""" 4-6
. . . .
  . .
. . . .
"""
sample2 = '1,0 2,0 0,1 1,1 2,1 3,1 0,2 1,2 2,2 3,2 1,3 2,3'
""" 4-4
  . .
. . . .
. . . .
  . .
"""
sample3 = '0,0 1,0 2,0 3,0 1,1 2,1 3,1 1,2 2,2 3,2 0,3 3,3'
""" 4-4
. . . .
  . . .
  . . .
.     .
"""
sample4 = '0,0 1,0 2,0 3,0 4,0 0,1 1,1 3,1 4,1 0,2 2,2 4,2' \
          ' 0,3 1,3 3,3 4,3 0,4 1,4 2,4 3,4 4,4'
""" 4-10
. . . . .
. .   . .
.   .   .
. .   . .
. . . . .
"""
sample5 = '0,0 1,0 3,0 4,0 1,2 2,2 3,2 5,2 1,4 2,4 3,4 0,6 1,6 3,6 4,6'
""" 4-9
XX XX

 XXX X

 XXX

XX XX
"""


samples = [(sample1, 6, 4),
           (sample2, 4, 4),
           (sample3, 4, 4),
           (sample4, 10, 4),
           (sample5, 9, 4), ]


if __name__ == '__main__':
    # prints all existed examples
    for e, *_ in samples:
        print('\tStart:')
        array = get_array(parse_string_to_array(e))
        for i in range(len(array)):
            print(''.join(array[i]))
        print('\t:End')

""" Module wih examples. """
from app import parse_string_to_array
from settings import COLUMNS, ROWS


# constants
exist = 1
not_exist = 0


# helper function
def get_array(tuples_array):
    # create example
    example = []
    for x in range(ROWS):
        example.append([])
        for y in range(COLUMNS):
            example[x].append(not_exist)

    for y, x in tuples_array:  # for better graphical reproduction
        example[x][y] = exist

    return example


# example of checkers array
sample1 = '0,0 0,9 4,0 4,3 4,6 4,9 8,0 8,3 8,6 8,9 12,0 12,9'
""" 6
. . . .
  . .
. . . .
"""
sample2 = '1,0 2,0 0,1 1,1 2,1 3,1 0,2 1,2 2,2 3,2 1,3 2,3'
""" 4
  . .
. . . .
. . . .
  . .
"""
sample3 = '0,0 1,0 2,0 3,0 1,1 2,1 3,1 1,2 2,2 3,2 0,3 3,3'
""" 4
. . . .
  . . .
  . . .
.     .
"""
sample4 = '0,0 1,0 2,0 3,0 4,0 0,1 1,1 3,1 4,1 0,2 2,2 4,2' \
          ' 0,3 1,3 3,3 4,3 0,4 1,4 2,4 3,4 4,4'
""" 10
. . . . .
. .   . .
.   .   .
. .   . .
. . . . .
"""


if __name__ == '__main__':
    # prints all existed examples
    for e in [sample1,
              sample2,
              sample3,
              sample4,]:
        print('\tStart:')
        array = get_array(parse_string_to_array(e))
        for i in range(len(array)):
            print(array[i])
        print('\t:End')

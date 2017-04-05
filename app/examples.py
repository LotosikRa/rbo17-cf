""" Module wih examples. """

# constants
a = 15  # horizontal rows
b = 15  # vertical rows
n = 12  # number of checkers
k = 4  # number of checkers in one row for new coin
exist = 1
not_exist = 0


# helper function
def get_array(tuples_array):
    # create example
    example = []
    for x in range(a):
        example.append([])
        for y in range(b):
            example[x].append(not_exist)

    for y, x in tuples_array:  # for better graphical reproduction
        example[x][y] = exist

    return example


# example of checkers array
sample_checkers1 = [(0 ,0),
                    (0 ,9),
                    (4 ,0),
                    (4 ,3),
                    (4 ,6),
                    (4 ,9),
                    (8 ,0),
                    (8 ,3),
                    (8 ,6),
                    (8 ,9),
                    (12,0),
                    (12,9),]
"""
. . . .
  . .
. . . .
"""


# print first example
def pex1():
    for i in range(a):
        print(get_array(sample_checkers1)[i])


if __name__ == '__main__':
    pex1()

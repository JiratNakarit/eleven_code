import math

def find_c(a, b):

    a = math.pow(a, 2)
    b = math.pow(b, 2)
    c = math.sqrt(a+b)
    return c

if __name__ == "__main__":

    # a = (0.972e-3)/2
    # b = 1.93e-3
    # c = find_c(a, b)

    a = (160e-3)/2
    b = 327.572e-3
    c = find_c(a, b)

    print(c)

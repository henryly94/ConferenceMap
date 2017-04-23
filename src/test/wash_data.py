#!/usr/bin/python
# coding=utf-8
import math
import sys
from sklearn.preprocessing import scale


assert len(sys.argv) == 3, "\nUsage:\n\tpython wash_data.py confer_vec washed_vec"
path_confer, path_washed = sys.argv[1:3]



def read_data():
    confer_vecs = list()
    with open(path_confer, 'r') as f:
        for line in f:
            try:
                new_vec = map(float, line.strip().split(' '))
                confer_vecs.append(new_vec)
            except ValueError:
                pass
    return confer_vecs


def regularize(a):
    A = math.sqrt(sum(map(lambda c:c*c, a)))
    if A == 0.0:
        return a
    else:
        return map(lambda c:c/A, a)

def write_data(data):
    with open(path_washed, 'w') as f:
        for vec in data:
            f.write(" ".join(map(str, vec)) + '\n')

def main():
    confer_vecs = read_data()

    reg_confer_vecs = map(regularize, confer_vecs)

    write_data(reg_confer_vecs)

if __name__ == "__main__":
    main()

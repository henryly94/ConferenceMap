#!/usr/bin/python
# coding=utf8

import sys
import math
import numpy as np

assert len(sys.argv) == 4, "Usage:\n\tpython gen_confervec.py confer_vec confer_tag tsne_confer_vec"
path_confer, path_tag, path_cluster = sys.argv[1:4]


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


def cluster():
    pass


def main():
    pass


if __name__ == '__main__':
    main()


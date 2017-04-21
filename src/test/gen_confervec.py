#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

assert len(sys.argv) == 3, "Usage:\n\tpython gen_confervec.py confer_vec tsne_confer_vec"
path_confer, path_tsne = sys.argv[1:3]

tsne = TSNE(n_components=2, init='pca', random_state=0)


def read_data():
    confer_vecs = list()
    with open(path_confer, 'r') as f:
        for line in f:
            try:
                new_vec = map(float, line.strip().split(' '))
                confer_vecs.append(new_vec)
            except ValueError:
                pass
    return np.array(confer_vecs)

def write_data(data):
    delim = ' '
    with open(path_tsne) as f:
        for vec in data:
            f.write(delim.join(vec))
            f.write('\n')

def plot_embedding(X):
    #坐标缩放到[0,1]区间
    x_min, x_max = np.min(X,axis=0), np.max(X,axis=0)
    X = (X - x_min) / (x_max - x_min)
    #降维后的坐标为（X[i, 0], X[i, 1],X[i,2]），在该位置画出对应的digits
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    for i in range(X.shape[0]):
        ax.text(
                X[i, 0], X[i, 1], X[i,2],str(digits.target[i]),
                color=plt.cm.Set1(y[i] / 10.),
                fontdict={'weight': 'bold', 'size': 9})


def main():
    pass

if __name__ == '__main__':
    main()



#!/usr/bin/python
# coding=utf8
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

assert len(sys.argv) == 4, "Usage:\n\tpython gen_confervec.py confer_vec confer_tag tsne_confer_vec"
path_confer, path_tag, path_tsne = sys.argv[1:4]

tsne = TSNE(n_components=3, init='pca', random_state=0)
pca = PCA(n_components=2)

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

def read_tag():
    confer_tags = list()
    with open(path_tag, 'r') as f:
        for line in f:
            try:
                confer_name, paper_amt = line.strip().split(' ')
                confer_tags.append((confer_name, int(paper_amt)))
            except ValueError:
                print line
    return confer_tags


def write_data(data):
    delim = ' '
    with open(path_tsne, 'w') as f:
        for vec in data:
            f.write(delim.join(map(str, vec)))
            f.write('\n')


def plot_embedding(X, tags):
    #坐标缩放到[0,1]区间
    x_min, x_max = np.min(X,axis=0), np.max(X,axis=0)
    print x_min, x_max
    X = (X - x_min) / (x_max - x_min)
    #降维后的坐标为（X[i, 0], X[i, 1],X[i,2]），在该位置画出对应的digits
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    print X.shape, len(tags)
    for i in range(X.shape[0]):
        ax.text(
                X[i, 0], X[i, 1], X[i, 2], str(tags[i][0]),
                fontdict={'weight': 'bold', 'size': 9})
    
    fig.savefig("ConferMap.png")

    plt.show()
    

def cosine(a, b):
    assert len(a) == len(b) and type(a[0]) == type(b[0]) == type(0.0)

    # \sqrt_{\sum_{a^2}}
    A, B = map(lambda e: math.sqrt(sum(map(lambda c:c*c, e))), [a,b])
    A_B = sum(map(lambda c: c[0] * c[1], zip(a,b)))
    try:
        res = A_B / (A * B)
    except ZeroDivisionError:
        return 0.0
    return res


def euler(a, b):
    return math.sqrt(sum(map(lambda p: (p[0]-p[1])*(p[0]-p[1]), zip(a, b))))


def cosine_dis(tar, vecs, tags):
    assert  type(tar[0]) == type(vecs[0][0]), "Type Error"
    distances = list()
    for i, each in enumerate(vecs):
        cos_dis = cosine(tar, each)
        distances.append(cos_dis)
    res = zip(distances, tags)
    res.sort(key=lambda c:c[0], reverse=True)
    return map(lambda c:c[1], res[:10])


def euler_dis(tar, vecs, tags):
    assert  type(tar[0]) == type(vecs[0][0]), "Type Error"
    distances = list()
    for i, each in enumerate(vecs):
        eu_dis = euler(tar, each)
        distances.append(eu_dis)
    res = zip(distances, tags)
    res.sort(key=lambda c:c[0])
    return map(lambda c:c[1], res[:10])


def test():
    confer_vec = read_data().tolist()
    confer_tags = read_tag()
    
    confer_tags = map(lambda c:c[0], confer_tags)
    
    tag2num = dict([[b, a] for a, b in enumerate(confer_tags)])

    while True:
        req = raw_input(">>")
        req_confer_num = tag2num.get(req, -1)
        if req == 'q':
            break
        if req_confer_num == -1:
            continue
        target = confer_vec[req_confer_num]
        print cosine_dis(target, confer_vec, confer_tags)
        


def main():

    # Read Conference Vector

    # T-SNE
    confer_vec = tsne.fit_transform(read_data())

    # PCA
    # confer_vec = pca.fit_transform(read_data())


    # Read Conference Name and Paper Amount
    confer_tags = read_tag()

    # Draw Picture:
    plot_embedding(confer_vec, confer_tags)

    # Write Data
    write_data(confer_vec.tolist())

if __name__ == '__main__':
    # main()
    test()


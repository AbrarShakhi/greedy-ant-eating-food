import numpy as np


class DisjointSetUnion:
    def __init__(self):
        self.__set = {}
        self.__size = {}

    def make_set(self, item):
        self.__set[item] = item
        self.__size[item] = 1

    def find_set(self, item):
        if self.__set[item] == item:
            return item
        self.__set[item] = self.find_set(self.__set[item])
        return self.__set[item]

    def union_set(self, item1, item2):
        item1 = self.find_set(item1)
        item2 = self.find_set(item2)
        if item1 != item2:
            if self.__size[item1] < self.__size[item2]:
                self.__set[item1] = item2
                self.__size[item2] += self.__size[item1]
            else:
                self.__set[item2] = item1
                self.__size[item1] += self.__size[item2]


def make_mst(adjmat):
    n = len(adjmat)
    mst_adjmat = np.zeros((n, n), dtype=int)
    edges = []

    for i in range(n):
        # for j in range(n):
        # sematric matric
        # undirected graph
        for j in range(i, n):
            # if adjmat[i][j] != 0:
            # dsu will discard self loop
            edges.append((int(adjmat[i][j]), (i, j)))

    edges.sort(key=lambda based_on: based_on[0])

    dsu = DisjointSetUnion()
    for _, (i, j) in edges:
        dsu.make_set(i)
        if i != j:
            dsu.make_set(j)

    for wight, (i, j) in edges:
        iclan = dsu.find_set(i)
        jclan = dsu.find_set(j)
        if iclan != jclan:
            mst_adjmat[i][j] = wight
            mst_adjmat[j][i] = wight
            dsu.union_set(i, j)

    return mst_adjmat

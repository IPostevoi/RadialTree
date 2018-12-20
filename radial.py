import matplotlib.pyplot as plt
import numpy as np


class Node():
    depth = 0
    leaves = 0
    parent = None

    def __init__(self, index, data):
        self.index = index
        self.children = []
        self.data = data

    def add_child(self, obj):
        old_len = len(self.children)
        self.children.append(obj)
        obj.parent = self
        # update depth and leaves
        self.update_depth(obj)
        self.update_leaves(obj, old_len)

    def update_leaves(self, node, old_len):
        new_len = len(self.children)
        if old_len == 0:
            node.leaves = 1
            node.parent.leaves = 1

        elif not old_len == new_len:
            while True:
                node.leaves += 1
                if node.parent is None:
                    break
                node = node.parent

    def update_depth(self, node):
        node.depth = self.depth + 1
        while not len(node.children) == 0:
            for c in node.children:
                self.update_depth(c)



def radial_position(v, a, b, dens, G):
    D = v.depth
    if D == 0:
        G.append((0, 0, v.index, v.data))
    theta = a
    R_D = R_0 + zeta * D
    k = v.leaves
    for c in v.children:
        l = c.leaves
        mu = theta + min((l / float(k) * (b - a)), dens)
        G.append((R_D * np.cos((theta + mu) / 2), R_D * np.sin((theta + mu) / 2), c.index, c.data))
        if len(c.children) > 0:
            radial_position(c, theta, mu, dens, G)

        theta = mu
    return G


R_0 = 1
zeta = 1


def get_radial_tree(root, a, b, dens):
# root = Node(0)
# p = Node(1)
# q = Node(2)
# r = Node(3)
# qq = Node(4)
# zz = Node(5)
# zzz = Node(6)
# zzzz = Node(7)
#
# p.add_child(qq)
# p.add_child(qq)
# p.add_child(qq)
# qq.add_child(zzzz)
# qq.add_child(zzz)
# zzzz.add_child(q)
#     a = 0
#     b = 2 * np.p
    G = []
    radial_position(root, a, b, dens, G)
    return G


def create_tree(input):
    arr = []
    inp = input.split('\n')
    for i in inp:
        j = i.split(',')
        arr.append((j[0], j[1]))

    arr1 = [i[0] for i in arr]
    arr2 = [i[1] for i in arr]
    st = list(dict.fromkeys(arr1+arr2))
    dct = dict()
    for i in range(len(st)):
        dct[st[i]] = i
    nodes = [Node(i, st[i]) for i in range(len(st))]
    root = nodes[0]
    curr = root
    for index in range(0, len(st)-1):
        for i in arr:
            if i[0] == curr.data:
                curr.add_child(nodes[dct[i[1]]])
        curr = nodes[index + 1]
    return root, arr
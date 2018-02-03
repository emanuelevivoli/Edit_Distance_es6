# -*- coding: utf-8 -*-
# import numpy as np
from test import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
#import pickle

# path = ["file/9000_nomi_propri.txt",    "file/60000_parole_italiane.txt",   "file/280000_parole_italiane.txt"]
#
# n_word = 1
# n_type = 6
# n_gram = 3



res = pickle.load(open("pickle/res.p", "rb"))
_parola = pickle.load(open("pickle/parola.p", "rb"))
c = pickle.load(open("pickle/c.p", "rb"))

legend = ["standard", "radomized", "-1 elem", "+1 elem", "1 error", "2 error"]

for k in range(0, len(path)):
    for i in range(len(res[k])):
        print str(k)+" "+str(i)+": "+str(res[k][i])
    print

plt.switch_backend('TkAgg')

for l in range(0, 3):
    fig = plt.figure(l+1)

    plt.style.use('seaborn-deep')
    # axes = ["no gram"] + range(1, len(res[l]) + 1)
    axes = range(0, len(res[l]))
    plt.subplot(221)
    path_ = ((path[l].split(".")[0]).split("/"))[1].split("_")
    plt.title((str(path_[0]) + " " + str(path_[1]) + " " + str(path_[2])))

    plt.xlabel("n-gram")
    plt.ylabel("Distanza")
    for k in range(0, n_type):
        print "Distanza "+str(k)
        print [float(each_list[k * 3]) for each_list in res[l]]
        plt.plot(axes, [float(each_list[k * 3]) for each_list in res[l]])
    plt.legend(legend)

    # plt.subplot(223)
    # plt.xlabel("n-gram")
    # plt.ylabel("Tempo")
    # app = [res[l][1], res[l][2], res[l][3]]
    # for k in range(0, n_type):
    #     plt.plot(range(1, len(app)+1), [float(each_list[k * 3 +1]) for each_list in app])
    # plt.legend(legend)

    plt.subplot(223)
    plt.xlabel("n-gram")
    plt.ylabel("Tempo")
    for k in range(0, n_type):
        print "Tempo " + str(k)
        print [float(each_list[k * 3 +1]) for each_list in res[l]]
        plt.plot(axes, [float(each_list[k * 3 +1]) for each_list in res[l]])
    plt.legend(legend)

    ax = fig.add_subplot(122, projection='3d')
    plt.xlabel("")
    for z in axes:
        xs = [1, 2, 3, 4, 5, 6]
        ys = []
        for ri in enumerate(res[l][z-1]):
            if ri[0] in range(2, n_type*3, 3):
                ys.append(ri[1])
        # You can provide either a single color or an array. To demonstrate this,
        # the first bar of each set will be colored cyan.
        print "Distanza " + str(k)
        print ys
        ax.bar(xs, ys, zs=z, zdir='y', color=['b', 'g', 'r', 'm', 'y', 'c'], alpha=0.8)

    ax.set_xlabel('test')
    ax.set_ylabel('n-gram')
    ax.set_zlabel('C-Jaccard')

    # imposto grandezza finestra plot Maximized
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

plt.show()
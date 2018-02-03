# -*- coding: utf-8 -*-
from editDistance import *
import random
from timeit import default_timer as timer
import pickle

path = ["file/9000_nomi_propri.txt",    "file/60000_parole_italiane.txt",   "file/280000_parole_italiane.txt"]

n_word = 1
n_type = 6
n_gram = 3

c = [[] for i in range(len(path))]
_parola = [[] for i in range(0, len(path))]
for i in range(len(path)):
    _parola[i] = []

    file_to_gram(path[i], n_gram)
    path_ = (path[i].split("/"))[1].split("_")[0]
    # prendo n_word parole a caso dal file in considerazione
    for k in range(n_word):
        fp = open(path[i])
        rand = int(random.uniform(0, int(
            ((path[i].split("/"))[1].split("_")[0]))))
        for j, line in enumerate(fp):
            if j == rand:
                _parola[i].append(line.rstrip())
        fp.close()

    if debug: print "PAROLE "+str(path_)+" ELEMENTI"
    if debug: print _parola[i]

    #
    c[i] = [[] for j in range(n_word)]
    for j in range(n_word):
        c[i][j] = [[] for k in range(n_gram)]
        for k in range(n_gram):

            # ricerca stringa vicina alla primo elemento di _parola
            start = timer()
            A, CJ = n_gram_compare(path[i], _parola[i][j], k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end-start)
            c[i][j][k].append(CJ)

            # ricerca stringa randomizzata
            tmp = ''.join(random.sample(_parola[i][j],len(_parola[i][j])))
            start = timer()
            A, CJ = n_gram_compare(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)

            # parola senza un elemento
            tmp = _parola[i][j]
            midlen = len(tmp) / 2
            tmp = tmp[:midlen] + tmp[midlen + 1:]
            start = timer()
            A, CJ = n_gram_compare(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)

            # perola con un elemento random
            tmp = _parola[i][j]
            midlen = len(tmp) / 2
            tmp = tmp[:midlen] + chr(int(random.uniform(97, 122)))+tmp[midlen:]
            start = timer()
            A, CJ = n_gram_compare(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)

            # 1 SCAMBIATE CON LE VICINE
            a = ['s', 'q', 'z']
            v = ['c', 'f', 'g', 'b']
            y = ['t', 'g', 'h', 'u']
            u = ['i', 'j', 'h', 'y']
            l = ['p', 'o', 'k']
            tmp = ''
            count = None
            print _parola[i][j]
            for char in _parola[i][j]:
                if char in a and count is None:
                    char = a[int(random.uniform(0, len(a)))]
                    count = 1
                elif char in v and count is None:
                    char = v[int(random.uniform(0, len(v)))]
                    count = 1
                elif char in y and count is None:
                    char = y[int(random.uniform(0, len(y)))]
                    count = 1
                elif char in u and count is None:
                    char = u[int(random.uniform(0, len(u)))]
                    count = 1
                elif char in l and count is None:
                    char = l[int(random.uniform(0, len(l)))]
                    count = 1
                tmp = tmp + char
            if count is None:
                randi = int(random.uniform(0, len(tmp)))
                tmp = tmp[:randi]+chr(ord(list(tmp)[randi])+1)+tmp[randi+1:]
            start = timer()
            A, CJ = n_gram_compare(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)


            # 2 SCAMBIATE CON LE VICINE
            tmp = ''
            count = 0
            for char in _parola[i][j]:
                if char in a and count < 2:
                    char = a[int(random.uniform(0, len(a)))]
                    count += 1
                elif char in v and count < 2:
                    char = v[int(random.uniform(0, len(v)))]
                    count += 1
                elif char in y and count < 2:
                    char = y[int(random.uniform(0, len(y)))]
                    count += 1
                elif char in u and count < 2:
                    char = u[int(random.uniform(0, len(u)))]
                    count += 1
                elif char in l and count < 2:
                    char = l[int(random.uniform(0, len(l)))]
                    count += 1
                tmp = tmp + char
            if count < 2:
                randi = int(random.uniform(0, len(tmp)))
                tmp = tmp[:randi]+chr(ord(list(tmp)[randi])+1)+tmp[randi+1:]
                count += 1
            if count < 2:
                randi = int(random.uniform(0, len(tmp)))
                tmp = tmp[:randi]+chr(ord(list(tmp)[randi])+1)+tmp[randi+1:]
            start = timer()
            A, CJ = n_gram_compare(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)

pickle.dump(c, open("pickle/c.p","wb"))
pickle.dump(_parola, open("pickle/parola.p", "wb"))

res = [[] for i in range(len(path))]
med = [[] for i in range(len(path))]

for i in range(len(path)):
    res[i] = [[0]*n_type*3 for j in range(n_gram)]
    med[i] = [0]*n_gram
    for k in range(n_word):
        for l in range(n_gram):
            for j in range(n_type*3):
                res[i][l][j] = ((int(res[i][l][j])*int(med[i][l])) + (c[i][k][l][j][1] if isinstance(c[i][k][l][j],
                    (list, tuple)) else c[i][k][l][j]))/(med[i][l]+1)
            med[i][l] += 1

pickle.dump(res, open("pickle/res.p", "wb"))



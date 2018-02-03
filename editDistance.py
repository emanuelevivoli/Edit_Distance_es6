# -*- coding: utf-8 -*-
import os
debug = True


def cost(operator):
    if operator in ["COPY"]:
        return 0
    return 1

# cost of "DELETE", "INSERT", "REPLACE", "TWIDDLE" is 1


def edit_distance(x, y):
    m = len(x)
    n = len(y)
    c = [[float("inf") for i in range(n + 1)] for j in range(m + 1)]
    for i in range(0, m + 1):
        c[i][0] = i * cost("DELETE")
    for j in range(0, n + 1):
        c[0][j] = j * cost("INSERT")

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + cost("COPY")
            else:
                c[i][j] = c[i - 1][j - 1] + cost("REPLACE")
            if i >= 2 and j >= 2 and x[i - 1] == y[j - 2] and x[i - 2] == y[j - 1] and c[i - 2][j - 2] + cost(
                    "TWIDDLE") < c[i][j]:
                c[i][j] = c[i - 2][j - 2] + cost("TWIDDLE")
            if c[i - 1][j] + cost("DELETE") < c[i][j]:
                c[i][j] = c[i - 1][j] + cost("DELETE")
            if c[i][j - 1] + cost("INSERT") < c[i][j]:
                c[i][j] = c[i][j - 1] + cost("INSERT")
    return c[m][n]


def n_gram_decompose(x, n):
    if x is None:
        return []
    a = [None] * (len(x) - n + 1)
    for i in range(len(x) - n + 1):
        a[i] = x[i:i + n]
    return a


def jaccard(x_gram, y_gram):
    inter = [val for val in x_gram if val in y_gram]
    union = x_gram + [e for e in y_gram if e not in x_gram]
    if debug:
        print x_gram
        print y_gram
        print "inter: " + str(len(inter))
        print "union: " + str(len(union))
        print "CJ: " + str(float(0 if len(union) is 0 else float(len(inter)) / float(len(union))))
    return float(0 if len(union) is 0 else float(len(inter)) / float(len(union)))


def all_compare(path, x):
    mini = [None, len(x)]
    list_of_min = []
    list_of_min.append(mini)
    #confrontare con ogni parola, e calcolare per ogni parola l'edit distance
    f = open(path, 'r')
    for y in f:
        y = y.rstrip()
        tmp = edit_distance(x, y)
        if tmp < mini[1]:
            mini[0] = y
            mini[1] = tmp
            list_of_min.append(mini)
    f.close()
    list_of_min = list_of_min[-5:]
    if debug:
        print "min: " + str(mini)
        print "list of min: " + str(list(reversed(list_of_min)))
        print
    return mini, None


def n_gram_compare(path, x, n):
    if n is 0:
        return all_compare(path, x)

    path_ = ((path.split(".")[0]).split("/"))[1].split("_")[0]
    x_gram = n_gram_decompose(x, n)

    if debug:
        print str(n) + "-gram: " + str(x_gram) + ": "

    CJ = 0.0
    CJ_limit = 0.6
    mini = [None, len(x)]
    list_of_min = []
    list_of_min.append(mini)
    for i in range(len(x_gram)):
        file = str(path_) + "/" + str(n) + "-gram/" + str(x_gram[i]) + "_"
        if os.path.isfile(file):
            f = open(file, 'r')
            for y in f:
                y = y.rstrip()
                y_gram = n_gram_decompose(y, n)
                jack = jaccard(x_gram, y_gram)
                if CJ_limit < jack:
                    tmp = edit_distance(x, y)
                    if tmp < mini[1]:
                        mini[0] = y
                        mini[1] = tmp
                        CJ = jack
                        list_of_min.append(mini)
            f.close()
    list_of_min = list_of_min[-5:]
    if debug:
        print "min: " + str(mini)
        print "list of min: " + str(list(reversed(list_of_min)))
        print
    return mini, CJ


def file_to_gram(path, n_gram):
    path_ = ((path.split(".")[0]).split("/"))[1].split("_")[0]
    if not os.path.exists(str(path_)):
        os.makedirs(str(path_))
        fp = open(path)
        for num, j in enumerate(fp):
            line = j.rstrip()
            for k in range(n_gram):
                if not os.path.exists(str(path_)+"/"+str(k + 1) + "-gram"):
                    os.makedirs(str(path_)+"/"+str(k + 1) + "-gram")
                line_gram = n_gram_decompose(line, k + 1)

                # funzione che elimina gli elementi uguali
                # line_gram = list(set(line_gram))
                line_gram = dict.fromkeys(line_gram).keys()

                for i in range(len(line_gram)):
                    # if not os.path.exists(str(k + 1) + "-gram/" + str(line_gram[i]) + "_"):
                    #    os.makedirs(str(k + 1) + "-gram/" + str(line_gram[i]) + "_")
                    f = open(str(path_)+"/"+str(k+1)+"-gram/"+str(line_gram[i])+"_", 'a')
                    f.write(str(line)+'\n')
                    if debug:
                        print "file: "+str(path_)+" riga: "+str(num)+" "+str(line)
                    f.close()
        fp.close()
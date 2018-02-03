c = [[] for i in range(len(path))]
_parola = [[] for i in range(0, len(path))]
for i in range(len(path)):
    _parola[i] = []

    file_to_gram(path[i], n_gram)

    path_ = (path[i].split("/"))[1].split("_")[0]
    # prendo n_word parole randomicamente dal file in considerazione
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

    # PER OGNI PAROLA APPARTENENTE ALLE 5 PESCATE
    # RANDOMICAMENTE
    c[i] = [[] for j in range(n_word)]
    for j in range(n_word):

        # DATA LA PAROLA, ESEGUO LE MODIFICHE ALLA PAROLA
        # ED I TEST, CON N-GRAM DA 0 (INDICA NON UTILIZZARE
        # LA TECNICA N-GRAM) FINO A [ 1, 2, 3 ].
        c[i][j] = [[] for k in range(n_gram)]
        for k in range(n_gram):

            # TEST 1:   PAROLA RESTA INVARIATA
            start = timer()
            A, CJ = n_gram_compare(path[i], _parola[i][j], k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end-start)
            c[i][j][k].append(CJ)

            # TEST 2:   PERMUTO I CARATTERI ALL'INTERNO
            #           DELLA PAROLA
            tmp = ''.join(random.sample(_parola[i][j],len(_parola[i][j])))
            start = timer()
            A, CJ = n_gram_compare(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)

            # TEST 3:   PAROLA SENZA UN ELEMENTO
            #           IN POSIZIONE RANDOM
            tmp = _parola[i][j]
            midlen = len(tmp) / 2
            tmp = tmp[:midlen] + tmp[midlen + 1:]
            start = timer()
            A, CJ = n_gram_compare(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)

            # TEST 4:   PROLA CON L'AGGIUNTA DI UN
            #           ELEMENTO IN POSIZIONE RANDOM
            tmp = _parola[i][j]
            midlen = len(tmp) / 2
            tmp = tmp[:midlen] + chr(int(random.uniform(97, 122)))+tmp[midlen:]
            start = timer()
            A, CJ = n_gram_compare(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)





            # TEST 5:   1 CARATTERE SCAMBIATO CON IL
            #           VICINO DELLA TASTIERA QWERTY
            a = ['s', 'q', 'z']
            v = ['c', 'f', 'g', 'b']
            y = ['t', 'g', 'h', 'u']
            u = ['i', 'j', 'h', 'y']
            l = ['p', 'o', 'k']

            change = [a, v, y, u, l]
            tmp = ''

            # FUNZIONE SCAMBIACARATTERE
            tmp = changeCaracters(1, _parola[i][j], change);

            start = timer()
            A, CJ = n_gram_compare(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)



            # TEST 6:   2 CARATTERI SCAMBIATI CON I
            #           VICINI DELLA TASTIERA QWERTY
            tmp = ''

            # FUNZIONE SCAMBIACARATTERE
            tmp = changeCaracters(2, _parola[i][j], change);

            start = timer()
            A, CJ = n_gram_compare(path[i], tmp, k)
            end = timer()
            c[i][j][k].append(A)
            c[i][j][k].append(end - start)
            c[i][j][k].append(CJ)
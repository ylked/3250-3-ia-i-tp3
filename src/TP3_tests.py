import numpy as np

import TP3 as tp
import math

import matplotlib.pyplot as plt

LIMIT_SEC = 10
TARGET = math.pi
NB_GENES = 30
NB_INDIVIDUALS = 50


def get_fitness_values():
    return [tp.fitness(c, TARGET) for c in tp.data]


def reset():
    tp.CROSSOVER_METHOD = (tp.CrossoverMethod.EXCHANGE_X_PARTS, 4)
    tp.MUTATION_METHOD = {
        # the method
        'method': tp.MutationMethod.INVERT_ONE_BIT_OF_X_GENES,

        # the X parameter (referring to the x argument of the above method)
        'x': 5,

        # The probability a chromosome gets mutated
        'incidence_percent': 30
    }
    tp.SELECTION_METHOD = (tp.SelectionMethod.TOURNAMENT, True)


def test_mutation():
    reset()
    std_x = 5
    std_incid = 50
    std_method = tp.MutationMethod.INVERT_ONE_BIT_OF_X_GENES
    std_method_name = f'Inverser 1 bit de {std_x} gènes'

    methods = [
        (tp.MutationMethod.INVERT_ALL_BITS_OF_X_GENES, f'Inverser tous les bits de {std_x} gènes'),
        (tp.MutationMethod.INVERT_ONE_BIT_OF_X_GENES, f'Inverser un bit de {std_x} gènes'),
        (tp.MutationMethod.SCRAMBLE_ALL_BITS_OF_X_GENES, f'Mélanger tous les bits de {std_x} gènes'),
        (tp.MutationMethod.INVERT_X_BITS, f'Inverser {std_x} bits du chromosome')
    ]

    nb_genes = 20
    nb_ind = 50

    x_values = [1, 2, 5, 10]
    incid_values = [1, 10, 20, 50, 75, 90, 100]

    test_methods = []
    for m in methods:
        test_methods.append(({
                                 'method': m[0],
                                 'x': std_x,
                                 'incidence_percent': std_incid
                             }, m[1]))

    test_x = []
    for x in x_values:
        test_x.append({
            'method': std_method,
            'x': x,
            'incidence_percent': std_incid
        })

    test_incid = []
    for i in incid_values:
        test_incid.append({
            'method': std_method,
            'x': std_x,
            'incidence_percent': i
        })

    for m in test_methods:
        tp.MUTATION_METHOD = m[0]

        res = tp.run_ag(nb_ind, nb_genes, TARGET, LIMIT_SEC)

        assert tp.data is not None
        f_values = [tp.fitness(c, math.pi) for c in tp.data]
        plt.plot(f_values, label=m[1])

    plt.title("Evolution du fitness selon la méthode de mutation")
    plt.xlabel("nombre d'itérations")
    plt.ylabel("Valeur de fitness")
    plt.legend()
    plt.show()

    for x in test_x:
        tp.MUTATION_METHOD = x

        res = tp.run_ag(nb_ind, nb_genes, TARGET, LIMIT_SEC)

        f_values = [tp.fitness(c, TARGET) for c in tp.data]
        plt.plot(f_values, label=f'$x = {x["x"]}$')

    plt.title("Evolution du fitness selon le nombre de gènes mutés x")
    plt.xlabel("nombre d'itérations")
    plt.ylabel("Valeur de fitness")
    plt.legend()
    plt.show()

    for incid in test_incid:
        tp.MUTATION_METHOD = incid

        res = tp.run_ag(nb_ind, nb_genes, TARGET, LIMIT_SEC)

        f_values = [tp.fitness(c, TARGET) for c in tp.data]
        plt.plot(f_values, label=f'incidence de {incid["incidence_percent"]}%')

    plt.title("Evolution du fitness selon l'incidence de mutation")
    plt.xlabel("Nombre d'itérations")
    plt.ylabel("Valeur de fitness")
    plt.legend()
    plt.show()


def test_selection():
    reset()
    methods = (
        ((tp.SelectionMethod.UNIFORM, None), 'Sélection uniforme'),
        ((tp.SelectionMethod.RANK, None), 'Sélection par rang'),
        ((tp.SelectionMethod.TOURNAMENT, True), 'Sélection par tournois (élitiste)'),
        ((tp.SelectionMethod.TOURNAMENT, False), 'Sélection par tournois (non élitiste)'),
        ((tp.SelectionMethod.ROULETTE, True), 'Sélection par roulette (élitiste)'),
        ((tp.SelectionMethod.ROULETTE, False), 'Sélection par roulette (non-élitiste)'),
    )

    for m in methods:
        if m[1] is None:
            m[1] = True

        tp.SELECTION_METHOD = m[0]
        tp.run_ag(NB_INDIVIDUALS, NB_GENES, TARGET, LIMIT_SEC)
        result = get_fitness_values()

        plt.plot(result)
        plt.title(f"Evolution du fitness selon la méthode : {m[1]} ")
        plt.xlabel("Nombre d'itérations")
        plt.ylabel("Valeur de fitness")
        plt.show()


def test_crossover():
    reset()
    std_x = 4
    methods_0 = (
        ((tp.CrossoverMethod.EXCHANGE_X_PARTS, 4), f'Echange de 4 parties'),
        # ((tp.CrossoverMethod.EXCHANGE_EACH_X_GENE, 4), f'Echange tous les 4 gènes'),
        ((tp.CrossoverMethod.EXCHANGE_EACH_X_BIT, 2), f'Echange tous les 2 bits')
    )

    std_method = tp.CrossoverMethod.EXCHANGE_EACH_X_BIT
    methods_1 = (
        (1, 'Echange à chaque bit'),
        (2, 'Echange tous les deux bits'),
        (6, f'Echange de {NB_GENES // 6} parties'),
        (10, f'Echange de {NB_GENES // 10} parties')
    )

    for m in methods_0:
        tp.CROSSOVER_METHOD = m[0]
        tp.run_ag(NB_INDIVIDUALS, NB_GENES, TARGET, LIMIT_SEC)
        plt.plot(get_fitness_values(), label=m[1])

    plt.title("Evolution du fitness selon la méthode de croisement")
    plt.xlabel("Nombre d'itérations")
    plt.ylabel("Valeur de fitness")
    plt.legend()
    plt.show()

    for m in methods_1:
        tp.CROSSOVER_METHOD = (std_method, m[0])
        tp.run_ag(NB_INDIVIDUALS, NB_GENES, TARGET, LIMIT_SEC)
        plt.plot(get_fitness_values(), label=m[1])

    plt.title("Evolution du fitness selon le nombre de parties de chromosome croisées")
    plt.xlabel("Nombre d'itérations")
    plt.ylabel("Valeur de fitness")
    plt.legend()
    plt.show()


def test_nb_genes():
    reset()
    values = (8, 12, 20, 50, 100, 500, 1000)

    for v in values:
        tp.run_ag(NB_INDIVIDUALS, v, TARGET, LIMIT_SEC)
        l = f'{v} gènes'

        x = tp.data_time
        y = get_fitness_values()

        assert len(x) == len(y)
        plt.plot(x, y, label=l)

    plt.title("Evolution du fitness selon le nombre de gènes")
    plt.xlabel("Temps d'éxecution [s]")
    plt.ylabel("Valeur de fitness")
    plt.legend()
    plt.show()


def test_nb_individus():
    reset()
    values = (8, 12, 20, 50, 100, 500, 1000)

    for v in values:
        break
        tp.run_ag(v, NB_GENES, TARGET, LIMIT_SEC)
        l = f'{v} individus'

        x = tp.data_time
        y = get_fitness_values()

        assert len(x) == len(y)
        plt.plot(x, y, label=l)

    # plt.xlabel("Temps d'éxecution [s]")
    # plt.ylabel("Valeur de fitness")
    # plt.legend()
    # plt.show()

    values = (
        6,
        10,
        15,
        20,
        30,
        40,
        50,
        75,
        100,
        500,
        1000,
    )

    for i in range(3):
        x, y = [], []
        for v in values:
            r = tp.run_ag(v, NB_GENES, TARGET, LIMIT_SEC)

            f = tp.fitness(r[0], TARGET)

            x.append(v)
            y.append(f)

        plt.plot(x, y, 'o', label=f'test {i}')

    plt.title("Valeurs de fitness à la fin de l'AG selon la taille de la population")
    plt.xlabel("Nombre d'individus")
    plt.ylabel("Valeur de fitness")
    plt.legend()
    plt.show()

def test_final():
    nb_indiv = 100
    nb_genes = 50
    limit = 5
    tp.MUTATION_METHOD = {
        'method': tp.MutationMethod.INVERT_ONE_BIT_OF_X_GENES,
        'x': nb_genes//10,
        'incidence_percent': 30
    }
    tp.SELECTION_METHOD = (tp.SelectionMethod.TOURNAMENT, True)
    tp.CROSSOVER_METHOD = (tp.CrossoverMethod.EXCHANGE_X_PARTS, 4)

    targets = (math.pi, 39, -25.43, 15.5)
    global TARGET

    for t in targets:
        TARGET = t
        res = tp.run_ag(nb_indiv, nb_genes, t, limit)
        plt.plot(get_fitness_values(), label=f"cible = {t}")

    plt.title("Evolution du fitness de l'AG optimisé")
    plt.xlabel("Nombre d'itérations")
    plt.ylabel("Valeur de fitness")
    plt.legend()
    plt.show()

def test_final_high():
    nb_indiv = 100
    nb_genes = 50
    limit = 5
    tp.MUTATION_METHOD = {
        'method': tp.MutationMethod.INVERT_ONE_BIT_OF_X_GENES,
        'x': nb_genes//10,
        'incidence_percent': 30
    }
    tp.SELECTION_METHOD = (tp.SelectionMethod.TOURNAMENT, True)
    tp.CROSSOVER_METHOD = (tp.CrossoverMethod.EXCHANGE_X_PARTS, 4)

    global TARGET

    t = 20000
    TARGET = t
    res = tp.run_ag(nb_indiv, nb_genes, t, limit)
    plt.plot(get_fitness_values())
    plt.title("Evolution du fitness de l'AG optimisé pour la cible 20'000")
    plt.xlabel("Nombre d'itérations")
    plt.ylabel("Valeur de fitness")
    plt.show()

if __name__ == '__main__':
    #test_final_high()
    #exit(0)
    #test_final()
    test_mutation()
    test_selection()
    test_crossover()
    test_nb_genes()
    test_nb_individus()



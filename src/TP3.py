"""
TP3 - Le compte est bon
Nous souhaitons réaliser une IA basée sur les algorithmes génétiques permettant de résoudre le problème du compte est bon.
"""

import random
from enum import Enum
import textwrap


"""
***********************************************************************************************************
Commencez par implémenter les fonctions `decode` et `evaluate`, en reprenant les signatures ci-dessous.
***********************************************************************************************************
"""



lookup_genes = {
    "0000": "0",
    "0001": "1",
    "0010": "2",
    "0011": "3",
    "0100": "4",
    "0101": "5",
    "0110": "6",
    "0111": "7",
    "1000": "8",
    "1001": "9",
    "1010": "+",
    "1011": "-",
    "1100": "*",
    "1101": "/",
}

lookup_types = {
    "operators":
        [
            "1010",
            "1011",
            "1100",
            "1101",
        ],
    "numbers":
        [
            "0000",
            "0001",
            "0010",
            "0011",
            "0100",
            "0101",
            "0110",
            "0111",
            "1000",
            "1001",
        ]
}

class GeneType(Enum):
    OPERATOR = 1
    NUMBER = 2
    INVALID = 3

class CrossoverType(Enum):
    EXCHANGE_EACH_X_BIT = 1
    EXCHANGE_EACH_X_GENE = 2
    EXCHANGE_X_PARTS = 3
    EXCHANGE_X_PARTS_BETWEEN_GENES = 4

CROSSOVER_METHOD = (CrossoverType.EXCHANGE_X_PARTS, 4)

class MutationMethod(Enum):
    # mutates x random bits of the whole chromosome (switching value 0 <-> 1)
    INVERT_X_BITS = 1

    # mutates one random bit of X random genes (switching value 0 <-> 1)
    INVERT_ONE_BIT_OF_X_GENES = 2

    # mutates all the bits of X random genes
    INVERT_ALL_BITS_OF_X_GENES = 3

    # randomly scramble all the bits of X random genes
    SCRAMBLE_ALL_BITS_OF_X_GENES = 4


# default mutation method
MUTATION_METHOD = (MutationMethod.INVERT_ALL_BITS_OF_X_GENES, 1)

def switch_type(type: Enum):
    if(type == GeneType.OPERATOR):
        return GeneType.NUMBER
    if(type == GeneType.NUMBER):
        return GeneType.OPERATOR
    return GeneType.INVALID

def get_gene_type(gene: str):
    if(gene in lookup_types["operators"]):
        return GeneType.OPERATOR
    if(gene in lookup_types["numbers"]):
        return GeneType.NUMBER
    return GeneType.INVALID

def crossover_each_x_bit(chromosome_1, chromosome_2, n):
    chromosome_1 = list(chromosome_1)
    chromosome_2 = list(chromosome_2)
    c_1 = chromosome_1
    c_2 = chromosome_2
    if len(chromosome_2) < len(chromosome_1):
        c_1 = chromosome_2
        c_2 = chromosome_1

    step = n
    if CROSSOVER_METHOD[0] == CrossoverType.EXCHANGE_EACH_X_GENE:
        step = n * 4

    change = True
    for i in range(0, len(c_1), step):
        start = i - step
        end = i
        if change:
            c_1[start:end] = c_2[start:end]
        elif i+step >= len(c_1):
            c_1[end+1:] = c_2[end+1:len(c_1)]
        change = not change

    return "".join(c_1)

def crossover_x_part(chromosome_1, chromosome_2, n, between_genes):
    chromosome_1 = list(chromosome_1)
    chromosome_2 = list(chromosome_2)
    c_1 = chromosome_1
    c_2 = chromosome_2
    if len(chromosome_2) < len(chromosome_1):
        c_1 = chromosome_2
        c_2 = chromosome_1
    length_part = len(c_1) // n
    if(between_genes):
        nb_gene = len(c_1) // 4
        length_part = (nb_gene // n) * 4
    change = True
    for i in range(n):
        print(f"iter {i}")
        if(change):
            start = i * length_part
            end = start + length_part
            print(f"start: {start}")
            print(f"stop: {end}")

            if (i == n - 1):
                end = len(c_1)
            c_1[start:end] = c_2[start:end]
        change = not change

    return "".join(c_1)

def decode(chromosome: str) -> str:
    """Converts a chromosome into a human-readable sequence.
    example : the chromosome "011010100101110001001101001010100001" should give something like "6 + 5 * 4 / 2 + 1" as a result

    Args:
        chromosome (str): a string of "0" and "1" that represents a possible sequence of operators and digits

    Returns:
        str: a translated string from the input chromosome in an human-readable format
    """

    #initialisation
    genes = textwrap.wrap(chromosome, 4)
    result = ""
    expected_type = GeneType.NUMBER

    for gene in genes:
        type = get_gene_type(gene)
        # ignore if gene is invalid, or not of type expected
        if(len(gene) == 4 and gene in lookup_genes.keys() and type == expected_type):
            result += lookup_genes[gene]
            result += " "
            # update expected type
            expected_type = switch_type(expected_type)
    # if the last gene was an operator, ignore it
    if expected_type == GeneType.NUMBER:
        result = result[:-2]
    # remove last space
    result = result[:-1]
    return result


def evaluate(chromosome: str) -> float:
    """Returns the evaluation of a chromosome.
    example : the chromosome "011010100101110001001101001010100001" should return 23 as a result

    Args:
        chromosome (str): a string of "0" and "1" that encode a sequence of digits and operators

    Returns:
        float: the result of the sequence of digits and operators
    """

    def number(x:str):
        assert is_number(x)
        return int(x)
    def is_number(x):
        return x.isdigit() and 0 <= int(x) < 10

    def is_op(x):
        return x in operations

    def is_valid(x):
        return is_op(x) or is_number(x)

    operations = {
        '+' : lambda x,y : x+y,
        '-' : lambda x,y : x-y,
        '*' : lambda x,y : x*y,
        '/' : lambda x,y : x/y
    }

    op = None
    res = None

    for value in decode(chromosome).split():
        assert is_valid(value)

        if is_op(value):
            op = value

        elif is_number(value) and res is None:
            res = number(value)

        elif is_number(value) and res is not None:
            assert op is not None
            res = operations[op](res, number(value))

        elif is_op(value):
            op = value

        else:
            assert False

    return float(res)


"""
***********************************************************************************************************
Fonction de fitness:
    Implémentez votre fonction de fitness selon la signature ci-dessous.
    Plus la valeur de fitness est haute, "meilleur" doit être le chromosome pour atteindre le nombre cible.
    N'hésitez pas à essayer plusieurs fonctions de fitness et de les comparer.
***********************************************************************************************************
"""


def fitness(chromosome: str, target: float) -> float:
    """The better the chromosome is at giving the target result, the higher the fitness function should be.

    Args:
        chromosome (str): a string composed of "0" and "1" that represent a possible sequence
        target (float): the value which we are trying to reach

    Returns:
        float: The fitness value of the chromosome
    """

    # TODO : implement the function

    fitness_value = 0
    return fitness_value


"""
***********************************************************************************************************
Opérateurs de croisement, mutation et sélection
    Implémentez maintenant vos fonctions de croisement, de mutation et de sélection selon les signatures ci-dessous.
    N'hésitez pas à essayer plusieurs fonctions et à voir quelles combinaisons donnent les meilleurs résultats.
    Note: il est possible ici de changer les signatures prosposées.
***********************************************************************************************************
"""


def crossover(chromosome_1: str, chromosome_2: str) -> [str]:
    """Performs the crossover on 2 chromosomes

    Args:
        chromosome_1 (str): the first parent chromosome as a string of "0" and "1"
        chromosome_2 (str): the second parent chromosome as a string of "0" and "1"

    Returns:
        str: a list containing the childrens of the two parents as strings of "0" and "1"
    """
    match CROSSOVER_METHOD[0]:
        case CrossoverType.EXCHANGE_EACH_X_BIT:
            return crossover_each_x_bit(chromosome_1, chromosome_2,CROSSOVER_METHOD[1])
        case CrossoverType.EXCHANGE_EACH_X_GENE:
            return crossover_each_x_bit(chromosome_1, chromosome_2, CROSSOVER_METHOD[1] * 4)
        case CrossoverType.EXCHANGE_X_PARTS:
            return crossover_x_part(chromosome_1, chromosome_2, CROSSOVER_METHOD[1], False)
        case CrossoverType.EXCHANGE_X_PARTS_BETWEEN_GENES:
            return crossover_x_part(chromosome_1, chromosome_2, CROSSOVER_METHOD[1], True)

def population_crossover(population: [str]) -> [str]:
    """Performs the crossover over the entire population (or a subpart of it)

    Args:
        population (str]): a list of all the chromosomes in the parent population as strings of "0" and "1"

    Returns:
        [str]: a list of all the chromosomes of the children population as strings of "0" and "1"
    """

    # TODO : implement the function
    return population


def mutation(chromosome: str) -> str:
    """Mutates the chromosome

    Args:
        chromosome (str): the chromosome as a string of "0" and "1"

    Returns:
        str: the mutated chromosome as a string of "0" and "1"
    """

    # TODO : implement the function
    return chromosome


def selection(population: [str], scores: [float]) -> [str]:
    """Selects some chromosomes that will be transmited to the next generation

    Args:
        population ([str]): all of the curent generation
        scores ([float]): the fitness values of the chromosomes such that fitness(population[i]) = score[i]

    Returns:
        [str]: the chromosomes that have been selected to create the next generation
    """

    # TODO : implement the function
    return population


"""
***********************************************************************************************************
Initialisation de la population
    Vous pouvez utiliser la fonction suivante pour générer la population initiale. 
    Comme précédemment, n'hésitez pas à modifier les paramètres (surtout la taille de la population et le nombre de gènes!)
***********************************************************************************************************
"""


def pad(chromosome: str, length: int) -> str:
    """Pads the chromosome to 'length' symbols"""

    chromosome = "0" * (length - len(chromosome)) + chromosome
    return chromosome


def generate(nb_individuals: int, nb_genes: int) -> [str]:
    """Randomly generates the initial population

    Args:
        nb_individuals (int, optional): the number of chromosome we want to generate
        nb_genes (int, optional): the number of gene in a chromosome

    Returns:
        [str]: the first generation as a list of strings of "0" and "1"
    """

    try:
        population = random.sample(range(2 ** (4 * (nb_genes))), nb_individuals)
        population = [pad(bin(c)[2:], (4 * nb_genes)) for c in population]
    except OverflowError:
        pop_1 = generate(nb_individuals, nb_genes // 2)
        pop_2 = generate(nb_individuals, nb_genes - nb_genes // 2)
        population = [p1 + p2 for p1, p2 in zip(pop_1, pop_2)]

    return population


"""
***********************************************************************************************************
L'algorithme génétique
    Nous pouvons maintenant implémenter les étapes principales de l'algorithme génétique (n'hésitez pas à essayer différentes version).
***********************************************************************************************************
"""


def run_ag(nb_individuals: int, nb_genes: int, target: float, limit_sec: float) -> [str]:
    """Runs the genetic algorithm, and returns the best individual (and the last population)

    Args:
        nb_individuals (int): the size of the population
        nb_genes (int): the number of genes
        target (float): the target value for le compte est bon
        limit_sec (float): maximum number of seconds allowed, must return a solution before this limit!

    Returns:
        [str]: the last population, sorted by fitness value, descending: best fitness (highest) is 1st, i.e., the best solution
    """

    # initialization

    population = generate(nb_individuals, nb_genes)
    cond = True

    while cond:  # TODO: use limit_sec to stop the algorithm after a certain time
        # evaluation
        fitness_values = [fitness(chromosome, target) for chromosome in population]
        # selection :
        population = selection(population, fitness_values)
        # crossover
        population = population_crossover(population)
        # mutation
        population = [mutation(chromosome) for chromosome in population]

        # over ?
        # TODO : implement the condition to stop the genetic algorithm
        best_individual=None
        cond = False

    # TODO: sort population DESC (see docstring) before returning
    return population



if __name__ == "__main__":

    nb_individuals = 20
    nb_genes = 5
    target = 4.5
    sorted_population = run_ag(nb_individuals=nb_individuals, nb_genes=nb_genes, target=target, limit_sec=10)
    solution=sorted_population[0]

    # Nous pouvons maintenant regarder le meilleur individu:
    scores = [fitness(chromosome, target) for chromosome in sorted_population]
    print(f"***TARGET***: {target}")
    f=fitness(chromosome=solution, target=target)
    d=decode(chromosome=solution)
    e=evaluate(chromosome=solution)
    print(f"***BEST***:  fitness: {f:6.2f} (value={e})     decoded: {d}")

    # Ou l'intégralité de la population:
    for c in sorted_population:
        f=fitness(chromosome=c, target=target)
        d=decode(chromosome=c)
        e=evaluate(chromosome=c)
        print(f"fitness: {f:6.2f}  (value={e})  decoded: {d} ")

    # Tests et optimisation des hyper-paramètres
    # Maintenant que tout fonctionne, il faut s'assurer que les critères d'arrêts soient respectés et trouver des "bonnes" valeurs!
    # Testez différentes valeurs des paramètres, et créez un plot qui affiche un fitness (p. ex. du meilleur, moyenne) en fonction du nombre d'itérations.

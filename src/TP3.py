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

def decode(chromosome: str) -> str:
    """Converts a chromosome into a human-readable sequence.
    example : the chromosome "011010100101110001001101001010100001" should give something like "6 + 5 * 4 / 2 + 1" as a result

    Args:
        chromosome (str): a string of "0" and "1" that represents a possible sequence of operators and digits

    Returns:
        str: a translated string from the input chromosome in an human-readable format
    """

    genes = textwrap.wrap(chromosome, 4)
    result = ""
    expected_type = GeneType.NUMBER
    for gene in genes:
        type = get_gene_type(gene)
        print(type)
        if(len(gene) == 4 and gene in lookup_genes.keys() and type == expected_type):
            result += lookup_genes[gene]
            result += " "
            expected_type = switch_type(expected_type)
    if expected_type == GeneType.NUMBER:
        result = result[:-2]
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

    # TODO : implement the function

    return chromosome


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

    # TODO : implement the function
    return chromosome_1


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

    print(decode("0010001010101110101101110010"))

    # nb_individuals = 20
    # nb_genes = 5
    # target = 4.5
    # sorted_population = run_ag(nb_individuals=nb_individuals, nb_genes=nb_genes, target=target, limit_sec=10)
    # solution=sorted_population[0]
    #
    # # Nous pouvons maintenant regarder le meilleur individu:
    # scores = [fitness(chromosome, target) for chromosome in sorted_population]
    # print(f"***TARGET***: {target}")
    # f=fitness(chromosome=solution, target=target)
    # d=decode(chromosome=solution)
    # e=evaluate(chromosome=solution)
    # print(f"***BEST***:  fitness: {f:6.2f} (value={e})     decoded: {d}")
    #
    # # Ou l'intégralité de la population:
    # for c in sorted_population:
    #     f=fitness(chromosome=c, target=target)
    #     d=decode(chromosome=c)
    #     e=evaluate(chromosome=c)
    #     print(f"fitness: {f:6.2f}  (value={e})  decoded: {d} ")

    # Tests et optimisation des hyper-paramètres
    # Maintenant que tout fonctionne, il faut s'assurer que les critères d'arrêts soient respectés et trouver des "bonnes" valeurs!
    # Testez différentes valeurs des paramètres, et créez un plot qui affiche un fitness (p. ex. du meilleur, moyenne) en fonction du nombre d'itérations.

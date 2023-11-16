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

# lookup dict to get the values of the genes
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

# lookup dict to get the type of the genes
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


class CrossoverMethod(Enum):
    # each x bit, exchange the value of the bit from chromomose 1 with the one from chromosome 2
    EXCHANGE_EACH_X_BIT = 1

    # each x gene, exchange the value of the gene from chromomose 1 with the one from chromosome 2
    EXCHANGE_EACH_X_GENE = 2

    # divide the chromosomes in x parts, and exchange the value of the 2 chromosome every 2 parts
    EXCHANGE_X_PARTS = 3

    # divide the chromosome in x parts, but between the genes to keep them intact, and exchange the value of the
    # 2 chromosome every 2 parts
    EXCHANGE_X_PARTS_BETWEEN_GENES = 4


CROSSOVER_METHOD = (CrossoverMethod.EXCHANGE_X_PARTS, 4)


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

class SelectionMethod(Enum):
    # random uniform selection
    UNIFORM = 1

    # keep n best individuals
    RANK = 2

    # randomly selects pairs of individuals and keep the best of the two
    TOURNAMENT = 3

    # roulette wheel selection
    ROULETTE = 4


# selection method tuple
# 1. first element is the method
# 2. second element is elitist mode (true/false) to the keep best individual
SELECTION_METHOD = (SelectionMethod.RANK, True)


class FitnessMethod(Enum):
    # return the opposite (negative) of absolute value of the difference between the result of the chromosome
    # and the goal value
    DISTANCE_TO_VALUE = 1

    # return the opposite (negative) of absolute value of the difference between the result of the chromosome
    # and the goal value, substracted by the number of genes
    DISTANCE_TO_VALUE_MINUS_NB_OP = 2


FITNESS_METHOD = FitnessMethod.DISTANCE_TO_VALUE_MINUS_NB_OP


def decode(chromosome: str) -> str:
    """Converts a chromosome into a human-readable sequence.
    example : the chromosome "011010100101110001001101001010100001" should give something like "6 + 5 * 4 / 2 + 1"
    as a result

    Args:
        chromosome (str): a string of "0" and "1" that represents a possible sequence of operators and digits

    Returns:
        str: a translated string from the input chromosome in an human-readable format
    """

    def switch_type(gene_type: Enum):
        if gene_type == GeneType.OPERATOR:
            return GeneType.NUMBER
        if gene_type == GeneType.NUMBER:
            return GeneType.OPERATOR
        return GeneType.INVALID

    def get_gene_type(gene: str):
        if gene in lookup_types["operators"]:
            return GeneType.OPERATOR
        if gene in lookup_types["numbers"]:
            return GeneType.NUMBER
        return GeneType.INVALID

    # initialisation
    genes = textwrap.wrap(chromosome, 4)
    result = ""
    expected_type = GeneType.NUMBER

    for gene in genes:
        gene_type = get_gene_type(gene)
        # ignore if gene is invalid, or not of type expected
        if len(gene) == 4 and gene in lookup_genes.keys() and gene_type == expected_type:
            # add gene value to result
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

    def number(x: str):
        assert is_number(x)
        return int(x)

    def is_number(x):
        return x.isdigit() and 0 <= int(x) < 10

    def is_op(x):
        return x in operations

    def is_valid(x):
        return is_op(x) or is_number(x)

    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else 0
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

    def get_distance_to_value(chromosome: str, target: float):
        return - abs(target - evaluate(chromosome))

    def get_nb_op(chromosome: str):
        return len(chromosome) // 4

    match FITNESS_METHOD:
        case FitnessMethod.DISTANCE_TO_VALUE:
            return get_distance_to_value(chromosome, target)
        case FitnessMethod.DISTANCE_TO_VALUE_MINUS_NB_OP:
            return get_distance_to_value(chromosome, target) - get_nb_op(chromosome)


"""
***********************************************************************************************************
Opérateurs de croisement, mutation et sélection
    Implémentez maintenant vos fonctions de croisement, de mutation et de sélection selon les signatures ci-dessous.
    N'hésitez pas à essayer plusieurs fonctions et à voir quelles combinaisons donnent les meilleurs résultats.
    Note: il est possible ici de changer les signatures prosposées.
***********************************************************************************************************
"""

def crossover(chromosome_1: str, chromosome_2: str) -> [str]:

    def exchange_x_parts():
        s1, s2 = [], []
        size = len(chromosome_1)
        assert size % x == 0

        step = size // x

        for i in range(x):
            start, end = i * step, (i + 1) * step

            c1, c2 = (list(chromosome_1), list(chromosome_2)) \
                if i % 2 == 0 else \
                (list(chromosome_2), list(chromosome_1))

            s1.extend(c1[start:end])
            s2.extend(c2[start:end])

        assert len(s1) == size
        assert len(s2) == size
        return "".join(s1), "".join(s2)

    def exchange_each_x_genes():
        g1, g2 = [], []
        size = len(chromosome_1)

        assert size / 4 % x == 0

        genes1 = textwrap.wrap(chromosome_1, 4)
        genes2 = textwrap.wrap(chromosome_2, 4)

        n = len(genes1)
        assert n % x == 0
        step = x

        change = False
        for i in range(n // x):
            start, end = i * step, (i + 1) * step
            gene1, gene2 = (genes1[start:end], genes2[start:end]) if change else (genes2[start:end], genes1[start:end])

            g1.extend(gene1)
            g2.extend(gene2)

            change = not change

        assert len(g1) == len(chromosome_1)
        assert len(g2) == len(chromosome_2)
        return "".join(g1), "".join(g2)

    def exchange_each_x_bit():
        s1, s2 = [], []

        size = len(chromosome_1)

        change = True
        for i in range(size // x):
            start, end = i * x, (i + 1) * x

            c1, c2 = (chromosome_1, chromosome_2) if change else (chromosome_2, chromosome_1)

            s1.extend(c1[start:end])
            s2.extend(c2[start:end])

            change = not change

        assert len(s1) == len(chromosome_1)
        assert len(s2) == len(chromosome_2)

        return "".join(s1), "".join(s2)

    def exchange_x_parts_between_genes():
        pass

    method, x = CROSSOVER_METHOD

    # maybe to change...
    assert len(chromosome_1) == len(chromosome_2)

    match method:
        case CrossoverMethod.EXCHANGE_X_PARTS:
            return exchange_x_parts()

        case CrossoverMethod.EXCHANGE_EACH_X_GENE:
            return exchange_each_x_genes()

        case CrossoverMethod.EXCHANGE_EACH_X_BIT:
            return exchange_each_x_bit()

        case CrossoverMethod.EXCHANGE_X_PARTS_BETWEEN_GENES:
            exchange_x_parts_between_genes()

def crossover_(chromosome_1: str, chromosome_2: str) -> [str]:
    """Performs the crossover on 2 chromosomes

    Args:
        chromosome_1 (str): the first parent chromosome as a string of "0" and "1"
        chromosome_2 (str): the second parent chromosome as a string of "0" and "1"

    Returns:
        str: a list containing the childrens of the two parents as strings of "0" and "1"

    """

    def crossover_each_x_bit(chromosome_1: str, chromosome_2: str, x: int):
        """Performs the crossover on 2 chromosomes:
            each x bit, exchange the value of the bit from chromomose 1 with the one from chromosome 2

            Args:
                chromosome_1 (str): the first parent chromosome as a string of "0" and "1"
                chromosome_2 (str): the second parent chromosome as a string of "0" and "1"
                x (int): step between exchange for value

            Returns:
                str: a list containing the childrens of the two parents as strings of "0" and "1"

            """
        chromosome_1 = list(chromosome_1)
        chromosome_2 = list(chromosome_2)
        c_1 = chromosome_1
        c_2 = chromosome_2
        if len(chromosome_2) < len(chromosome_1):
            c_1 = chromosome_2
            c_2 = chromosome_1

        step = x
        if CROSSOVER_METHOD[0] == CrossoverMethod.EXCHANGE_EACH_X_GENE:
            step = x * 4

        change = True
        for i in range(0, len(c_1), step):
            start = i - step
            end = i
            if change:
                c_1[start:end] = c_2[start:end]
            elif i + step >= len(c_1):
                c_1[end + 1:] = c_2[end + 1:len(c_1)]
            change = not change

        return "".join(c_1)

    def crossover_x_part(chromosome_1: str, chromosome_2: str, x: int, between_genes: bool):
        """Performs the crossover on 2 chromosomes:
            # divide the chromosomes in x parts, and exchange the value of the 2 chromosome every 2 parts


            Args:
                chromosome_1 (str): the first parent chromosome as a string of "0" and "1"
                chromosome_2 (str): the second parent chromosome as a string of "0" and "1"
                x (int): step between exchange of value
                between_genes (bool): indicate if the division should be done between gene to keep them intact (True, to do it between genes, false otherwise)


            Returns:
                str: a list containing the childrens of the two parents as strings of "0" and "1"

            """
        chromosome_1 = list(chromosome_1)
        chromosome_2 = list(chromosome_2)
        c_1 = chromosome_1
        c_2 = chromosome_2
        if len(chromosome_2) < len(chromosome_1):
            c_1 = chromosome_2
            c_2 = chromosome_1
        length_part = len(c_1) // x
        if between_genes:
            nb_gene = len(c_1) // 4
            length_part = (nb_gene // x) * 4
        change = True
        for i in range(x):
            print(f"iter {i}")
            if change:
                start = i * length_part
                end = start + length_part
                print(f"start: {start}")
                print(f"stop: {end}")

                if i == x - 1:
                    end = len(c_1)
                c_1[start:end] = c_2[start:end]
            change = not change

        return "".join(c_1)

    match CROSSOVER_METHOD[0]:
        case CrossoverMethod.EXCHANGE_EACH_X_BIT:
            return crossover_each_x_bit(chromosome_1, chromosome_2, CROSSOVER_METHOD[1])
        case CrossoverMethod.EXCHANGE_EACH_X_GENE:
            return crossover_each_x_bit(chromosome_1, chromosome_2, CROSSOVER_METHOD[1] * 4)
        case CrossoverMethod.EXCHANGE_X_PARTS:
            return crossover_x_part(chromosome_1, chromosome_2, CROSSOVER_METHOD[1], False)
        case CrossoverMethod.EXCHANGE_X_PARTS_BETWEEN_GENES:
            return crossover_x_part(chromosome_1, chromosome_2, CROSSOVER_METHOD[1], True)


def population_crossover(population: [str]) -> [str]:
    """Performs the crossover over the entire population (or a subpart of it)

    Args:
        population (str]): a list of all the chromosomes in the parent population as strings of "0" and "1"

    Returns:
        [str]: a list of all the chromosomes of the children population as strings of "0" and "1"
    """

    output = []
    pop = population
    random.shuffle(pop)
    s = len(population)

    for i in range(len(pop)):
        c1 = pop[i % s]
        c2 = pop[(i+1) % s]
        output.extend(crossover(c1, c2))

    assert len(output) == 2*len(population)
    return output


def mutation(chromosome: str) -> str:
    """Mutates the chromosome

    Args:
        chromosome (str): the chromosome as a string of "0" and "1"

    Returns:
        str: the mutated chromosome as a string of "0" and "1"
    """

    def invert_bit(bit: str) -> str:
        assert bit in ['0', '1'], 'Invalid bit value'
        return '0' if bit == '1' else '1'

    def get_x_distinct_random_numbers(max_value: int, x: int) -> tuple:
        s = set()
        while len(s) < x:
            s.add(random.randint(0, max_value))
        return tuple(s)

    def invert_one_bit_of_x_genes(_chromosome: str, x: int):
        # split chromosome by genes
        genes = textwrap.wrap(_chromosome, 4)

        # randomly select the genes to be mutated
        genes_indices = get_x_distinct_random_numbers(len(genes) - 1, x)

        # mutate a random bit in the selected genes
        for i in genes_indices:
            # split string as list
            gene_as_list = list(genes[i])

            # select the random bit
            index = random.randint(0, 3)

            # mutate it
            gene_as_list[index] = invert_bit(gene_as_list[index])

            # join list as string
            mutated_gene = "".join(gene_as_list)

            # replace it in the list of genes
            genes[i] = mutated_gene

        return "".join(genes)

    def invert_x_bits(_chromosome: str, x: int):
        chromosome_as_list = list(_chromosome)

        # randomly select x distinct bits to be mutated
        bit_indices = get_x_distinct_random_numbers(len(_chromosome) - 1, x)

        # mutated the selected bits
        for i in bit_indices:
            chromosome_as_list[i] = invert_bit(chromosome_as_list[i])

        return "".join(chromosome_as_list)

    def invert_all_bits_of_x_genes(_chromosome: str, x: int):
        # split chromosome by genes
        genes = textwrap.wrap(_chromosome, 4)

        genes_indices = get_x_distinct_random_numbers(len(genes) - 1, x)
        print(genes_indices, x)

        # mutate all the bits in the selected genes
        for i in genes_indices:
            # split gene string as list
            gene_as_list = list(genes[i])
            print(gene_as_list)

            # mutate all the bits
            for j in range(4):
                gene_as_list[j] = invert_bit(gene_as_list[j])

            # join gene list as string
            mutated_gene = "".join(gene_as_list)

            # replace it in the list of genes
            genes[i] = mutated_gene

        return "".join(genes)

    def scramble_all_bits_of_x_genes(_chromosome: str, x: int):
        # split chromosome by genes
        genes = textwrap.wrap(_chromosome, 4)

        # randomly select the genes to be scrambled
        gene_indices = get_x_distinct_random_numbers(len(genes) - 1, x)

        for i in gene_indices:
            # split string as list
            gene_as_list = list(genes[i])

            # scramble the gene
            random.shuffle(gene_as_list)

            # replace the gene in the list
            genes[i] = "".join(gene_as_list)

        return "".join(genes)

    method, value = MUTATION_METHOD

    match method:
        case MutationMethod.INVERT_X_BITS:
            return invert_x_bits(chromosome, value)

        case MutationMethod.INVERT_ONE_BIT_OF_X_GENES:
            return invert_one_bit_of_x_genes(chromosome, value)

        case MutationMethod.INVERT_ALL_BITS_OF_X_GENES:
            return invert_all_bits_of_x_genes(chromosome, value)

        case MutationMethod.SCRAMBLE_ALL_BITS_OF_X_GENES:
            return scramble_all_bits_of_x_genes(chromosome, value)

        case _:
            assert False, 'Mutation not implemented yet'


def selection(population: [str], scores: [float]) -> [str]:
    """Selects some chromosomes that will be transmited to the next generation

    Args:
        population ([str]): all of the curent generation
        scores ([float]): the fitness values of the chromosomes such that fitness(population[i]) = score[i]

    Returns:
        [str]: the chromosomes that have been selected to create the next generation
    """

    def uniform_selection():
        next_gen: list = population

        random.shuffle(next_gen)
        next_gen = next_gen[:len(population) // 2]

        if elitist:
            best = sorted_population[0]
            print(best)
            if best not in next_gen:
                next_gen[0] = best

        return next_gen

    def rank_selection():
        return sorted_population[:len(population) // 2]

    def tournament_selection():
        next_gen = []
        lookup_scores = {}
        for i in range(len(population)):
            lookup_scores[population[i]] = scores[i]

        pairs = []
        pool:list = population

        while len(pool) >= 2:
            c1 = random.choice(pool)
            pool.remove(c1)

            c2 = random.choice(pool)
            pool.remove(c2)

            pairs.append((c1, c2))

        for c1, c2 in pairs:
            score1, score2 = lookup_scores[c1], lookup_scores[c2]
            next_gen.append(c1 if score1 > score2 else c2)

        return next_gen

    def roulette_selection():
        s = set()

        if elitist:
            s.add(sorted_population[0])

        while len(s) < len(population) // 2:
            # we need to add an offset to the scores because they are negatives and
            # the random.choices does not like it...
            s.add(random.choices(population, weights=[x - min(scores) + 1 for x in scores])[0])
        return list(s)

    method, elitist = SELECTION_METHOD

    sorted_population = [p for _, p in sorted(zip(scores, population), reverse=True)]

    match method:
        case SelectionMethod.UNIFORM:
            return uniform_selection()

        case SelectionMethod.RANK:
            return rank_selection()

        case SelectionMethod.TOURNAMENT:
            return tournament_selection()

        case SelectionMethod.ROULETTE:
            return roulette_selection()

        case _:
            raise Exception('Chosen selection method has not been implemented yet')

"""
***********************************************************************************************************
Initialisation de la population
    Vous pouvez utiliser la fonction suivante pour générer la population initiale. 
    Comme précédemment, n'hésitez pas à modifier les paramètres (surtout la taille de la population et le nombre
    de gènes!)
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
        population = random.sample(range(2 ** (4 * nb_genes)), nb_individuals)
        population = [pad(bin(c)[2:], (4 * nb_genes)) for c in population]
    except OverflowError:
        pop_1 = generate(nb_individuals, nb_genes // 2)
        pop_2 = generate(nb_individuals, nb_genes - nb_genes // 2)
        population = [p1 + p2 for p1, p2 in zip(pop_1, pop_2)]

    return population


"""
***********************************************************************************************************
L'algorithme génétique
    Nous pouvons maintenant implémenter les étapes principales de l'algorithme génétique (n'hésitez pas à essayer
    différentes version).
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
        [str]: the last population, sorted by fitness value, descending: best fitness (highest) is 1st, i.e., the
        best solution
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
        best_individual = None
        cond = False

    # TODO: sort population DESC (see docstring) before returning
    return population


if __name__ == "__main__":

    nb_individuals = 20
    nb_genes = 5
    target = 4.5
    sorted_population = run_ag(nb_individuals=nb_individuals, nb_genes=nb_genes, target=target, limit_sec=10)
    solution = sorted_population[0]

    # Nous pouvons maintenant regarder le meilleur individu:
    scores = [fitness(chromosome, target) for chromosome in sorted_population]
    print(f"***TARGET***: {target}")
    f = fitness(chromosome=solution, target=target)
    d = decode(chromosome=solution)
    e = evaluate(chromosome=solution)
    print(f"***BEST***:  fitness: {f:6.2f} (value={e})     decoded: {d}")

    # Ou l'intégralité de la population:
    for c in sorted_population:
        f = fitness(chromosome=c, target=target)
        d = decode(chromosome=c)
        e = evaluate(chromosome=c)
        print(f"fitness: {f:6.2f}  (value={e})  decoded: {d} ")

    # Tests et optimisation des hyper-paramètres
    # Maintenant que tout fonctionne, il faut s'assurer que les critères d'arrêts soient respectés et trouver des
    # "bonnes" valeurs!
    # Testez différentes valeurs des paramètres, et créez un plot qui affiche un fitness (p. ex. du meilleur, moyenne)
    # en fonction du nombre d'itérations.

"""
TP3 - Le compte est bon
Nous souhaitons réaliser une IA basée sur les algorithmes génétiques permettant de résoudre le problème du compte est bon.
"""
import math
import random
import textwrap
from datetime import datetime as dt
from enum import Enum

# these variables are updated during run_ag with fitness values
# and are used for making plots in test script
global data
data = None
data_time = None

# release mode for forcing default parameters
RELEASE = True

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

# lookup dict to get the type of the genes (number or operator)
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
    """
    Enumeration of the different gene types that can exist
    """

    OPERATOR = 1
    NUMBER = 2
    INVALID = 3


class CrossoverMethod(Enum):
    """
    Enumeration of the different implemented crossover methods
    """

    # each x bit, exchange the value of the bit from chromomose 1 with the one from chromosome 2
    EXCHANGE_EACH_X_BIT = 1

    # each x gene, exchange the value of the gene from chromomose 1 with the one from chromosome 2
    EXCHANGE_EACH_X_GENE = 2

    # divide the chromosomes in x parts, and exchange the value of the 2 chromosome every 2 parts
    EXCHANGE_X_PARTS = 3

    # divide the chromosome in x parts, but between the genes to keep them intact, and exchange the value of the
    # 2 chromosome every 2 parts
    EXCHANGE_X_PARTS_BETWEEN_GENES = 4


# The default crossover method the AG should use
CROSSOVER_METHOD = (CrossoverMethod.EXCHANGE_X_PARTS, 4)


class MutationMethod(Enum):
    """
    Enumeration of the different implemented mutation methods
    """

    # mutates x random bits of the whole chromosome (switching value 0 <-> 1)
    INVERT_X_BITS = 1

    # mutates one random bit of X random genes (switching value 0 <-> 1)
    INVERT_ONE_BIT_OF_X_GENES = 2

    # mutates all the bits of X random genes
    INVERT_ALL_BITS_OF_X_GENES = 3

    # randomly scramble all the bits of X random genes
    SCRAMBLE_ALL_BITS_OF_X_GENES = 4


# The default mutation method the AG should use
MUTATION_METHOD = {
    # the method
    'method': MutationMethod.INVERT_ONE_BIT_OF_X_GENES,

    # the X parameter (referring to the x argument of the above method)
    'x': 5,

    # The probability a chromosome gets mutated
    'incidence_percent': 50
}


class SelectionMethod(Enum):
    """
    Enumeration of the different implemented selection methods
    """

    # random uniform selection
    UNIFORM = 1

    # keep n best individuals
    RANK = 2

    # randomly selects pairs of individuals and keep the best of the two
    TOURNAMENT = 3

    # roulette wheel selection
    ROULETTE = 4


# The default selection method the AG should use
# 1. first element is the method
# 2. second element is elitist mode (true/false) to always keep the best individual
SELECTION_METHOD = (SelectionMethod.TOURNAMENT, True)


def decode(chromosome: str) -> str:
    """
    Converts a chromosome into a human-readable sequence.
    example : the chromosome "011010100101110001001101001010100001" should give something like "6 + 5 * 4 / 2 + 1"
    as a result

    Args:
        chromosome (str): a string of "0" and "1" that represents a possible sequence of operators and digits

    Returns:
        str: a translated string from the input chromosome in an human-readable format
    """

    def switch_type(gene_type: GeneType) -> GeneType:
        """
        Switch the type of the given gene type enumerator
        Args:
            gene_type (GeneType): The gene type enumerator

        Returns:
            GeneType: NUMBER if gene is OPERATOR and vice versa. If invalid, stays invalid.
        """

        match gene_type:
            case GeneType.OPERATOR:
                return GeneType.NUMBER

            case GeneType.NUMBER:
                return GeneType.OPERATOR

            case _:
                return GeneType.INVALID

    def get_gene_type(_gene: str):
        """
        Get the type of given gene (OPERATOR, NUMBER or INVALID)

        Args:
            _gene(str): The gene to evaluate

        Returns:
            GeneType: The type of the given gene
        """

        if _gene in lookup_types["operators"]:
            return GeneType.OPERATOR

        if _gene in lookup_types["numbers"]:
            return GeneType.NUMBER

        return GeneType.INVALID

    # initialisation
    genes = textwrap.wrap(chromosome, 4)
    result = ""
    expected_type = GeneType.NUMBER

    for gene in genes:
        gene_type = get_gene_type(gene)

        # ignore division by zero
        if gene in lookup_genes.keys():
            if len(result) > 2 and result[-2] == "/" and lookup_genes[gene] == "0":
                result = result[:-2]
                expected_type = switch_type(expected_type)
                continue

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
    """
    Returns the evaluation of a chromosome.

    example : the chromosome "011010100101110001001101001010100001" should return 23 as a result

    Args:
        chromosome (str): a string of "0" and "1" that encode a sequence of digits and operators

    Returns:
        float: the result of the sequence of digits and operators
    """

    def number(x: str):
        """
        Return the integer value of a string. The string must contain a valid number between 0 and 9,
        otherwise it will fail.

        Args:
            x(str): The number as string

        Returns:
            int: the value of the number

        """

        assert is_number(x)
        return int(x)

    def is_number(x):
        """
        Determines whether the given string is a valid number between 0 and 9 or not.

        Args:
            x(str): The string to evaluate

        Returns:
            bool: True if the number is valid, false if not

        """

        return x.isdigit() and 0 <= int(x) < 10

    def is_op(x):
        """
        Determines whether the given string is a valid operator or not.

        Args:
            x(str): The string to evaluate

        Returns: True if the string is a valid operator, false if not

        """
        return x in operations

    def is_valid(x):
        """
        Determines whether the given string is a valid symbol, i.e. if it is a number or an operator.

        Args:
            x(str): The string to evaluate

        Returns: True if the symbol is valid, false if not

        """
        return is_op(x) or is_number(x)

    # Mapping of the operator symbols to a function calculating the appropriate result
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else float('nan')
    }

    # This variable will contain the operator between two numbers
    op = None

    # This variable will contain the intermediate result
    res = None

    # looping over all the decoded symbols of the chromosome
    # Assumptions about decoding function:
    #   1. Each symbol is separated from the others by a single space
    #   2. The function only returns valid symbols sequences
    for value in decode(chromosome).split():
        # checking the above assumption (no. 2)
        assert is_valid(value)

        if is_op(value):
            op = value

        # If we encounter the first number (should be first symbol),
        # We set the intermediate result to the value of the current number
        elif is_number(value) and res is None:
            res = number(value)

        # Otherwise, if the number is not the first one,
        # we calculate the next intermediate result by doing :
        # intermediate_result OP current_numner
        # OP is +, -, * or /
        elif is_number(value) and res is not None:
            assert op is not None
            res = operations[op](res, number(value))

        elif is_op(value):
            op = value

        # If symbol is neither a number nor an operator, it is invalid or unknown
        else:
            raise Exception('Unknown or invalid gene type')

    return float(res) if res is not None else -1000


"""
***********************************************************************************************************
Fonction de fitness:
    Implémentez votre fonction de fitness selon la signature ci-dessous.
    Plus la valeur de fitness est haute, "meilleur" doit être le chromosome pour atteindre le nombre cible.
    N'hésitez pas à essayer plusieurs fonctions de fitness et de les comparer.
***********************************************************************************************************
"""


def fitness(chromosome: str, target: float) -> float:
    """
    Calculates a *fitness value* of a given chromosome.

    The better the chromosome is at giving the target result, the higher the fitness function should be.

    Args:
        chromosome (str): a string composed of "0" and "1" that represent a possible sequence
        target (float): the value which we are trying to reach

    Returns:
        float: The fitness value of the chromosome
    """

    return - abs(target - evaluate(chromosome))


"""
***********************************************************************************************************
Opérateurs de croisement, mutation et sélection
    Implémentez maintenant vos fonctions de croisement, de mutation et de sélection selon les signatures ci-dessous.
    N'hésitez pas à essayer plusieurs fonctions et à voir quelles combinaisons donnent les meilleurs résultats.
    Note: il est possible ici de changer les signatures prosposées.
***********************************************************************************************************
"""


def crossover(chromosome_1: str, chromosome_2: str) -> tuple[str, str]:
    """
    Crossover the two given chromosomes and return their **two** children.

    The way the chromosomes are reproduced can be configured by editing the CROSSOVER_METHOD tuple global variable.

    Args:
        chromosome_1(str): The first parent chromosome as a string of 0 and 1
        chromosome_2(str): The second parent chromosome as string a string of 0 and 1

    Returns:
        (str, str) : The two children of the given parents

    Note:
        The two given parent chromosomes **must have the same length**!
    """

    def exchange_x_parts():
        """
        Crossover method that exchanges X parts between the two parents.


        For example, if X=2, the first child
        will get the first half of the first parent and the second half of the second parent.
        If X=4, the first child will get the first quarter of the first parent, the second quarter of the second
        parent, the third quarter of the first parent and so on.

        Returns:
             (str, str) : The two children of the given parents

        Note:
            The chromosome **must** be equally divisible by X

        """

        child1, child2 = [], []
        size = len(chromosome_1)

        # check that we can equally divide the chromosome by X
        assert size % x == 0

        # number of elements between two parts, depending on the give part size X
        step = size // x

        for i in range(x):
            # Calculates the start and end indices of the parent chromome to give to the children
            start, end = i * step, (i + 1) * step

            # Select the appropriate parent to give the gene part
            # This permits to alternate between the two parents
            giver1, giver2 = (list(chromosome_1), list(chromosome_2)) \
                if i % 2 == 0 else \
                (list(chromosome_2), list(chromosome_1))

            child1.extend(giver1[start:end])
            child2.extend(giver2[start:end])

        # Check that the children have the same size as the parents
        assert len(child1) == size
        assert len(child2) == size

        return "".join(child1), "".join(child2)

    def exchange_each_x_genes():
        """
        Performs a crossover operation between two chromosomes by exchanging each block of 'x' genes.

        The method takes two parent chromosomes, divides them into blocks of 'x' genes,
        and then alternates these blocks between the two parent chromosomes to create two new child chromosomes.

        (*This docstring documentation has been partially generated by chatGPT*)

        Returns:
            (str, str): A tuple containing the two child chromosomes resulting from the crossover.

        Note:
            This method assumes that the length of each chromosome is divisible by the length of a gene block ('4 * x').
        """

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
        """
        Performs a crossover operation between two chromosomes by exchanging each block of x bits.

        This method alternates blocks of 'x' bits between two parent chromosomes to create two new child chromosomes.
        It operates by iterating over the chromosomes and swapping blocks of bits of size 'x' from one parent
        to the other, and vice versa.

        (*This docstring documentation has been partially generated by chatGPT*)

        Returns:
            (str, str): A tuple containing the two child chromosomes resulting from the crossover.

        Note:
            This method assumes that the length of each chromosome is divisible by 'x', the block size of bits.

        """

        child1, child2 = [], []

        size = len(chromosome_1)

        change = True
        for i in range(size // x):
            start, end = i * x, (i + 1) * x

            giver1, giver2 = (chromosome_1, chromosome_2) if change else (chromosome_2, chromosome_1)

            child1.extend(giver1[start:end])
            child2.extend(giver2[start:end])

            change = not change

        # check that the children have the same size as the parents
        assert len(child1) == len(chromosome_1)
        assert len(child2) == len(chromosome_2)

        return "".join(child1), "".join(child2)

    method, x = CROSSOVER_METHOD

    assert len(chromosome_1) == len(chromosome_2)

    match method:
        case CrossoverMethod.EXCHANGE_X_PARTS:
            return exchange_x_parts()

        case CrossoverMethod.EXCHANGE_EACH_X_GENE:
            return exchange_each_x_genes()

        case CrossoverMethod.EXCHANGE_EACH_X_BIT:
            return exchange_each_x_bit()


def population_crossover(population: [str]) -> [str]:
    """
    Performs the crossover over the entire population (or a subpart of it)

    Args:
        population (str]): a list of all the chromosomes in the parent population as strings of "0" and "1"

    Returns:
        [str]: a list of all the chromosomes of the children population as strings of "0" and "1"
    """

    # list containing the generated population
    output = []

    # make a copy of the population
    pop = population.copy()

    # shuffle the population
    random.shuffle(pop)

    s = len(population)

    # Creates the next generation by making chromosome 'i' reproduce with chromosome 'i+1'
    for i in range(len(pop)):
        c1 = pop[i % s]
        c2 = pop[(i + 1) % s]
        output.extend(crossover(c1, c2))

    # check that the next generation is twice as big
    assert len(output) == 2 * len(population)

    return output


def mutation(chromosome: str) -> str:
    """
    Mutates the chromosome.

    The way the chromosome mutates can be configured by editing MUTATION_METHOD dictionary global variable.
    Make sure that this function has accessed to the global variable.

    Args:
        chromosome (str): the chromosome as a string of "0" and "1"

    Returns:
        str: the mutated chromosome as a string of "0" and "1"
    """

    def invert_bit(bit: str) -> str:
        """
        Utility function that inverts bit, given as one character string.

        Args:
            bit(str): The bit to invert. Must be either '0' or '1'

        Returns:
            str: The inverted bit. If input was '1', the output will be '0' and vice versa

        """
        assert bit in ['0', '1'], 'Invalid bit value'
        return '0' if bit == '1' else '1'

    def get_x_distinct_random_numbers(max_value: int, x: int) -> tuple:
        """
        Utility function that returns the given number of distinct random integers. Each number is
        greater that 0 and less than the given max value.

        Note:
            Since the number must be distinct, the max value **must** be greater or equal than the number
            of integers to generate. Otherwise, there are not enough existing numbers :(

        Args:
            max_value(int): The biggest integer that can be generated (inclusive)
            x(int): The number of distinct random integers to generate.

        Returns:
            tuple: A tuple containing the generated integers

        """
        assert max_value >= x

        s = set()
        while len(s) < x:
            s.add(random.randint(0, max_value))
        return tuple(s)

    def chromosome_mutates():
        """
        Utility function that randomly determines whether the current chromosome must mutate or not,
        by using the incidence parameter.

        Note:
            the incidence is defined in the outer function and must represent the percentage of chance
            that the chromosome will mutate. E.g. if incidence=23, it means that there is 23% chance it will.

        Returns:
            bool: True if the chromosome must mutate, False if not

        """
        return random.random() * 100 < incidence

    def invert_one_bit_of_x_genes():
        """
        Mutation method that randomly invert exactly 1 bit on X distinct random genes.

        Returns:
            str: The mutated chromosome

        """

        # split chromosome by genes
        genes = textwrap.wrap(chromosome, 4)

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

    def invert_x_bits():
        """
        Mutation method that randomly inverts exactly X distinct bits of the chromosome.

        Returns:
            str: The mutated chromosome

        """

        chromosome_as_list = list(chromosome)

        # randomly select x distinct bits to be mutated
        bit_indices = get_x_distinct_random_numbers(len(chromosome) - 1, x)

        # mutated the selected bits
        for i in bit_indices:
            chromosome_as_list[i] = invert_bit(chromosome_as_list[i])

        return "".join(chromosome_as_list)

    def invert_all_bits_of_x_genes():
        """
        Mutation method that inverts all the bits of exactly X distinct random genes.

        Returns:
            str: The mutated chromosome

        """
        # split chromosome by genes
        genes = textwrap.wrap(chromosome, 4)

        genes_indices = get_x_distinct_random_numbers(len(genes) - 1, x)

        # mutate all the bits in the selected genes
        for i in genes_indices:
            # split gene string as list
            gene_as_list = list(genes[i])

            # mutate all the bits
            for j in range(4):
                gene_as_list[j] = invert_bit(gene_as_list[j])

            # join gene list as string
            mutated_gene = "".join(gene_as_list)

            # replace it in the list of genes
            genes[i] = mutated_gene

        return "".join(genes)

    def scramble_all_bits_of_x_genes():
        """
        Mutation method that randomly scrambles all bits of exactly X distinct random genes.

        For each gene that mutates, the value of the bits does not change but their order in the gene does.

        Returns:
            str: The mutated chromosome
        """

        # split chromosome by genes
        genes = textwrap.wrap(chromosome, 4)

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

    method = MUTATION_METHOD['method']
    x = MUTATION_METHOD['x']
    incidence = MUTATION_METHOD['incidence_percent']

    # determining whether the chromosome must mutate
    if chromosome_mutates():

        # select the appropriate method depending on the configuration variable
        match method:
            case MutationMethod.INVERT_X_BITS:
                return invert_x_bits()

            case MutationMethod.INVERT_ONE_BIT_OF_X_GENES:
                return invert_one_bit_of_x_genes()

            case MutationMethod.INVERT_ALL_BITS_OF_X_GENES:
                return invert_all_bits_of_x_genes()

            case MutationMethod.SCRAMBLE_ALL_BITS_OF_X_GENES:
                return scramble_all_bits_of_x_genes()

            case other:
                raise Exception(f'Mutation {other} is not yet implemented or is invalid')

    # If the chromosome does not mutate, we return it as is.
    else:
        return chromosome


def selection(population: [str], scores: [float]) -> [str]:
    """
    Selects some chromosomes that will be transmitted to the next generation.

    The size of the next generation is exactly the half of the current.

    Args:
        population ([str]): the current generation
        scores ([float]): the fitness values of the chromosomes such that fitness(population[i]) = score[i]

    Returns:
        [str]: the chromosomes that have been selected to create the next generation
    """

    def uniform_selection():
        """
        Uniformly and randomly select the population to constitute the next generation.

        Returns:
            [str]: The next generation.

        """
        next_gen: list = population

        random.shuffle(next_gen)
        next_gen = next_gen[:len(population) // 2]

        if elitist:
            best = _sorted_population[0]
            if best not in next_gen:
                next_gen[0] = best

        return next_gen

    def rank_selection():
        """
        Select the best half of the population.
        Returns:
            [str]: The next generation.

        """
        return _sorted_population[:len(population) // 2]

    def tournament_selection():
        """
        Select the population by making a tournament. We randomly make as many chromosome pairs as possible and
        select the one that has the best fitness value.

        Returns:
            [str]: The next generation.

        """
        next_gen = []

        # Since we will shuffle the population, it is easier to make a dictionary
        # to find the fitness values of each chromosome
        lookup_scores = {}
        for i in range(len(population)):
            lookup_scores[population[i]] = scores[i]

        pairs = []
        pool: list = population

        random.shuffle(pool)

        # make the pairs
        for i in range(0, len(pool)-1, 2):
            c1 = pool[i]
            c2 = pool[i + 1]
            pairs.append((c1, c2))

        # make them fight and keep the best
        for c1, c2 in pairs:
            score1, score2 = lookup_scores[c1], lookup_scores[c2]
            next_gen.append(c1 if score1 > score2 else c2)

        return next_gen

    def roulette_selection():
        """
        Roulette selection method to make the next generation.
        Each chromosome has a probability to be selected that is proportional to its fitness value.

        Returns:
            [str]: The next generation.

        """

        # Scores of the chromosome, offset to be strictly positive
        w = [x - min(scores) + 1 for x in scores]

        # Randomly select the indices of the chromosome to select, based on their scores
        indices = random.choices(range(len(population)), weights=w, k=len(population) // 2)

        # Generate the list containing the selected population
        next_gen = [population[i] for i in indices]

        # check that the best chromosome has been kept (if appropriate)
        best = _sorted_population[0]
        if elitist and best not in next_gen:
            next_gen.append(best)

        return [population[i] for i in indices]

    method, elitist = SELECTION_METHOD

    # sort the population by descending fitness value. Useful for some selection methods.
    _sorted_population = [p for _, p in sorted(zip(scores, population), reverse=True)]

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

    if RELEASE:
        global MUTATION_METHOD, SELECTION_METHOD, CROSSOVER_METHOD
        MUTATION_METHOD = {
            'method': MutationMethod.INVERT_ONE_BIT_OF_X_GENES,
            'x': nb_genes // 10,
            'incidence_percent': 30
        }
        SELECTION_METHOD = (SelectionMethod.TOURNAMENT, True)
        CROSSOVER_METHOD = (CrossoverMethod.EXCHANGE_X_PARTS, 4)

    def is_time_left():
        """
        This methods determines whether there is still time left to make another iteration or not.

        It is doing so by reading the time that was necessary to perform the last iteration, multiplying by 2
        (just to be sure) and adding it to the current time. If the result is greater than the allowed time,
        it returns false.

        Returns:
            True if there is enough time for another iteration, False if not.

        """
        return (dt.now() - interval_start).total_seconds() * 2 + (dt.now() - start).total_seconds() < limit_sec

    # initialization

    population = generate(nb_individuals, nb_genes)
    global data
    global data_time
    data = []
    data_time = []

    start = dt.now()
    interval_start = dt.now()

    while is_time_left():
        interval_start = dt.now()

        # evaluation
        fitness_values = [fitness(chromosome, target) for chromosome in population]
        # selection :
        population = selection(population, fitness_values)
        # crossover
        population = population_crossover(population)
        # mutation
        population = [mutation(chromosome) for chromosome in population]

        best = sorted(population, key=lambda x: fitness(x, target), reverse=True)[0]
        data.append(best)
        data_time.append((dt.now() - start).total_seconds())

    _p = sorted(population, key=lambda x: fitness(x, target), reverse=True)

    return _p


if __name__ == "__main__":

    NB_INDIVIDUALS = 200
    NB_GENES = 100
    TARGET = math.pi
    LIMIT = 5

    MUTATION_METHOD = {
        'method': MutationMethod.INVERT_ONE_BIT_OF_X_GENES,
        'x': NB_GENES // 10,
        'incidence_percent': 30
    }

    SELECTION_METHOD = (SelectionMethod.TOURNAMENT, True)
    CROSSOVER_METHOD = (CrossoverMethod.EXCHANGE_X_PARTS, 4)

    print(f"searching solution for target={TARGET} in {LIMIT} seconds...")

    sorted_population = run_ag(nb_individuals=NB_INDIVIDUALS, nb_genes=NB_GENES, target=TARGET, limit_sec=LIMIT)
    solution = sorted_population[0]

    # Nous pouvons maintenant regarder le meilleur individu:
    scores = [fitness(chromosome, TARGET) for chromosome in sorted_population]
    print(f"***TARGET***: {TARGET}")
    f = fitness(chromosome=solution, target=TARGET)
    d = decode(chromosome=solution)
    e = evaluate(chromosome=solution)
    print(f"***BEST***:  fitness: {f:6.2f} (value={e})     decoded: {d}")

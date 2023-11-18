---
subtitle: 3250.3 Intelligence artificielle I
title: Travail pratique 3 - Le Compte Est Bon
author: Nima Dekhli \& Maëlys Bühler
date: Le \today
lang: fr-CH
geometry: 
  - margin=2cm
  - includehead
  - includefoot
papersize: a4
colorlinks: true
linkcolor: blue
citecolor: MidnightBlue
urlcolor: MidnightBlue
numbersections: true
links-as-notes: true

lofTitle: Liste des figures
lolTitle: Liste des codes
listingTitle: Code
lstPrefix: 
  - code
  - codes

toc: false
toc-depth: 4
header-includes: |
    \usepackage{fancyhdr}
    \pagestyle{fancy}\usepackage{float}
    \let\origfigure=\figure
    \let\endorigfigure=\endfigure
    \renewenvironment{figure}[1][]{%
      \origfigure[H]
    }{%
      \endorigfigure
    }

---

# Introduction
De nos jours, l'intelligence artificielle est un domaine très recherché et en pleine extension. En effet, elle est utilisée dans de nombreux domaines tels que la médecine, la finance, la robotique, etc. Dans ce travail pratique, nous allons nous intéresser à un jeu de calcul mental, le compte est bon. Ce jeu consiste à trouver une expression mathématique en manipulant des 10 digits (0,1,2,3,4,5,6,7,8,9) et en leur appliquant des opérations de base (+,-,*,/) pour atteindre un nombre cible. Pour cela, nous allons utiliser un algorithme génétique. Ce dernier est un algorithme qui s'inspire de la théorie de l'évolution de Darwin, et de la génétique de Mendel.  
Dans cet algorithme, les potentielles solutions sont des chromosomes, faisant partie d'une population - L'ensemble des solutions à tester - et sont composés de gènes, qui sont ici les nombres et opérateurs.

# L'implémentation
Notre implémentation est en python, reprenant le modèle python fourni initialement. Aucune définition de fonction n'a été changé.  
Les différentes étapes de l'algorithme comporte plusieurs méthodes possible. Ces méthodes sont chacunes décrites dans des énumérations.  
En haut du programme, des variables globales sont déclarées pour indiquer les méthodes utilisés pour chaque étapes.
## Décodage d'un chromosome
La fonction de décodage permet de passer d'un chromosome binaire, donc chaque groupe de 4 bit représente un gène, à une chaîne de caractère représentant une suite d'opération valide.  
Si un chromosome comporte des opérations invalide, on va les ignorer dans le résultat final.  
Voilà quelques exemples d'opérations invalide (Ici déjà décodées pour rendre compréhensible le problème:)
### 2 digits consécutifs

    3 + 4 5 / 3   ->   3 + 4 / 3
Ici, deux digits se suivent, le deuxième digit, le 5, sera donc ignoré.

### 2 opérateurs consécutifs

    3 + - 5   ->   3 + 5
Ici, deux opérateurs se suivent, le deuxième opérateur, le -, sera donc ignoré.

### Division par 0

    3 + 5 / 0 + 6   ->   3 + 5 + 6
Ici, une division par zéro a lieu. Ce n'est pas valide mathématiquement, on va donc ignorer cette division

### Gène invalide

    3 + n/a 5   ->   3 + 5
Les gènes sont encodés en binaire, sur 4 bits, cela laisse donc la possiblité d'avoir 16 caractères, seulement, nous n'en utilisons que 14, il reste donc 2 gènes possible, qui ne correspondent à aucun gène. Si l'un gène pareil est obtenu, il est ignoré.

## Evaluation d'un chromosome
L'evaluation d'un chromosome permet d'obtenir le résultat du chromosome.
Dans notre cas, nous commençons pas obtenir le chromosome décodé, afin d'avoir une suite d'opération valide à évaluer.  
On va donc évaluer les charactères du chromosome décodés les uns après les autres, et leur appliquer les opérations obtenues.  
Si une opération invalide est trouvée, cela indiquerait un défaut dans la fonction de décodage, et le problème va s'arrêter.

## Fonction de fitness
La fonction de fitness doit retourner une valeur pour indiquer à quelle point le chromosome est une bonne solution. Plus la valeur est élevée, meilleure la solution est.  
Une seule fonction de fitness a été implémentée dans notre solution, et elle retourne simplement l'opposé de la différence entre le résultat recherché et le résultat de l'évaluation du chromosome.

## Les crossover de deux chromosomes
Le crossover de deux chromosomes consiste à retourner 2 chromosomes, qui sont des mélanges des deux chromosomes de base.  
Pour le crossover, on a 3 méthodes possibles. La méthode utilisée est choisie en utilisant la variable globale CROSSOVER_METHOD, qui consiste en un tuple, avec comme première valeur, la méthode choisie, et en deuxième valeur, le paramètre de la méthode (une valeur entière).  
Pour rendre l'implémentation plus facile, nous partons du principe que les deux chromosomes obtenus en paramètre sont de même longueur, et les chromosomes qui résulte de la fonction seront aussi aussi de la même longueur que leurs parents

### Découpage des chromosomes en un nombre n de parties
Cette méthode correspond à la valeur EXCHANGE_X_PARTS. Exemple de valeur de la variable globale:

    CROSSOVER_METHOD = (CrossoverMethod.EXCHANGE_X_PARTS, 4)

Cette méthode va découper les chromosomes en un nombre de partie indiquée dans la variable globale, et échanger entre les deux chromosomes une partie sur deux pour créer les chromosomes finaux. Par exemple, pour la valeur passé en paramètre 4, et les deux chromosomes suivants: "00000000" et "11111111", on obtiendra les enfants suivant:
"00110011" et "11001100".

### Echange tout les n bits
Cette méthode correspond à la valeur EXCHANGE_EACH_X_BIT. Exemple de valeur de la variable globale:

    CROSSOVER_METHOD = (CrossoverMethod.EXCHANGE_EACH_X_BIT, 1)
Cette méthode va échanger les bits une fois sur deux, tout les n nombre de bit (n étant la valeur indiquée dans la variable globale).  
Par exemple, pour la valeur passé en paramètre 1, et les deux chromosomes suivants: "00000000" et "11111111", on obtiendra les enfants suivant:
"01010101" et "10101010".

### Echange tout les n gènes
Cette méthode correspond à la valeur EXCHANGE_EACH_X_GENE. Exemple de valeur de la variable globale:

    CROSSOVER_METHOD = (CrossoverMethod.EXCHANGE_EACH_X_GENE, 1)
Cette méthode va échanger les genes une fois sur deux, tout les n nombre de genes (n étant la valeur indiquée dans la variable globale).  
Par exemple, pour la valeur passé en paramètre 1, et les deux chromosomes suivants: "0000000000000000" et "1111111111111111", on obtiendra les enfants suivant:
"0000111100001111" et "1111000011110000".

## Crossover sur une population
Le crossover sur une population a comme objectif de prendre une population initiale, et retourner une population d'enfant de la population initiale.
Nous avons décidé que la population d'enfant doit être 2 fois plus grande que celle de ses parents. Cela, pour permettre de rééquilibrer la taille de la population, car lors de la sélection, nous ne gardons que la moitié de la population.  
Pour faire cela, on prend deux chromosome de la population initale, on applique la fonction de crossover, puis on recommence avec un autre couple de chromosome.
Pour obtenir une population finale de taille 2 fois supérieure à la population initiale, nous avons conclu qu'il fallait que chaque chromosome participe à un crossover 2 fois, chaque fois avec un partenaire différent.  
Pour faire cela, nous avons décidé que l'on itérerait sur chaque chromosome d'une liste contenant la population, et qu'à chaque itération, le chromosome actuel ferait un crossover avec le chromosome suivant. Le dernier chromosome de la liste prendra comme partenaire le premier chromosome de la liste.  
De cette manière, chaque chromosome va faire un crossover avec ses deux voisins dans la liste.

## Mutation d'un chromosome
La mutation d'un chromosome consiste à modifier son contenu.  
Nous avons pour cette étape 4 méthodes. Toutes ces méthodes dépendant d'un algorithme de pseudo aléatoire déjà implémenté dans le langage python.
La méthode utilisée est choisie en utilisant la variable globale MUTATION_METHOD, qui consiste en un tuple, avec comme première valeur, la méthode choisie, et en deuxième valeur, le paramètre de la méthode (une valeur entière).  
### Inversion de n bits
Cette méthode correspond à la valeur INVERT_X_BIT de l'énumération. Exemple:

    MUTATION_METHOD = (MutationMethod.INVERT_X_BIT, 4)
Cette méthode va choisir de manière aléatoire n bits du chromosome (ou n est la deuxième valeur de la variable globale), et les inverser, c'est à dire faire passer 1 à 0, et 0 à 1. Par exemple, pour le chromosome "11111111" avec la valeur n=4, on pourrait obtenir: "10110010" (Les index 1,4,5,7 ont été inversés).

### Inversion de 1 bits pour n gènes
Cette méthode correspond à la valeur INVERT_ONE_BIT_OF_X_GENES de l'énumération. Exemple:

    MUTATION_METHOD = (MutationMethod.INVERT_ONE_BIT_OF_x_GENES, 2)
Cette méthode va choisir de manière aléatoire n gènes du chromosome (ou n est la deuxième valeur de la variable globale), et inverser un bit choisi aléatoirement pour chacun. Par exemple, pour le chromosome "1111000011110000" avec la valeur n=2, on pourrait obtenir: "1011000011110010" (Les index 1 et 14 dans les gènes 0 et 3 ont été inversés).

### Inversion de tout les bits de n gènes
Cette méthode correspond à la valeur INVERT_ALL_BITS_OF_X_GENES de l'énumération. Exemple:

    MUTATION_METHOD = (MutationMethod.INVERT_ALL_BITS_OF_X_GENES, 2)
Cette méthode va choisir de manière aléatoire n genes du chromosome (ou n est la deuxième valeur de la variable globale), et inverser tout leurs bits. Par exemple, pour le chromosome "1111000011110000" avec la valeur n=2, on pourrait obtenir: "1111111100000000" (Les 2ème et 3ème gènes ont été inversés).

### Mélange de tout les bits de n gènes
Cette méthode correspond à la valeur SCRAMBLE_ALL_BITS_OF_X_GENES de l'énumération. Exemple:

    MUTATION_METHOD = (MutationMethod.SCRAMBLE_ALL_BITS_OF_X_GENES, 2)
Cette méthode va choisir de manière aléatoire n genes du chromosome (ou n est la deuxième valeur de la variable globale), et mélanger de manières aléatoire tout leurs bits. Par exemple, pour le chromosome "1001100110011001" avec la valeur n=2, on pourrait obtenir: "1100100101101001" (Les 1er et 3ème gènes ont été mélangés).

## Sélection dans une population
Cette étape permet de sélectionner la partie de la population que l'on va garder pour la suite de l'algorithme. Dans notre implémentation, nous gardons la moitié de la population donnée.
Il y a 4 méthode, et un mode élitiste à activer ou désactiver.
La méthode utilisée est choisie en utilisant la variable globale SELECTION_METHOD, qui consiste en un tuple, avec comme première valeur, la méthode choisie, et en deuxième valeur, un booléen indiquant si l'on active (True) le mode élitiste ou non (False).

### Le mode élitiste
Le mode élitiste consiste à toujours garder dans la population la meilleure solution trouvée. Cela permet de ne pas divergé totalement d'une bonne solution. Ce mode complète les méthodes expliqué ensuite s'il est activé.

### La sélection uniforme
Cette méthode correspond à la valeur UNIFORM de l'énumération. Exemple: 

    SELECTION_METHOD = (SelectionMethod.UNIFORM, True)
La méthode de sélection uniforme consiste en la sélection de manière aléatoire de la population. Pour cela, on utilise l'algorithme de pseudo-aléatoire de python pour mélanger un tableau contenant la population, puis on sélectionne la première moitié du tableau.

### La sélection par rang
Cette méthode correspond à la valeur RANK de l'énumération. Exemple: 

    SELECTION_METHOD = (SelectionMethod.RANK, True)
La méthode de sélection par rang consiste en la sélection des meilleures chromosome. Pour cela, on tri la population selon leur résultat à la fonction de fitness, et on prend la moitié avec le meilleur résultat.

### La sélection par tournoi
Cette méthode correspond à la valeur TOURNAMENT de l'énumération. Exemple: 

    SELECTION_METHOD = (SelectionMethod.TOURNAMENT, True)
La méthode de sélection par tournoi consiste en l'organisation d'un sorte de tournoi, donc on garde les chromosomes ayant gagné leur match. Pour cela, on crée de manière aléatoire des paires avec tout les chromosomes, et on ne garde que le chromosome avec le meilleur résulat à la fonction de fitness pour chaque paire.

### La sélection par roulette
[//]: # (TODO)


## Génération d'une population initiale
Cette méthode n'a pas été modifiée, et correspond donc à la version originale qui se trouvait dans le modèle de départ

## L'algorithme génétique
Cette méthode n'a pas été modifiée, et correspond donc à la version originale qui se trouvait dans le modèle de départ
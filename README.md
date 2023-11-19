# Intelligence artificielle I - TP3 : Le Compte Est Bon

## Description

Le principe du jeu est le suivant :  A l'aide des nombres entiers de 0 à 9 et des opérateurs mathématiques de base (addition, soustraction, multiplication et division), trouver une suite de nombres et d'opérateurs permettant d'atteindre une cible numérique donnée. 

Chaque individu représente une suite de nombre et d'opérateurs. Un individu est représenté par son chromosome qui est une suite de gènes. Chaque gène représente un nombre, un opérateur ou un gène invalide (qui ne contribue pas au calcul). Chaque gène est encodé par une suite de 4 symboles 1 ou 0 (encodage binaire). 

## Résultat

Le script est capable de trouver une suite de nombre et d'opérateur qui donne la cible. La limite de temps donné est toujours strictement respectée. 

## Dépendances 

- Python > 3.10
- Matplotlib (uniquement pour les tests)

## Utilisation

Vous pouvez importer le module `Buhler_Dekhli` et utiliser la fonction `run_ag()` avec les arguments suivants : 

- `nb_individuals: int` Le nombre d'individus de la population (conseillé : 200)
- `nb_genes: int` : Le nombre de gènes de chaque chromosome (conseillé : 100)
- `target` : La cible à atteindre 
- `limit_sec` Le temps à disposition pour résoudre le problème

Cette fonction retourne la population **triée par ordre décroissant de fitness** à la fin de l'algorithme. Pour évaluer le meilleur résultat, il est possible d'utiliser la fonction `evaluate()` sur le premier élément de la population reçue. 

La fonction `main()` recherche par défaut le nombre $\pi$ en 5 secondes, avec une population de 200 et 100 gènes. 

```bash
python3 Buhler_Dekhli.py
```


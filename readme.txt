(1 min):
python .\main.py .\jeu1-faux-4x4.txt
le puzzle est insolvable en raison d'une répétition du chiffre 2 dans la première colonne.

python .\main.py .\jeu2-faux-9x9.txt
le puzzle est insolvable en raison d'une répétition du chiffre 5 dans la sixième ligne.

python .\main.py .\jeu3-faux-9x9.txt
le puzzle est insolvable en raison d'une répétition du chiffre 5 dans une région.

python .\main.py .\jeu2-vrai-4x4.txt
un exemple de puzzle Sudoku solvable de taille 4x4.

python .\main.py .\jeu1-vrai-9x9.txt
un exemple de puzzle Sudoku solvable de taille 9x9.

Le Sudoku est un jeu de logique populaire qui consiste à remplir une grille 9x9 avec des chiffres de 1 à 9, 
en veillant à ce que chaque ligne, chaque colonne et chaque région 3x3 contienne tous les chiffres de 1 à 9 sans répétition.

Formalisation du Problème (3 min) :

Pour résoudre le Sudoku, nous avons d'abord dû formaliser le problème en utilisant la logique propositionnelle.
Nous avons représenté chaque combinaison possible de chiffres dans la grille (ligne, colonne, valeur) comme une variable booléenne.
Par exemple, pour une grille 9x9, nous avons utilisé un tableau 3D s où s[a][b][c] représente la présence du chiffre c+1 dans la case (a+1, b+1).
Ensuite, nous avons défini des clauses logiques qui garantissent que chaque ligne, colonne et région contient exactement un chiffre de chaque valeur de 1 à 9, 
ainsi que des clauses pour respecter les indices initiaux donnés dans le puzzle.

Génération des Clauses (3 min) :

Nous avons développé des fonctions pour générer les différentes clauses nécessaires pour représenter les contraintes du Sudoku en logique propositionnelle.
Cela inclut des clauses pour assurer qu'il y a au moins un chiffre dans chaque case, que chaque chiffre apparaît au plus une fois dans chaque ligne, colonne et région, 
et que les indices initiaux sont respectés.
Ces clauses ont été ajoutées à un tableau clauses pour être utilisées par le SAT-solveur.

Utilisation du SAT-solveur (2 min) :

Une fois les clauses générées, nous avons utilisé un SAT-solveur pour résoudre le problème.
Nous avons traduit les clauses en format DIMACS, un format standard pour les SAT-solveurs, puis en format DIMACS 3-SAT si nécessaire.
Enfin, nous avons utilisé la bibliothèque Z3 pour résoudre le problème SAT et trouver une solution satisfaisante.

Résultats et Conclusion (1 min) :

Grâce à notre approche, nous avons réussi à résoudre efficacement des puzzles Sudoku de différentes tailles et niveaux de difficulté.
Notre programme peut résoudre des puzzles en quelques secondes, offrant une solution précise à des problèmes autrement complexes.
En conclusion, ce projet nous a permis d'explorer la puissance de la logique propositionnelle et des SAT-solveurs dans la résolution de problèmes pratiques comme le Sudoku.


729 variables booléennes
12402 clauses generée
p cnf format fichier DIMACS forme conjonctif
chaque ligne une clauses


Dans le contexte du format DIMACS, 
signifie qu'il y a un total de 729 variables booléennes dans le problème SAT associé.
Chaque variable booléenne représente une combinaison possible de chiffres dans la grille du Sudoku.

Pour un Sudoku de taille standard 9x9, il y a 81 cases dans la grille, 
et chaque case peut contenir un chiffre parmi 1 à 9. 
Donc, il y a un total de 81 * 9 = 729 combinaisons possibles de chiffres dans la grille. 
Chaque combinaison est représentée par une variable booléenne dans le problème SAT.

la structure s est créée comme une liste 3D,
où s[z][y][x] représente une variable booléenne associée à la cellule (x, y) de la grille de Sudoku,
 contenant la valeur z + 1.
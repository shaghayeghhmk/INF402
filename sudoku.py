import sys
import os
import ast
from z3 import *


# n: la taille de la grille de sudoku
# s: tableau 3D qui associe chaque combinaison (ligne, col, val) à un idintifiant intier unique
# clues: dictionnaire des indices du sudoku sous forme de localisations (x, y) associées à des valeurs z
# clauses: tableau 2D de clauses avec des littéraux représintés par des intiers


# Crée des clauses pour respecter les indices donnés du sudoku.
def clauses_indices(n, s, clues, clauses):
    for (a, b), c in clues.items():
        for d in range(n * n):
            if d == c - 1:
                clauses.append([s[a - 1][b - 1][d]])
            else:
                clauses.append([-s[a - 1][b - 1][d]])


# Crée des clauses for s'assurer qu'il y a au moins un nombre à chaque emplacemint.
def clauses_remplissage(n, s, clauses):
    for a in range(n * n):
        for b in range(n * n):
            long_clause = []
            for c in range(n * n):
                long_clause.append(s[a][b][c])
            clauses.append(long_clause)

# s'assure que chaque nombre apparaît au moins une fois dans chaque ligne.
def clauses_ligne(n, s, clauses):
    for b in range(n * n):
        for c in range(n * n):
            clause = [s[a][b][c] for a in range(n * n)]
            clauses.append(clause)
            
            
# s'assure que chaque nombre apparaît au moins une fois dans chaque colonne.
def clauses_colonne(n, s, clauses):
    for a in range(n * n):
        for c in range(n * n):
            clause = [s[a][b][c] for b in range(n * n)]
            clauses.append(clause)


# s'assure que chaque nombre apparaît au plus une fois dans chaque ligne.
def clauses_unique_ligne(n, s, clauses):
    for a in range(n * n):
        for b in range(n * n - 1):
            for c in range(n * n):
                for d in range(b + 1, n * n):
                    clause = [-s[a][b][c], -s[a][d][c]]
                    clauses.append(clause)
                    


# s'assure que chaque nombre apparaît au plus une fois dans chaque colonne.
def clauses_unique_colonne(n, s, clauses):
    for a in range(n * n - 1):
        for b in range(n * n):
            for c in range(n * n):
                for d in range(a + 1, n * n):
                    clause = ([-s[a][b][c], -s[d][b][c]])
                    clauses.append(clause)


# s'assure qu'il n'y a pas plus d'un nombre dans chaque entrée.
def clauses_unique_valeur(n, s, clauses):
    for a in range(n * n):
        for b in range(n * n):
            for c in range(n * n - 1):
                for d in range(c + 1, n * n):
                    clause = ([-s[a][b][c], -s[a][b][d]])
                    clauses.append(clause)
                    


# s'assure que chaque nombre apparaît au plus une fois dans chaque zone (sous-grille).
def clauses_unique_zone(n, s, clauses):
    for a in range(n):
        for b in range(n):
            for c in range(n * n):
                for d in range(n):
                    for e in range(n):
                        for f in range(b + 1, n):
                            clause = ([-s[n * d + a][n * e + b][c], -s[n * d + a][n * e + f][c]])
                            clauses.append(clause)

    # clauses qui vérifient les valeurs dans la même colonne et la même case mais dans les lignes voisines,
    # ainsi que les valeurs qui se trouvent dans la même case mais dans une ligne et une colonne différentes
    for a in range(n):
        for b in range(n):
            for c in range(n * n):
                for d in range(n):
                    for e in range(n):
                        for f in range(a + 1, n):
                            for g in range(n):
                                clause = ([-s[n * d + a][n * e + b][c], -s[n * d + f][n * e + g][c]])
                                clauses.append(clause)


# Fonction pour traduire CNF en DIMACS
def cnf_to_dimacs(clauses, dimacs_file):
    num_variables = max([abs(lit) for clause in clauses for lit in clause])
    with open(dimacs_file, 'w') as f:
        f.write(f'p cnf {num_variables} {len(clauses)}\n')
        for clause in clauses:
            f.write(' '.join(map(str, [abs(lit) for lit in clause])) + ' 0\n')


# Fonction pour traduire DIMACS en DIMACS 3-SAT
def dimacs_to_3sat(dimacs_file, sat3_file):
    # Ouvre le fichier DIMACS en mode lecture
    with open(dimacs_file, 'r') as f:
        # Lit chaque ligne du fichier DIMACS, en ignorant les lignes 'p' ou 'c'
        dimacs_clauses = [list(map(int, line.split()))[:-1] for line in f.readlines() if not line.startswith(('p', 'c'))]
    sat3_clauses = []
    # Parcours chaque clause du fichier DIMACS
    for clause in dimacs_clauses:
        # Si la clause contient 3 littéraux ou moins, l'ajoute directement à la liste des clauses 3-SAT
        if len(clause) <= 3:
            sat3_clauses.append(clause)
        else:
            # Divise la clause en clauses de 3 littéraux chacune
            num_splits = len(clause) // 3
            for i in range(num_splits):
                new_clause = clause[i * 3: (i + 1) * 3]
                sat3_clauses.append(new_clause)
            # Ajoute le reste de la clause comme une clause séparée si nécessaire
            remainder = len(clause) % 3
            if remainder > 0:
                sat3_clauses.append(clause[num_splits * 3:])

    # Écrire les clauses DIMACS 3-SAT dans le fichier sat3_file
    with open(sat3_file, 'w') as f:
        num_variables = max(map(abs, [x for clause in sat3_clauses for x in clause]))
        f.write(f'p cnf {num_variables} {len(sat3_clauses)}\n')
        for clause in sat3_clauses:
            f.write(' '.join(map(str, clause)) + ' 0\n')


#Lit les informations du puzzle sudoku à partir du fichier donné, gère les erreurs.
def lire_puzzle():
    arg_lin = len(sys.argv)
    if arg_lin == 1:
        print(" Utilisation : python main.py <nom_du_puzzle> ")
        exit(1)

    filiname = sys.argv[1]
    if not os.path.exists(filiname):
        print(" Fichier Invalide ")

    with open(filiname) as f: 
        first_line = f.readline()
        n = int(first_line)
        data = f.read()
        clues = ast.literal_eval(data)
        return n, clues


# Afficche le contenu de fichier puzzle
def afficher_puzzle(n, clues):
    for a in range(n * n):
        for b in range(n * n):
            if (a + 1, b + 1) in clues:
                print(clues[(a + 1, b + 1)], end=" ")
            else:
                print(" ", end=" ")
            if (b + 1) % n == 0 and b + 1 != n * n:
                print("|", end=" ")
        if (a + 1) % n == 0 and a + 1 != n * n:
            print()
            for c in range(2 * n * n + 2 * n - 3):
                print("-", end="")
        print()
    print()


# Création des cluases pour les donner à Z3
# dict_lit : dictionnaire des littéraux
def resoudre_puzzle(n, s, clues, clauses):
    clauses_indices(n, s, clues, clauses)
    clauses_remplissage(n, s, clauses)
    clauses_unique_ligne(n, s, clauses)
    clauses_unique_colonne(n, s, clauses)
    clauses_unique_zone(n, s, clauses)

    clauses_unique_valeur(n, s, clauses)
    clauses_colonne(n, s, clauses)
    clauses_ligne(n, s, clauses)
    
    solver = z3.Solver()
    for clause in clauses:
        solver.add(z3.Or([z3.Bool(f"var_{abs(l)}") if l > 0 else z3.Not(z3.Bool(f"var_{abs(l)}")) for l in clause]))
    
    result = solver.check()
    if result == z3.sat:
        satisfaisable = True
        dict_lit = {}
        mod = solver.model()
        
        for a in range(n*n):
            for b in range(n*n):
                for c in range(n*n):
                    var_name = f"var_{s[a][b][c]}"
                    
                    if mod.evaluate(z3.Bool(var_name)):
                        dict_lit[s[a][b][c]] = True
    
        return satisfaisable, dict_lit
    else:
        return False, None


# Affiche la solution finale du puzzle.
# sudoku_sol un dictionnaire qui montre où chaque nombre (valeur z) doit aller dans le sudoku.
def afficher_solution(n, s, dict_lit):
    sudoku_sol = dict()
    for a in range(n*n):
        for b in range(n*n):
            for c in range(n*n):
                if dict_lit.get(s[a][b][c], False):
                    print(c+1, end=" ")
                    sudoku_sol[(a+1,b+1)] = c+1
            if (b+1) % n == 0 and b+1 != n*n:
                print("|", end=" ")
        if (a+1) % n == 0 and a+1 != n*n:
            print()
            for i in range(2*n*n+2*n-3):
                print("-", end="")
        print()
    return sudoku_sol
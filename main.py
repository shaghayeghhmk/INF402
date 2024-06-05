import sudoku
import os
import sys

if __name__ == "__main__":
    
    # Lecture du puzzle Sudoku à partir d'un fichier
    n, clues = sudoku.lire_puzzle()

    # Affichage du puzzle initial
    print("Voici le puzzle initial :")
    sudoku.afficher_puzzle(n, clues)

    # Mapping des variables et génération des clauses
    s = [[[(n*n*n*n*x) + (n*n*y) + z + 1 for x in range(n*n)] for y in range(n*n)] for z in range(n*n)]
    clauses = []

    # Résolution du puzzle Sudoku
    sat, assm = sudoku.resoudre_puzzle(n, s, clues, clauses)
    if sat:
        print("Le puzzle est solvable !")
        # Affichage de la solution
        print("Voici la solution :")
        sudoku.afficher_solution(n, s, assm)
        
        # Créer les noms des fichiers de sortie
        file_prefix = os.path.splitext(os.path.basename(sys.argv[1]))[0]
        cnf_dimacs_file = f"{file_prefix}_cnf_dimacs.txt"
        sat3_dimacs_file = f"{file_prefix}_3sat_dimacs.txt"
        
        # Traduction des clauses en format DIMACS
        sudoku.cnf_to_dimacs(clauses, cnf_dimacs_file)
        
        # Traduction du format DIMACS en format DIMACS 3-SAT
        sudoku.dimacs_to_3sat(cnf_dimacs_file, sat3_dimacs_file)
        
    else:
        print("Le puzzle est insolvable.")

"""
Rôle : Orchestrer le pipeline complet de résolution Norinori.

Pipeline :
  [1/3] lecteur_grille     → lire et parser le fichier grille
  [2/3] generateur_dimacs  → produire le fichier .cnf DIMACS
  [3/3] MiniSat            → résoudre + affichage_solution

Usage :
  python main.py instances/ma_grille.txt

Codes de retour de MiniSat :
  10 = SAT   (solution trouvée)
  20 = UNSAT (pas de solution)
"""

import sys
import os
import subprocess

from lecteur     import parse_grid, afficher_grille, afficher_zones
from generateur_dimacs   import generer_dimacs
from affichage_solution  import lire_solution, afficher_solution


def resoudre(chemin_grille):

    # Dériver les noms de fichiers intermédiaires
    base       = os.path.splitext(chemin_grille)[0]
    chemin_cnf = base + ".cnf"
    chemin_sat = base + ".sat"

    # Étape 1 : lire la grille
    print(f"[1/3] Lecture de la grille : {chemin_grille}")
    n, m, grille, zones = parse_grid(chemin_grille)
    afficher_grille(n, m, grille)
    afficher_zones(zones)

    # Étape 2 : générer le fichier DIMACS
    print(f"[2/3] Génération du fichier DIMACS : {chemin_cnf}")
    nb_clauses = generer_dimacs(n, m, zones, chemin_cnf)
    print(f"      {n * m} variables, {nb_clauses} clauses\n")

    # Étape 3 : appeler MiniSat
    print("[3/3] Appel à MiniSat...")
    resultat = subprocess.run(
        ["minisat", chemin_cnf, chemin_sat],
        capture_output=True,
        text=True
    )

    # Codes de retour MiniSat : 10 = SAT, 20 = UNSAT
    if resultat.returncode == 20:
        print("\n UNSAT : cette grille n'a pas de solution.\n")
        return False
    elif resultat.returncode != 10:
        print(f"\n Code inattendu de MiniSat : {resultat.returncode}")
        return False

    print("Solution trouvée !\n")

    # Étape 4 : afficher la solution 
    satisfaisable, cases_noires = lire_solution(chemin_sat)
    afficher_solution(n, m, grille, cases_noires)

    return True


# Point d'entrée
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage   : python main.py <fichier_grille.txt>")
        print("Exemple : python main.py instances/test_2x2.txt")
        sys.exit(1)

    chemin = sys.argv[1]

    if not os.path.exists(chemin):
        print(f"Erreur : fichier introuvable → {chemin}")
        sys.exit(1)

    succes = resoudre(chemin)
    sys.exit(0 if succes else 1)
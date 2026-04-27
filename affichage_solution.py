"""
Rôle : Lire la sortie de MiniSat et afficher la grille
       Norinori résolue de façon lisible.

Format du fichier de sortie MiniSat :
  Ligne 1 : "SAT" ou "UNSAT"
  Ligne 2 : liste d'entiers terminée par 0
            entier positif  k  → variable k = VRAI  (case noire)
            entier négatif -k  → variable k = FAUX  (case blanche)

"""


def numero_variable(i, j, m):

    return i * m + j + 1



def lire_solution(chemin_sat):
    try:
        with open(chemin_sat, "r") as fichier:
            lignes = [ligne.strip() for ligne in fichier.readlines()]
    except FileNotFoundError:
        print(f"Erreur : fichier {chemin_sat} introuvable")
        return False, set()
    
    if not lignes or lignes[0] != "SAT":
        return False, set()
    
    # Ignorer la ligne 0 et prendre la ligne 1
    if len(lignes) < 2:
        return False, set()
    
    entiers = []
    for mot in lignes[1].split():
        if mot == '0':
            break
        entiers.append(int(mot))
    
    cases_noires = {k for k in entiers if k > 0}  # uniquement les variables VRAIES
    return True, cases_noires


def afficher_solution(n, m, grille, cases_noires):
  
    # Étape 1 : grille solution
    print("═" * (m*3 + 2))
    print(" SOLUTION NORINORI ")
    print("═" * (m*3 + 2))
    
    # Grille solution
    for i in range(n):
        ligne = "│ "
        for j in range(m):
            if numero_variable(i, j, m) in cases_noires:
                ligne += "■ │"
            else:
                ligne += "□ │"
        print(ligne)
    print("╚" + "═══" * m)

    # Étape 2 : grille de référence 
    print("Zones (pour référence) :")
    for i in range(n):
        print("  " + "  ".join(f"{grille[i][j]:<2}" for j in range(m)))
    print()

    # ── Étape 3 : vérification règle 1 
    print("Vérification (cases noires par zone) :")
    comptage = {}
    for i in range(n):
        for j in range(m):
            id_zone = grille[i][j]
            if id_zone not in comptage:
                comptage[id_zone] = 0
            if numero_variable(i, j, m) in cases_noires:
                comptage[id_zone] += 1

    tout_correct = True
    for id_zone, nb in comptage.items():
        statut = "v" if nb == 2 else "x ERREUR"
        print(f"  Zone {id_zone} : {nb} case(s) noire(s)  {statut}")
        if nb != 2:
            tout_correct = False

    print()
    if tout_correct:
        print("La règle 1 est respectée pour toutes les zones.")
    else:
        print("Certaines zones ne respectent pas la règle 1 !")


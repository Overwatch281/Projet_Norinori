"""
Rôle : Traduire une grille Norinori en un fichier DIMACS
       (.cnf) lisible par un SAT-solveur (ex: MiniSat).

Rappel des règles :
  Règle 1   : exactement 2 cases noires par zone
                = "au moins 2" ET "au plus 2"
  Règles 2+3: chaque case noire a exactement 1 voisin
              orthogonal noir
                = "au moins 1 voisin" ET "au plus 1 voisin"

Numérotation des variables SAT :
numero_variable(i, j) = i * m + j + 1
(les variables SAT commencent à 1, jamais à 0)
"""



from itertools import combinations

def var(i,j,m):
    """
    Retourne le numéro de variable SAT (≥ 1) pour la case (i, j).

    Paramètres :
      i (int) : ligne
      j (int) : colonne
      m (int) : nombre de colonnes de la grille
    """
    return i*m + j + 1



def generer_regle1(zones, m):
    """
    Génère les clauses imposant exactement 2 cases noires par zone.

    Paramètres :
      zones (dict) : { id_zone: [(i,j), ...] }
      m     (int)  : nombre de colonnes

    Retourne :
      clauses (list[list[int]]) : liste de clauses
    """
    clauses = []
    # Numéros de variables pour toutes les cases de cette zone
    for zone, cases in zones.items():
        var_zone = [var(i,j,m) for (i,j) in cases]
        
        # AU MOINS 1 case noire dans la zone (interdit que tout soit blanc)
        clauses.append(var_zone[:])

        # AU MOINS 2 : si Ci est noire, au moins une autre l'est aussi
        for idx, vi in enumerate(var_zone):
            autres = [vj for vj in var_zone if vj != vi]
            clauses.append([-vi] + autres)
        
        # AU PLUS 2 : interdire TOUTES les combinaisons > 2
        for k in range(3, len(var_zone) + 1):  # 3,4,5,...
            for combi in combinations(var_zone, k):
                clause = [-v for v in combi]  # toutes négatives
                clauses.append(clause)
    return clauses

def voisins(i, j, n, m):
    """
    Retourne la liste des cases voisines orthogonales valides.

    Paramètres :
      i, j (int) : coordonnées de la case
      n, m (int) : dimensions de la grille
    """
    resultat = []
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for dc_l, dc_c in directions:
        ligne_voisine = i + dc_l
        colonne_voisine = j + dc_c

        if 0 <= ligne_voisine < n and 0 <= colonne_voisine < m:
            resultat.append((ligne_voisine,colonne_voisine))
    
    return resultat



def generer_regles2_3(n, m):
    clauses = []
    for i in range(n):
        for j in range(m):
            var_case = var(i,j,m)
            voisins_case = voisins(i,j,n,m)
            
            if not voisins_case:
                clauses.append([-var_case])
                continue
            
            # Au moins 1 : une seule clause !
            clause_au_moins_1 = [-var_case]
            for li, lj in voisins_case:
                clause_au_moins_1.append(var(li,lj,m))
            clauses.append(clause_au_moins_1)  # ✅ APRÈS la boucle !
            
            # Au plus 1
            for indice_a in range(len(voisins_case)):
                for indice_b in range(indice_a + 1, len(voisins_case)):
                    va = var(voisins_case[indice_a][0], voisins_case[indice_a][1], m)
                    vb = var(voisins_case[indice_b][0], voisins_case[indice_b][1], m)
                    clauses.append([-var_case, -va, -vb])
    return clauses



def ecrire_fichier_dimacs(chemin, nb_vars, clauses):

    with open(chemin, "w") as fichier:

        fichier.write("c FIchier Dimacs Norinori \n")
        fichier.write(f"p cnf {nb_vars} {len(clauses)} \n")


        for clause in clauses :
            fichier.write(" ".join(str(l) for l in clause) + " 0\n")

def generer_dimacs(n, m, zones, chemin_sortie):
    """
    Génère le fichier DIMACS complet pour une instance Norinori.

    Paramètres :
      n, m          (int)  : dimensions de la grille
      zones         (dict) : { id_zone: [(i,j), ...] }
      chemin_sortie (str)  : chemin du fichier .cnf à créer

    Retourne :
      nb_clauses (int) : nombre total de clauses générées
    """
    nb_vars = n * m

    clauses_r1   = generer_regle1(zones, m)
    clauses_r2r3 = generer_regles2_3(n, m)
    toutes_clauses = clauses_r1 + clauses_r2r3

    ecrire_fichier_dimacs(chemin_sortie, nb_vars, toutes_clauses)

    return len(toutes_clauses)


# Test rapide
if __name__ == "__main__":
    import sys
    from lecteur import parse_grid, afficher_grille, afficher_zones

    chemin_grille = sys.argv[1] if len(sys.argv) > 1 else "instances/test_4x4.txt"
    chemin_cnf    = sys.argv[2] if len(sys.argv) > 2 else "instances/test_4x4.cnf"

    print(f"Lecture : {chemin_grille}")
    n, m, grille, zones = parse_grid(chemin_grille)
    afficher_grille(n, m, grille)

    print(f"Génération DIMACS : {chemin_cnf}")
    nb = generer_dimacs(n, m, zones, chemin_cnf)
    print(f"  Variables : {n * m}")
    print(f"  Clauses   : {nb}\n")

    clausees_2 = generer_regles2_3(n,m)
    print(len(clausees_2))
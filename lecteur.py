"""

Lit un fichier décrivant une grille Norinori et retourne :
  - n, m       : dimensions de la grille
  - grille     : matrice n×m des identifiants de zone
  - zones      : dictionnaire { zone_id : [(i,j), ...] }

Format du fichier d'entrée :
  Ligne 1      : "n m"  (nombre de lignes, nombre de colonnes)
  Lignes 2..reste: identifiants de zone séparés par des espaces

Exemple (4×4) :
  4 4
  A A B B
  A C C B
  D D C E
  D F F E
"""


def parse_grid(filepath):
    """
    Lit le fichier et retourne (n, m, grille, zones).
    """
    with open(filepath, "r") as f:
        lignes = f.read().splitlines()  # lire toutes les lignes sans \n

    # --- Ligne 1 : dimensions ---
    premiere_ligne = lignes[0].split()
    n = int(premiere_ligne[0])  # nombre de lignes
    m = int(premiere_ligne[1])  # nombre de colonnes

    # --- Initialisation ---
    grille = []          # grille[i][j] = identifiant de zone
    zones  = {}          # zones["A"] = [(0,0), (0,1), ...]

    #Lecture case par case
    for i in range(n):
        ligne_courante = lignes[i + 1].split()  # +1 car ligne 0 = dimensions

        if len(ligne_courante) != m:
            raise ValueError(
                f"Ligne {i+1} : attendu {m} cases, trouvé {len(ligne_courante)}"
            )

        ligne_grille = []
        for j in range(m):
            zone_id = ligne_courante[j]
            ligne_grille.append(zone_id)

            # Ajouter la case dans le dictionnaire des zones
            if zone_id not in zones:
                zones[zone_id] = []
            zones[zone_id].append((i, j))

        grille.append(ligne_grille)

    return n, m, grille, zones


def afficher_grille(n, m, grille):
    """
    Affiche la grille avec les identifiants de zone.
    """
    print("Grille des zones :")
    for i in range(n):
        print("  " + "  ".join(grille[i]))
    print()


def afficher_zones(zones):
    """
    Affiche le contenu de chaque zone.
    """
    print("Zones détectées :")
    for zone_id, cases in sorted(zones.items()):
        print(f"  Zone {zone_id} ({len(cases)} cases) : {cases}")
    print()


if __name__ == "__main__":
    import sys

    fichier = sys.argv[1] if len(sys.argv) > 1 else "instances/test_4x4.txt"

    print(f"Lecture du fichier : {fichier}\n")
    n, m, grille, zones = parse_grid(fichier)

    print(f"Dimensions : {n} lignes × {m} colonnes\n")
    afficher_grille(n, m, grille)
    afficher_zones(zones)
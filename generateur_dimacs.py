



"""

def var(i,j,m):
    return i*m + j + 1





def generer_regle1(zones,m):
    clauses = []
    for zone,cases in zones.item():
        var_zone = [var(i,j,m) for (i,j) in cases]
        n_cases = len(var_zone)

        clauses.append(var_zone[:])

    for idex, vi in enumerate(var_zone):
        autres = [vj for vj in var_zone if vi != vj]
        clauses.append([-vi] + autres)

    for (vi,vj,vk) in combinaisons(var_zone,3):
        clauses.append([-vi,vj,vk])

    return clauses



def generer_regles2_3(n,m):
    pass
"""



def ecrire_fichier_dimacs(chemin, nb_vars, clauses):

    with open(chemin, "w") as fichier:

        fichier.write("c FIchier Dimacs Norinori \n")
        fichier.write(f"p cnf {nb_vars} {len(clauses)} \n")


        for clause in clauses :
            fichier.write(" ".join(str(l) for l in clause) + " 0\n")

import os
chemin = "/home/pentester/Bureau/norinori/essai.cnf"

nb = 5
clauses = [[5,5,5],[3,6,3]]

ecrire_fichier_dimacs(chemin,nb,clauses)

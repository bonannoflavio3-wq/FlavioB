import numpy as np

plateau = np.full((3, 3), ' ')

joueurs = {
    "X": "",
    "O": ""
}

def afficher_plateau():
    print("\n  0   1   2")
    for i in range(3):
        print(i, " | ".join(plateau[i]))
        if i < 2:
            print("  ---------")

def verifier_victoire(symbole):
    for i in range(3):
        if all(plateau[i, :] == symbole) or all(plateau[:, i] == symbole):
            return True
    if all(np.diag(plateau) == symbole) or all(np.diag(np.fliplr(plateau)) == symbole):
        return True
    return False

def plateau_plein():
    return ' ' not in plateau

print("Bienvenue dans le jeu du Morpion !")
joueurs["X"] = input("Nom du joueur X : ")
joueurs["O"] = input("Nom du joueur O : ")

symbole_actuel = "X"

while True:
    print("\n" + "-" * 20)
    afficher_plateau()
    print(f"\n{joueurs[symbole_actuel]} ({symbole_actuel}), à vous de jouer.")

    try:
        ligne = int(input("Entrez la ligne (0, 1 ou 2) : "))
        colonne = int(input("Entrez la colonne (0, 1 ou 2) : "))
    except ValueError:
        print("Entrée invalide. Veuillez entrer un nombre.")
        continue

    if 0 <= ligne <= 2 and 0 <= colonne <= 2:
        if plateau[ligne, colonne] == ' ':
            plateau[ligne, colonne] = symbole_actuel
            if verifier_victoire(symbole_actuel):
                afficher_plateau()
                print(f"\n Félicitations {joueurs[symbole_actuel]} ! Vous avez gagné. ")
                break
            elif plateau_plein():
                afficher_plateau()
                print("\nMatch nul ! Le plateau est plein.")
                break
            symbole_actuel = "O" if symbole_actuel == "X" else "X"
        else:
            print(" Case déjà occupée, choisissez une autre.")
    else:
        print(" Coordonnées hors limites. Choisissez entre 0 et 2.")

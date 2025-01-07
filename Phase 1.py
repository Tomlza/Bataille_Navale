# Phase 1 : Mise en place des classes
import random

# Classe représentant un navire
class Navire:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []
        self.touches = []

    def est_coule(self):
        return set(self.positions) == set(self.touches)

# Classe représentant le plateau de jeu
class Plateau:
    def __init__(self, taille=10):
        self.taille = taille
        self.grille = [[None for _ in range(taille)] for _ in range(taille)]
        self.navires = []

    def placer_navire(self, navire, positions):
        if len(positions) != navire.taille:
            raise ValueError("Le nombre de positions ne correspond pas à la taille du navire.")
        for x, y in positions:
            if not (0 <= x < self.taille and 0 <= y < self.taille):
                raise ValueError("Position hors des limites de la grille.")
            if self.grille[x][y] is not None:
                raise ValueError("Position déjà occupée.")
        for x, y in positions:
            self.grille[x][y] = navire.nom
        navire.positions = positions
        self.navires.append(navire)

    def tirer(self, coordonnees):
        x, y = coordonnees
        if not (0 <= x < self.taille and 0 <= y < self.taille):
            raise ValueError("Tir hors des limites.")
        for navire in self.navires:
            if coordonnees in navire.positions:
                navire.touches.append(coordonnees)
                return "Touché" if not navire.est_coule() else f"Coulé: {navire.nom}"
        return "Manqué"

# Classe représentant un joueur
class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.plateau = Plateau()
        self.tirs_effectues = []

    def jouer(self, coordonnees, plateau_adverse):
        if coordonnees in self.tirs_effectues:
            raise ValueError("Case déjà visée.")
        self.tirs_effectues.append(coordonnees)
        return plateau_adverse.tirer(coordonnees)

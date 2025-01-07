import tkinter as tk
import random
import pygame
import time

# Classe représentant un navire
class Navire:
    def __init__(self, nom, taille):
        self.nom = nom  # Nom du navire
        self.taille = taille  # Taille du navire (nombre de cases occupées)
        self.positions = []  # Positions occupées par le navire
        self.touches = []  # Positions touchées par l'adversaire

    # Vérifie si le navire est entièrement coulé
    def est_coule(self):
        return set(self.positions) == set(self.touches)

# Classe représentant le plateau de jeu
class Plateau:
    def __init__(self, taille=10):
        self.taille = taille  # Taille du plateau (par défaut 10x10)
        self.grille = [[None for _ in range(taille)] for _ in range(taille)]  # Grille initiale vide
        self.navires = []  # Liste des navires placés sur le plateau

    # Place un navire sur le plateau à des positions spécifiques
    def placer_navire(self, navire, positions):
        if len(positions) != navire.taille:
            raise ValueError("Le nombre de positions ne correspond pas à la taille du navire.")

        # Vérifie si toutes les positions sont valides
        for x, y in positions:
            if not (0 <= x < self.taille and 0 <= y < self.taille):
                raise ValueError("Position hors des limites de la grille.")
            if self.grille[x][y] is not None:
                raise ValueError("Position déjà occupée.")

        # Place le navire sur les positions spécifiées
        for x, y in positions:
            self.grille[x][y] = navire.nom
        navire.positions = positions
        self.navires.append(navire)

    # Vérifie si les positions données sont libres
    def verifier_positions_libres(self, positions):
        for x, y in positions:
            if not (0 <= x < self.taille and 0 <= y < self.taille):
                return False
            if self.grille[x][y] is not None:
                return False
        return True

    # Génère un placement aléatoire pour un navire
    def generer_placement_aleatoire(self, navire):
        tentatives = 0
        max_tentatives = 100  # Limite pour éviter les boucles infinies
    
        while tentatives < max_tentatives:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                x = random.randint(0, self.taille - 1)
                y = random.randint(0, self.taille - navire.taille)
                positions = [(x, y + i) for i in range(navire.taille)]
            else:
                x = random.randint(0, self.taille - navire.taille)
                y = random.randint(0, self.taille - 1)
                positions = [(x + i, y) for i in range(navire.taille)]

            # Si les positions sont valides, place le navire
            if self.verifier_positions_libres(positions):
                self.placer_navire(navire, positions)
                return True
            
            tentatives += 1
        raise ValueError(f"Impossible de placer le navire {navire.nom} après {max_tentatives} tentatives")

    # Gère un tir sur une position donnée
    def tirer(self, coordonnees):
        x, y = coordonnees
        if not (0 <= x < self.taille and 0 <= y < self.taille):
            raise ValueError("Tir hors des limites de la grille.")

        for navire in self.navires:
            if coordonnees in navire.positions:
                navire.touches.append(coordonnees)
                return "Touché" if not navire.est_coule() else f"Coulé: {navire.nom}"
        return "Manqué"

# Classe représentant un joueur (humain ou ordinateur)
class Joueur:
    def __init__(self, nom):
        self.nom = nom  # Nom du joueur
        self.plateau = Plateau()  # Plateau du joueur
        self.tirs_effectues = []  # Liste des tirs déjà effectués
        self.tirs_reussis = 0  # Nombre de tirs réussis
        self.tirs_rates = 0  # Nombre de tirs ratés

    # Effectue un tir sur le plateau adverse
    def jouer(self, coordonnees, plateau_adverse):
        if coordonnees in self.tirs_effectues:
            raise ValueError("Case déjà visée.")
        self.tirs_effectues.append(coordonnees)
        resultat = plateau_adverse.tirer(coordonnees)
        if "Touché" in resultat or "Coulé" in resultat:
            self.tirs_reussis += 1
        else:
            self.tirs_rates += 1
        return resultat

    # Vérifie si le joueur a perdu (tous ses navires sont coulés)
    def a_perdu(self):
        perdu = all(navire.est_coule() for navire in self.plateau.navires)
        if perdu:
            print(f"{self.nom} a perdu: tous les navires sont coulés.")
        return perdu

# Classe représentant l'interface utilisateur pour le jeu de bataille navale
class InterfaceBatailleNavale:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")

        # Initialisation des sons pour les actions
        pygame.mixer.init()
        self.son_touche = pygame.mixer.Sound("touche.mp3")
        self.son_manque = pygame.mixer.Sound("manque.mp3")
        self.son_coule = pygame.mixer.Sound("coule.mp3")

        # Initialisation des joueurs (humain et ordinateur)
        self.joueur = Joueur("Joueur")
        self.ordinateur = Joueur("Ordinateur")

        # Grilles pour l'interface
        self.grille_joueur = [[None for _ in range(10)] for _ in range(10)]
        self.grille_ordinateur = [[None for _ in range(10)] for _ in range(10)]

        # Création des grilles visuelles
        self.creer_grille("Joueur", 0, 0, self.grille_joueur)
        self.creer_grille("Ordinateur", 0, 15, self.grille_ordinateur, joueur=False)

        # Interface de contrôle (nouvelle partie, niveau de difficulté, etc.)
        self.panneau_controle = tk.Frame(self.root)
        self.panneau_controle.grid(row=1, column=0, columnspan=30)

        self.bouton_nouvelle_partie = tk.Button(self.panneau_controle, text="Nouvelle Partie", command=self.nouvelle_partie)
        self.bouton_nouvelle_partie.pack(side=tk.LEFT, padx=10)

        self.indicateur_tour = tk.Label(self.panneau_controle, text="Tour du joueur")
        self.indicateur_tour.pack(side=tk.LEFT, padx=10)

        # Niveau de difficulté
        self.niveau_difficulte = tk.StringVar(value="Facile")
        self.radio_facile = tk.Radiobutton(self.panneau_controle, text="Facile", variable=self.niveau_difficulte, value="Facile")
        self.radio_facile.pack(side=tk.LEFT)
        self.radio_difficile = tk.Radiobutton(self.panneau_controle, text="Difficile", variable=self.niveau_difficulte, value="Difficile")
        self.radio_difficile.pack(side=tk.LEFT)

        # Orientation des navires
        self.orientation = "horizontal"
        self.bouton_horizontal = tk.Button(self.panneau_controle, text="Horizontal", command=self.set_orientation_horizontal)
        self.bouton_horizontal.pack(side=tk.LEFT, padx=10)

        self.bouton_vertical = tk.Button(self.panneau_controle, text="Vertical", command=self.set_orientation_vertical)
        self.bouton_vertical.pack(side=tk.LEFT, padx=10)

        # Liste des navires à placer pour le joueur
        self.navires_a_placer = [
            Navire("Porte-avions", 5),
            Navire("Croiseur", 4),
            Navire("Destroyer", 3),
            Navire("Destroyer", 3),
            Navire("Sous-marin", 2),
            Navire("Sous-marin", 2)
        ]
        self.navire_courant = None  # Navire en cours de placement
        self.mode_placement = True  # Mode de placement des navires
        self.tour_joueur = True  # Indique si c'est le tour du joueur
        self.tirs_ordinateur_potentiels = []  # Liste des cibles potentielles pour l'ordinateur

        # Compteurs pour les statistiques de tirs
        self.tirs_reussis_joueur = tk.IntVar(value=0)
        self.tirs_rates_joueur = tk.IntVar(value=0)
        self.tirs_reussis_ordinateur = tk.IntVar(value=0)
        self.tirs_rates_ordinateur = tk.IntVar(value=0)
        self.temps_debut = time.time()  # Temps de début de la partie

        # Panneau pour les informations de tirs et le temps de jeu
        self.panneau_stats = tk.Frame(self.root)
        self.panneau_stats.grid(row=2, column=0, columnspan=30, pady=10)

        # Étiquettes pour afficher les statistiques des tirs
        self.label_tirs_reussis_joueur = tk.Label(self.panneau_stats, text="Tirs réussis (Joueur):")
        self.label_tirs_reussis_joueur.pack(side=tk.LEFT, padx=10)
        self.valeur_tirs_reussis_joueur = tk.Label(self.panneau_stats, textvariable=self.tirs_reussis_joueur)
        self.valeur_tirs_reussis_joueur.pack(side=tk.LEFT, padx=10)

        self.label_tirs_rates_joueur = tk.Label(self.panneau_stats, text="Tirs ratés (Joueur):")
        self.label_tirs_rates_joueur.pack(side=tk.LEFT, padx=10)
        self.valeur_tirs_rates_joueur = tk.Label(self.panneau_stats, textvariable=self.tirs_rates_joueur)
        self.valeur_tirs_rates_joueur.pack(side=tk.LEFT, padx=10)

        self.label_tirs_reussis_ordinateur = tk.Label(self.panneau_stats, text="Tirs réussis (Ordinateur):")
        self.label_tirs_reussis_ordinateur.pack(side=tk.LEFT, padx=10)
        self.valeur_tirs_reussis_ordinateur = tk.Label(self.panneau_stats, textvariable=self.tirs_reussis_ordinateur)
        self.valeur_tirs_reussis_ordinateur.pack(side=tk.LEFT, padx=10)

        self.label_tirs_rates_ordinateur = tk.Label(self.panneau_stats, text="Tirs ratés (Ordinateur):")
        self.label_tirs_rates_ordinateur.pack(side=tk.LEFT, padx=10)
        self.valeur_tirs_rates_ordinateur = tk.Label(self.panneau_stats, textvariable=self.tirs_rates_ordinateur)
        self.valeur_tirs_rates_ordinateur.pack(side=tk.LEFT, padx=10)

        self.label_temps_total = tk.Label(self.panneau_stats, text="Temps de jeu: 0s")
        self.label_temps_total.pack(side=tk.LEFT, padx=10)

        # Mise à jour régulière du temps de jeu
        self.mettre_a_jour_temps()

    # Met à jour le temps de jeu toutes les secondes
    def mettre_a_jour_temps(self):
        temps_ecoule = int(time.time() - self.temps_debut)
        self.label_temps_total.config(text=f"Temps de jeu: {temps_ecoule}s")
        self.root.after(1000, self.mettre_a_jour_temps)

    # Création d'une grille pour l'interface
    def creer_grille(self, titre, row, col, grille, joueur=True):
        cadre = tk.Frame(self.root)
        cadre.grid(row=row, column=col, padx=10, pady=10)

        label = tk.Label(cadre, text=titre)
        label.grid(row=0, column=0, columnspan=10)

        for i in range(10):
            for j in range(10):
                bouton = tk.Button(cadre, width=3, height=2, bg="lightblue",
                                   command=lambda x=i, y=j: self.case_cliquee(x, y, joueur))
                bouton.grid(row=i + 1, column=j)
                grille[i][j] = bouton

    # Gère les actions lors du clic sur une case
    def case_cliquee(self, x, y, joueur):
        if joueur and self.mode_placement:
            self.placer_navire_joueur(x, y)
        elif not joueur and not self.mode_placement and self.tour_joueur:
            self.jouer_tour(x, y)

    # Définit l'orientation des navires sur horizontal
    def set_orientation_horizontal(self):
        self.orientation = "horizontal"
        print("Orientation définie sur Horizontal")

    # Définit l'orientation des navires sur vertical
    def set_orientation_vertical(self):
        self.orientation = "vertical"
        print("Orientation définie sur Vertical")

    # Place un navire pour le joueur
    def placer_navire_joueur(self, x, y):
        if not self.navire_courant:
            if self.navires_a_placer:
                self.navire_courant = self.navires_a_placer.pop(0)
                print(f"Placement de: {self.navire_courant.nom}")
            else:
                print("Tous les navires ont été placés!")
                self.mode_placement = False
                self.placer_navires_ordinateur()
                return

        try:
            if self.orientation == "horizontal":
                positions = [(x, y + i) for i in range(self.navire_courant.taille)]
            else:
                positions = [(x + i, y) for i in range(self.navire_courant.taille)]

            self.joueur.plateau.placer_navire(self.navire_courant, positions)
            for px, py in positions:
                self.grille_joueur[px][py].config(bg="black")
            self.navire_courant = None
        except ValueError as e:
            print(f"Erreur de placement: {e}")

    # Gère le tour du joueur
    def jouer_tour(self, x, y):
        try:
            resultat = self.joueur.jouer((x, y), self.ordinateur.plateau)
            if "Touché" in resultat:
                self.dessiner_croix(self.grille_ordinateur[x][y])
                print(resultat)
                self.son_touche.play()
                if "Coulé" in resultat:
                    self.son_coule.play()
                    print(f"Navire coulé : {resultat.split(': ')[1]}")
            else:
                self.dessiner_cercle(self.grille_ordinateur[x][y])
                print(resultat)
                self.son_manque.play()

            self.tirs_reussis_joueur.set(self.joueur.tirs_reussis)
            self.tirs_rates_joueur.set(self.joueur.tirs_rates)

            if self.ordinateur.a_perdu():
                print("Vous avez gagné!")
                self.indicateur_tour.config(text="Victoire du joueur!")
                return  # Arrêter le jeu si le joueur a gagné

            self.tour_joueur = False
            self.indicateur_tour.config(text="Tour de l'ordinateur")
            self.tir_ordinateur()

            # Vérifie si le joueur a perdu après le tir de l'ordinateur
            if self.joueur.a_perdu():
                print("L'ordinateur a gagné!")
                self.indicateur_tour.config(text="Défaite!")
        except ValueError as e:
            print(f"Erreur: {e}")

    # Dessine une croix rouge pour indiquer un tir réussi
    def dessiner_croix(self, bouton):
        canvas = tk.Canvas(bouton, width=20, height=20, bg="white", highlightthickness=0)
        canvas.create_line(2, 2, 18, 18, fill="red", width=2)
        canvas.create_line(2, 18, 18, 2, fill="red", width=2)
        canvas.pack()

    # Dessine un cercle bleu pour indiquer un tir manqué
    def dessiner_cercle(self, bouton):
        canvas = tk.Canvas(bouton, width=20, height=20, bg="white", highlightthickness=0)
        canvas.create_oval(2, 2, 18, 18, outline="blue", width=2)
        canvas.pack()

    # Gestion du tir de l'ordinateur
    def tir_ordinateur(self):
        if self.niveau_difficulte.get() == "Facile":
            self.tir_ordinateur_facile()
        else:
            self.tir_ordinateur_difficile()

    # Tir aléatoire pour l'ordinateur (mode facile)
    def tir_ordinateur_facile(self):
        while not self.tour_joueur:
            x, y = random.randint(0, 9), random.randint(0, 9)
            if (x, y) not in self.ordinateur.tirs_effectues:
                self.tirer_ordinateur(x, y)
                break

    # Tir stratégique pour l'ordinateur (mode difficile)
    def tir_ordinateur_difficile(self):
        while not self.tour_joueur:
            if self.tirs_ordinateur_potentiels:
                x, y = self.tirs_ordinateur_potentiels.pop(0)
            else:
                x, y = random.randint(0, 9), random.randint(0, 9)

            if (x, y) not in self.ordinateur.tirs_effectues:
                resultat = self.ordinateur.jouer((x, y), self.joueur.plateau)
                self.tirer_ordinateur(x, y, resultat)
                if "Touché" in resultat:
                    self.tirs_ordinateur_potentiels.extend(
                        [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                         if 0 <= x + dx < 10 and 0 <= y + dy < 10 and (x + dx, y + dy) not in self.ordinateur.tirs_effectues]
                    )
                break

    # Effectue un tir pour l'ordinateur et gère le résultat
    def tirer_ordinateur(self, x, y, resultat=None):
        if not resultat:
            resultat = self.ordinateur.jouer((x, y), self.joueur.plateau)

        if "Touché" in resultat:
            self.dessiner_croix(self.grille_joueur[x][y])
            print(f"Résultat du tir: {resultat}")
            self.son_touche.play()
        elif "Manqué" in resultat:
            self.dessiner_cercle(self.grille_joueur[x][y])
            print(f"Résultat du tir: {resultat}")
            self.son_manque.play()
        elif "Coulé" in resultat:
            self.dessiner_croix(self.grille_joueur[x][y])
            print(f"Résultat du tir: {resultat}")
            self.son_coule.play()

        self.tirs_reussis_ordinateur.set(self.ordinateur.tirs_reussis)
        self.tirs_rates_ordinateur.set(self.ordinateur.tirs_rates)

        if self.joueur.a_perdu():
            print("L'ordinateur a gagné!")
            self.indicateur_tour.config(text="Défaite!")
        else:
            self.tour_joueur = True
            self.indicateur_tour.config(text="Tour du joueur")

    # Place les navires pour l'ordinateur
    def placer_navires_ordinateur(self):
        navires_a_placer = [
            Navire("Porte-avions", 5),
            Navire("Croiseur", 4),
            Navire("Destroyer", 3),
            Navire("Destroyer", 3),
            Navire("Sous-marin", 2),
            Navire("Sous-marin", 2)
        ]
    
        for navire in navires_a_placer:
            try:
                self.ordinateur.plateau.generer_placement_aleatoire(navire)
            except ValueError as e:
                print(f"Erreur lors du placement du navire {navire.nom} de l'ordinateur : {e}")

    # Lance une nouvelle partie en réinitialisant toutes les variables
    def nouvelle_partie(self):
        print("Nouvelle partie lancée.")
        # Réinitialisation des variables de jeu
        self.mode_placement = True
        self.navires_a_placer = [
            Navire("Porte-avions", 5),
            Navire("Croiseur", 4),
            Navire("Destroyer", 3),
            Navire("Destroyer", 3),
            Navire("Sous-marin", 2),
            Navire("Sous-marin", 2)
        ]
        self.navire_courant = None
        self.joueur = Joueur("Joueur")
        self.ordinateur = Joueur("Ordinateur")
        self.tirs_ordinateur_potentiels = []
        self.tour_joueur = True
        self.indicateur_tour.config(text="Tour du joueur")

        # Réinitialisation des compteurs de tirs
        self.tirs_reussis_joueur.set(0)
        self.tirs_rates_joueur.set(0)
        self.tirs_reussis_ordinateur.set(0)
        self.tirs_rates_ordinateur.set(0)

        # Réinitialisation du temps de jeu
        self.temps_debut = time.time()

        # Réinitialisation des grilles visuelles
        for i in range(10):
            for j in range(10):
                # Grille du joueur
                self.grille_joueur[i][j].config(bg="lightblue", state=tk.NORMAL)
                for child in self.grille_joueur[i][j].winfo_children():
                    child.destroy()

                # Grille de l'ordinateur
                self.grille_ordinateur[i][j].config(bg="lightblue", state=tk.NORMAL)
                for child in self.grille_ordinateur[i][j].winfo_children():
                    child.destroy()

        # Réinitialisation des navires de l'ordinateur
        self.ordinateur.plateau.navires = []
        self.ordinateur.plateau.grille = [[None for _ in range(10)] for _ in range(10)]

        # Réinitialisation de l'orientation par défaut à "horizontal"
        self.orientation = "horizontal"
        self.bouton_horizontal.config(relief=tk.SUNKEN)
        self.bouton_vertical.config(relief=tk.RAISED)

        # Replacer les navires de l'ordinateur
        self.placer_navires_ordinateur()

# Point d'entrée principal pour exécuter l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBatailleNavale(root)
    root.mainloop()

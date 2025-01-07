# Phase 2 : Interface utilisateur
import tkinter as tk
from phase_1_classes import Plateau, Joueur, Navire

class InterfaceBatailleNavale:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")

        self.grille_joueur = [[None for _ in range(10)] for _ in range(10)]
        self.grille_ordinateur = [[None for _ in range(10)] for _ in range(10)]

        self.creer_grille("Joueur", 0, 0, self.grille_joueur)
        self.creer_grille("Ordinateur", 0, 15, self.grille_ordinateur)

    def creer_grille(self, titre, row, col, grille):
        cadre = tk.Frame(self.root)
        cadre.grid(row=row, column=col, padx=10, pady=10)

        label = tk.Label(cadre, text=titre)
        label.grid(row=0, column=0, columnspan=10)

        for i in range(10):
            for j in range(10):
                bouton = tk.Button(cadre, width=3, height=2, bg="lightblue")
                bouton.grid(row=i + 1, column=j)
                grille[i][j] = bouton

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBatailleNavale(root)
    root.mainloop()

# Phase 3 : Placement des navires
from phase_2_interface import InterfaceBatailleNavale
from phase_1_classes import Navire

class InterfaceBatailleNavale(InterfaceBatailleNavale):
    def __init__(self, root):
        super().__init__(root)
        self.joueur = Joueur("Joueur")
        self.placer_navires_joueur()

    def placer_navires_joueur(self):
        navires = [
            Navire("Porte-avions", 5),
            Navire("Croiseur", 4),
            Navire("Destroyer", 3),
            Navire("Sous-marin", 2)
        ]
        for navire in navires:
            self.joueur.plateau.placer_navire(navire, [(0, i) for i in range(navire.taille)])
        print("Navires placés pour le joueur.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBatailleNavale(root)
    root.mainloop()

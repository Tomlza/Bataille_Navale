# Phase 4 : Logique de jeu
from phase_3_placement import InterfaceBatailleNavale

class InterfaceBatailleNavale(InterfaceBatailleNavale):
    def jouer_tour(self, x, y):
        resultat = self.joueur.jouer((x, y), self.joueur.plateau)
        if "Touché" in resultat:
            print("Touché !")
        elif "Coulé" in resultat:
            print(f"Navire coulé : {resultat.split(': ')[1]}")
        else:
            print("Manqué !")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBatailleNavale(root)
    root.mainloop()

# Phase 5 : Bonus et améliorations
import pygame
from phase_4_logique import InterfaceBatailleNavale

class InterfaceBatailleNavale(InterfaceBatailleNavale):
    def __init__(self, root):
        pygame.mixer.init()
        self.son_touche = pygame.mixer.Sound("touche.mp3")
        self.son_manque = pygame.mixer.Sound("manque.mp3")
        self.son_coule = pygame.mixer.Sound("coule.mp3")
        super().__init__(root)

    def jouer_tour(self, x, y):
        resultat = super().jouer_tour(x, y)
        if "Touché" in resultat:
            self.son_touche.play()
        elif "Coulé" in resultat:
            self.son_coule.play()
        else:
            self.son_manque.play()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBatailleNavale(root)
    root.mainloop()

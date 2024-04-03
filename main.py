"""
NOM : LIEFFERINCKX
PRÉNOM : Romain
SECTION : INFO
MATRICULE : 000591790
"""
from PySide6.QtWidgets import QApplication
from window import Ui_Form
"""
Date de remise: intermédiaire: 10/03/2024
                finale: 24/03/2024
Nom du projet: Projet 2 – Représentation et compression d’images
Description: Ce programme est chargé de lire, d’écrire, d’afficher et de compresser des images. En utilisant le format
de fichier ulbmp, ulbmp2, ulbmp3 et ulbmp4 et la compression rle ou une sorte de compression QOI.
Le programme doit comprendre une interface graphique qui permet à l'utilisateur de charger les images, de les afficher,
de les compresser et de les enregistrer dans un dossier au choix.
l'enregistrement doit comprendre une boîte de dialogue qui demande à l'utilisateur dans quel fichier enregistré l'image.
De plus, l'interface doit afficher le nombre de couleurs total de l'image.
Ce projet est composé du fichier main.py, window.py, image.py, pixel.py et encoding.py.
"""

if __name__ == "__main__":
    app = QApplication([])  # Création d'une instance de QApplication
    window = Ui_Form()  # Création de la fenêtre Ui_Form
    window.show()  # Affichage de la fenêtre
    app.exec()  # Exécution de l'application

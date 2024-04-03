"""
NOM : LIEFFERINCKX
PRÉNOM : Romain
SECTION : INFO
MATRICULE : 000591790
"""

from PySide6.QtWidgets import QPushButton, QWidget, QFileDialog, QLabel, QVBoxLayout, QErrorMessage, QComboBox
from PySide6.QtGui import QImage, QPixmap, QColor
from PySide6.QtCore import Qt
from encoding import Encoder, Decoder


class Ui_Form(QWidget):
    """
    Classe Ui_Form: cette classe représente l'interface graphique du programme. Elle contient les attributs suivants:
    """
    def __init__(self):
        """
        initialisation des attributs de la classe Ui_Form
        """
        super().__init__()
        self.pushButton = None
        self.pushButton_2 = None
        self.image = None
        self.image_label = QLabel()
        self.depth_combo_box = QComboBox()
        self.rle_combo_box = QComboBox()
        self.version_combo_box = QComboBox()
        self.color_label = QLabel()
        self.error_dialog = QErrorMessage()
        self.setupUi()
        self.version = None

    def setupUi(self):
        """
        Configuration de l'interface graphique
        """
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowTitle("Image ULBMP Viewer")
        layout = QVBoxLayout(self)
        button_style = "QPushButton { color: white; border: none; padding: 10px 20px; font-size: 16px; }"
        button_style += "QPushButton:enabled { background-color: purple; }"
        disabled_button_style = "QPushButton:disabled { color: lightgray; }"
        self.setStyleSheet(button_style + disabled_button_style)
        self.pushButton = QPushButton("Load Image")
        self.pushButton.clicked.connect(self.ouverture_image_fichier)
        layout.addWidget(self.pushButton)  # Bouton Load Image
        layout.addWidget(self.image_label)
        layout.addWidget(self.color_label)
        layout.addWidget(self.depth_combo_box)
        layout.addWidget(self.rle_combo_box)
        layout.addWidget(self.version_combo_box)
        self.pushButton_2 = QPushButton("Save Image")  # Bouton Save Image
        self.pushButton_2.clicked.connect(self.sauvegarde_image)
        self.pushButton_2.setEnabled(False)
        layout.addWidget(self.pushButton_2)
        layout.addWidget(self.color_label)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)
        label_style = "QLabel { border: 2px solid gray; padding: 5px; }"
        self.image_label.setStyleSheet(label_style)
        self.depth_combo_box.addItem("Depth 1")  # Configuration des QComboBox
        self.depth_combo_box.addItem("Depth 2")
        self.depth_combo_box.addItem("Depth 4")
        self.depth_combo_box.addItem("Depth 8")
        self.depth_combo_box.addItem("Depth 24")
        self.depth_combo_box.setEnabled(False)  # Désactiver par défaut
        self.rle_combo_box.addItem("RLE: Off")
        self.rle_combo_box.addItem("RLE: On")
        self.rle_combo_box.setEnabled(False)  # Désactive le bouton par défaut
        self.version_combo_box.addItem("ULBMP 1")
        self.version_combo_box.addItem("ULBMP 2")
        self.version_combo_box.addItem("ULBMP 3")
        self.version_combo_box.addItem("ULBMP 4")
        self.version_combo_box.currentIndexChanged.connect(self.changement_de_version)
        self.depth_combo_box.currentIndexChanged.connect(self.changement_de_profondeur)

    def changement_de_version(self, index):
        """
        Désactive le bouton RLE en fonction de la version ou de la profondeur.
        :param index: Index de la version sélectionnée.
        """
        version = index + 1
        if version == 3:
            self.depth_combo_box.setEnabled(True)
            self.rle_combo_box.setEnabled(True)
        else:
            self.depth_combo_box.setEnabled(False)
            self.rle_combo_box.setEnabled(False)
            self.rle_combo_box.setCurrentIndex(0)  # Remet l'option RLE à "Off" lorsque la version n'est pas ULBMP 3
            self.depth_combo_box.setCurrentIndex(4)  # Met Depth à 24 quand la version n'est pas ULBMP 3
        # Désactive l'option RLE si la profondeur est 1, 2 ou 4
        depth_index = self.depth_combo_box.currentIndex()
        if depth_index in [0, 1, 2]:
            self.rle_combo_box.setEnabled(False)
            self.rle_combo_box.setCurrentIndex(0)  # Remet l'option RLE à "Off" lorsque la profondeur est 1, 2 ou 4
        # Désactive l'option RLE si la version est égal à ULBMP 1 ou 2
        if version in [1, 2, 4]:
            self.rle_combo_box.setEnabled(False)
            self.rle_combo_box.setCurrentIndex(0)  # Remet l'option RLE à Off lorsque la version est ULBMP 1 ou 2
    def changement_de_profondeur(self, index):
        """
        Désactive le bouton RLE si la profondeur est égale à 1, 2 ou 4.
        :param index: Index de la profondeur sélectionnée.
        """
        depth_index = index
        if depth_index in [0, 1, 2]:
            self.rle_combo_box.setEnabled(False)
            self.rle_combo_box.setCurrentIndex(0)
        else:
            self.rle_combo_box.setEnabled(True)
    def ouverture_image_fichier(self):
        """
        Charge une image dans les formats ulbmp(1, 2, 3 ou 4) depuis un fichier.
        """
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.ulbmp *.ulbmp1 *.ulbmp2 *.ulbmp3 *.ulbmp4)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.exec_()
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            chemin_fichier = selected_files[0]
            try:
                self.chargement_image(chemin_fichier)
            except Exception as e:
                self.envoi_message_erreur(e)
    def chargement_image(self, chemin_fichier):
        """
        Charge l'image depuis le chemin du fichier spécifié.
        :param chemin_fichier: Chemin du fichier à charger.
        """
        self.image = Decoder.load_from(chemin_fichier)
        self.affichage_image(self.image)
        self.nombre_tot_couleurs()
        self.pushButton_2.setEnabled(True)
        self.adjustSize()
    def envoi_message_erreur(self, e):
        """
        Affiche un message d'erreur dans une boîte de dialogue si il y en a besoin.
        :param e: Exception à afficher.
        """
        self.error_dialog.showMessage(f"Erreur de chargement de l'image: {e}")
        self.color_label.hide()

    def nombre_tot_couleurs(self):
        """
        Affiche le nombre total de couleurs dans l'image.
        """
        if self.image:
            num_colors = len(set((pixel.red, pixel.green, pixel.blue) for pixel in self.image.pixels))
            self.color_label.setText(f"Nombre de couleurs: {num_colors}")
            self.color_label.show()
        else:
            self.color_label.hide()
    def sauvegarde_image(self):
        """
        Sauvegarde l'image dans un fichier ulbmp(1, 2, 3 ou 4) spécifié par l'utilisateur.
        Si la version est 3, la profondeur et l'option RLE sont prises en compte et demandées à l'utilisateur.
        """
        dico_profondeur = {0: 1, 1: 2, 2: 4, 3: 8, 4: 24}
        file_dialog = QFileDialog(self)
        version = self.version_combo_box.currentIndex() + 1
        file_dialog.setNameFilter(f"ULBMP{version} files (*.ulbmp{version})")
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                chemin_fichier = selected_files[0]
                if not chemin_fichier.endswith(f".ulbmp{version}"):
                    chemin_fichier += f".ulbmp{version}"
                try:
                    depth_index = self.depth_combo_box.currentIndex()
                    depth = dico_profondeur.get(depth_index)
                    rle = self.rle_combo_box.currentIndex()
                    if version == 3 and depth in [1, 2, 4, 8, 24]:
                        encoder = Encoder(self.image, version=version, depth=depth, rle=bool(rle))
                    else:
                        encoder = Encoder(self.image, version=version, depth=None, rle=False)
                    encoder.save_to(chemin_fichier)
                except Exception as e:
                    self.error_dialog.showMessage(f"Erreur de sauvegarde de l'image: {e}")
    def affichage_image(self, image):  # Affiche l'image dans l'interface graphique
        """
        Affiche l'image dans l'interface graphique
        :param image: Image à afficher.
        """
        qimage = QImage(image.width, image.height, QImage.Format_RGB888)
        for compte in range(image.width * image.height):
            x = compte % image.width
            y = compte // image.width
            pixel = image.pixels[compte]
            qimage.setPixelColor(x, y, QColor(pixel.red, pixel.green, pixel.blue))
        pixmap = QPixmap(qimage)
        self.image_label.setPixmap(pixmap)

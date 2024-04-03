"""
NOM : LIEFFERINCKX
PRÉNOM : Romain
SECTION : INFO
MATRICULE : 000591790
"""

from image import Image
from pixel import Pixel


class Decoder:
    """
    Classe Decoder: Cette classe est chargée d'ouvrir et s'il faut décompresser une image.
    """

    @staticmethod
    def load_from(path):
        """
        charge une image à partir d'un fichier avec comme extension .ulbmp (1, 2, 3, 4).
        :param path: chemin du fichier à charger.
        :return: image chargée.
        """
        with open(path, "rb") as file:
            header = file.read(5)  # lecture des 5 premiers octets
            if header != b"ULBMP":  # si les 5 premiers octets ne sont pas égaux à ULBMP lève une erreur
                raise ValueError
            version_ulbmp = int.from_bytes(file.read(1))  # lecture de la version du fichier
            image_chargee = Decoder.decode_ulbmp(file, version_ulbmp)  # appel de la méthode decode_ulbmp
            return image_chargee

    @staticmethod
    def lecture_header_v1v2v4(file):
        """
        lecture du header pour les versions 1, 2 et 4.
        :param file: fichier à lire.
        :return: longueur_du_header, width, height.
        """
        longueur_du_header = int.from_bytes(file.read(2), "little")
        width = int.from_bytes(file.read(2), "little")
        height = int.from_bytes(file.read(2), "little")
        return longueur_du_header, width, height

    @staticmethod
    def decode_ulbmp(file, version):
        """
        décode un fichier ulbmp en fonction de sa version.
        :param file: fichier à lire.
        :param version: version du fichier.
        :return: image décodée.
        """
        # clé: version, valeur: fonction de décodage
        dico_versions_decode = {1: Decoder.lecture_pixels_v1, 2: Decoder.lecture_pixels_v2, 3:
            lambda f: Decoder.lecture_pixels_v3(f, width, height, profondeur_encodage, byte_pour_rle, palette),
                                4: Decoder.lecture_pixels_v4}
        if version in [1, 2, 4]:
            longueur_du_header, width, height = Decoder.lecture_header_v1v2v4(file)
        elif version == 3:
            (longueur_du_header, width, height, profondeur_encodage, byte_pour_rle,
             palette) = Decoder.lecture_header_v3(file)
        pixels = dico_versions_decode[version](file)
        return Image(width, height, pixels)

    @staticmethod
    def lecture_pixels_v1(file):
        """
        lit les pixels de la version 1.
        :param file: fichier à lire.
        :return: liste des pixels.
        """
        pixels = []
        while suite_pix := file.read(3):  # si file.read(3) est vide, la boucle s'arrête
            red, green, blue = suite_pix[0], suite_pix[1], suite_pix[2]
            pixel = Pixel(red, green, blue)
            pixels.append(pixel)
        return pixels

    @staticmethod
    def lecture_pixels_v2(file):
        """
        lit les pixels de la version 2.
        :param file: fichier à lire.
        :return: liste des pixels.
        """
        pixels = []
        suite_donnees = file.read()
        for infos in range(0, len(suite_donnees), 4):
            infos = suite_donnees[infos: infos + 4]
            repetition, red, green, blue = infos
            pixel = Pixel(red, green, blue)
            pixels.extend([pixel] * repetition)
        return pixels

    @staticmethod
    def lecture_header_v3(file):
        """
        lit le header de la version 3.
        :param file: fichier à lire.
        :return: longueur du header, largeur et hauteur de l'image, profondeur d'encodage, byte pour RLE, palette.
        """
        longueur_du_header, width, height, profondeur_encodage, byte_pour_rle = Decoder.valider_header_v3(file)
        palette = Decoder.lecture_palette_v3(file, profondeur_encodage, longueur_du_header)
        return longueur_du_header, width, height, profondeur_encodage, byte_pour_rle, palette

    @staticmethod
    def valider_header_v3(file):
        """
        valide le header de la version 3.
        :param file: fichier à valider.
        :return: longueur du header, largeur et hauteur de l'image, profondeur d'encodage, byte pour RLE.
        """
        longueur_du_header = int.from_bytes(file.read(2), "little")
        width = int.from_bytes(file.read(2), "little")
        height = int.from_bytes(file.read(2), "little")
        profondeur_encodage = int.from_bytes(file.read(1))
        byte_pour_rle = int.from_bytes(file.read(1))
        if not ((byte_pour_rle in [0, 1]) and
                ((byte_pour_rle == 1 and profondeur_encodage in [8, 24]) or
                 (byte_pour_rle == 0 and profondeur_encodage in [1, 2, 4, 8, 24]))):
            raise ValueError
        return longueur_du_header, width, height, profondeur_encodage, byte_pour_rle

    @staticmethod
    def lecture_palette_v3(file, profondeur_encodage, longueur_du_header):
        """
        lit la palette de la version 3.
        :param file: fichier à lire.
        :param profondeur_encodage: profondeur d'encodage de l'image.
        :param longueur_du_header: longueur du header de l'image.
        :return: palette de l'image.
        """
        if profondeur_encodage in [1, 2, 4, 8]:
            taille_palette = (longueur_du_header - 14)
        else:
            taille_palette = 0
        palette = file.read(taille_palette)
        return palette

    @staticmethod
    def lecture_pixels_v3(file, width, height, profondeur, rle=False, palette=None):
        """
        lit les pixels de la version 3.
        :param file: fichier à lire.
        :param width: largeur de l'image.
        :param height: hauteur de l'image.
        :param profondeur: profondeur d'encodage de l'image.
        :param rle: indicateur RLE.
        :param palette: palette de l'image.
        :return: liste des pixels.
        """
        # clé: profondeur, valeur: fonction de lecture des pixels
        lecteur_pixel = {1: lambda f, w, h, p: Decoder.lecture_pixels_profondeur_1_2_4_8(f, w, h, p, 1),
                         2: lambda f, w, h, p: Decoder.lecture_pixels_profondeur_1_2_4_8(f, w, h, p, 2),
                         4: lambda f, w, h, p: Decoder.lecture_pixels_profondeur_1_2_4_8(f, w, h, p, 4),
                         8: lambda f, w, h, p: Decoder.lecture_pixels_profondeur_1_2_4_8(f, w, h, p, 8)
                         if not rle else Decoder.lecture_pixels_rle_profondeur_8(f, p), 24: lambda f, w, h, _:
            Decoder.lecture_pixels_v1(f) if not rle else Decoder.lecture_pixels_v2(f)}
        return lecteur_pixel[profondeur](file, width, height, palette)

    @staticmethod
    def lecture_pixels_profondeur_1_2_4_8(file, width, height, palette, profondeur):
        """
        Lit les pixels de profondeur 1, 2, 4 et 8 sans RLE pour 8.
        :param file: fichier à lire.
        :param width: largeur de l'image.
        :param height: hauteur de l'image.
        :param palette: palette de l'image.
        :param profondeur: profondeur d'encodage de l'image.
        :return: liste des pixels.
        """
        pixels = []
        for i in range(height * width):
            if i % (8 // profondeur) == 0:
                byte = int.from_bytes(file.read(1))
            infos = (byte >> ((8 // profondeur - 1 - i % (8 // profondeur)) * profondeur)) & ((1 << profondeur) - 1)
            red, green, blue = palette[infos * 3:infos * 3 + 3]
            pixel = Pixel(red, green, blue)
            pixels.append(pixel)
        return pixels[:width * height]

    @staticmethod
    def lecture_pixels_rle_profondeur_8(file, palette):
        """
        lit les pixels en profondeur 8 avec RLE.
        :param file: fichier à lire.
        :param palette: palette de l'image.
        :return: liste des pixels.
        """
        pixels = []
        suite_donnees = file.read()
        for infos in range(0, len(suite_donnees), 2):
            repetition = suite_donnees[infos]
            couleur = suite_donnees[infos + 1]
            red, green, blue = palette[couleur * 3: couleur * 3 + 3]
            pixel = Pixel(red, green, blue)
            pixels.extend([pixel] * repetition)
        return pixels

    @staticmethod
    def decode_new_pix(suite_donnees, pixel_position):
        """
        décode un nouveau pixel lorsqu'il est trop éloigné en valeur RGB.
        :param suite_donnees: suite de données à décoder.
        :param pixel_position: position du pixel à décoder.
        :return: valeurs RGB du pixel et nouvelle position du pixel.
        """
        red, green, blue = suite_donnees[pixel_position + 1: pixel_position + 4]
        pixel_position += 4
        return red, green, blue, pixel_position

    @staticmethod
    def decode_small_diff(suite_donnees, pixel_position, premier_pixel):
        """
        décode une petite différence entre les valeurs RGB des pixels.
        :param suite_donnees: suite de données à décoder.
        :param pixel_position: position du pixel à décoder.
        :param premier_pixel: premier pixel de la suite de données.
        :return: valeurs RGB du pixel et nouvelle position du pixel.
        """
        byte = suite_donnees[pixel_position]
        decalage_r = (byte & 0b00110000) >> 4
        decalage_g = (byte & 0b00001100) >> 2
        decalage_b = (byte & 0b00000011)
        red = decalage_r + premier_pixel.red - 2
        green = decalage_g + premier_pixel.green - 2
        blue = decalage_b + premier_pixel.blue - 2
        pixel_position += 1
        return red, green, blue, pixel_position

    @staticmethod
    def decode_inter_diff(suite_donnees, pixel_position, premier_pixel):
        """
        décode une différence intermédiaire dans les valeurs RGB des pixels.
        :param suite_donnees: suite de données à décoder.
        :param pixel_position: position du pixel à décoder.
        :param premier_pixel: premier pixel de la suite de données.
        :return: valeurs RGB du pixel et nouvelle position du pixel.
        """
        byte1, byte2 = suite_donnees[pixel_position: pixel_position + 2]
        decalage_g = (byte1 & 0b00111111)
        decalage_rg = (byte2 & 0b11110000) >> 4
        decalage_bg = (byte2 & 0b00001111)
        red = decalage_rg + premier_pixel.red + decalage_g - 8 - 32
        green = decalage_g + premier_pixel.green - 32
        blue = decalage_bg + premier_pixel.blue + decalage_g - 8 - 32
        pixel_position += 2
        return red, green, blue, pixel_position

    @staticmethod
    def decode_big_diff(suite_donnees, pixel_position, premier_pixel):
        """
        décode une grande différence dans les valeurs RGB des pixels et envoie a
        la fonction associée au tyoe de big_diff.
        :param suite_donnees: suite de données à décoder.
        :param pixel_position: position du pixel à décoder.
        :param premier_pixel: premier pixel de la suite de données.
        :return: valeurs RGB du pixel et nouvelle position du pixel.
        """
        byte = suite_donnees[pixel_position]
        if byte < 144:  # big diff r
            red, green, blue, pixel_position = Decoder.decode_big_diff_r(suite_donnees, pixel_position, premier_pixel)
        elif 144 <= byte < 160:  # big diff g
            red, green, blue, pixel_position = Decoder.decode_big_diff_g(suite_donnees, pixel_position, premier_pixel)
        elif 159 < byte < 176:  # big diff b
            red, green, blue, pixel_position = Decoder.decode_big_diff_b(suite_donnees, pixel_position, premier_pixel)
        return red, green, blue, pixel_position

    @staticmethod
    def decode_big_diff_r(suite_donnees, pixel_position, premier_pixel):
        """
        décode une grande différence dans les valeurs RGB des pixels pour la composante rouge.
        :param suite_donnees: suite de données à décoder.
        :param pixel_position: position du pixel à décoder.
        :param premier_pixel: premier pixel de la suite de données.
        :return: valeurs RGB du pixel et nouvelle position du pixel.
        """
        byte1, byte2, byte3 = suite_donnees[pixel_position: pixel_position + 3]
        decalage_r = (byte1 & 0b00001111) << 4 | (byte2 & 0b11110000) >> 4
        decalage_gr = ((byte2 & 0b00001111) << 2) | ((byte3 & 0b11000000) >> 6)
        decalage_br = (byte3 & 0b00111111)
        red = decalage_r + premier_pixel.red - 128
        green = decalage_gr + decalage_r - 32 - 128 + premier_pixel.green
        blue = decalage_br + decalage_r - 32 - 128 + premier_pixel.blue
        pixel_position += 3
        return red, green, blue, pixel_position

    @staticmethod
    def decode_big_diff_g(suite_donnees, pixel_position, premier_pixel):
        """
        décode une grande différence dans les valeurs RGB des pixels pour la composante verte.
        :param suite_donnees: suite de données à décoder.
        :param pixel_position: position du pixel à décoder.
        :param premier_pixel: premier pixel de la suite de données.
        :return: valeurs RGB du pixel et nouvelle position du pixel.
        """
        byte1, byte2, byte3 = suite_donnees[pixel_position: pixel_position + 3]
        decalage_g = (byte1 & 0b00001111) << 4 | (byte2 & 0b11110000) >> 4
        decalage_rg = ((byte2 & 0b00001111) << 2) | ((byte3 & 0b11000000) >> 6)
        decalage_bg = (byte3 & 0b00111111)
        red = decalage_rg + decalage_g + premier_pixel.red - 32 - 128
        green = decalage_g + premier_pixel.green - 128
        blue = decalage_bg + premier_pixel.blue + decalage_g - 32 - 128
        pixel_position += 3
        return red, green, blue, pixel_position

    @staticmethod
    def decode_big_diff_b(suite_donnees, pixel_position, premier_pixel):
        """
        décode une grande différence dans les valeurs RGB des pixels pour la composante bleue.
        :param suite_donnees: suite de données à décoder.
        :param pixel_position: position du pixel à décoder.
        :param premier_pixel: premier pixel de la suite de données.
        :return: valeurs RGB du pixel et nouvelle position du pixel.
        """
        byte1, byte2, byte3 = suite_donnees[pixel_position: pixel_position + 3]
        decalage_b = (byte1 & 0b00001111) << 4 | (byte2 & 0b11110000) >> 4
        decalage_rb = ((byte2 & 0b00001111) << 2) | ((byte3 & 0b11000000) >> 6)
        decalage_gb = (byte3 & 0b00111111)
        red = decalage_rb + decalage_b + premier_pixel.red - 32 - 128
        green = decalage_b + decalage_gb + premier_pixel.green - 32 - 128
        blue = decalage_b + premier_pixel.blue - 128
        pixel_position += 3
        return red, green, blue, pixel_position

    @staticmethod
    def lecture_pixels_v4(file):
        """
        lit les pixels de la version 4 et renvoie une fonction pour lire les pixels adaptée a la diff
        :param file: fichier à lire.
        :return: liste des pixels.
        """
        premier_pix = Pixel(0, 0, 0)
        pixels = []
        suite_donnees = file.read()
        pixel_position = 0
        while pixel_position < len(suite_donnees):
            byte = suite_donnees[pixel_position]
            if byte == 255:  # new pix
                red, green, blue, pixel_position = Decoder.decode_new_pix(suite_donnees, pixel_position)
            elif byte < 64:  # small diff
                red, green, blue, pixel_position = Decoder.decode_small_diff(suite_donnees, pixel_position, premier_pix)
            elif 63 < byte < 128:  # intermediate diff
                red, green, blue, pixel_position = Decoder.decode_inter_diff(suite_donnees, pixel_position, premier_pix)
            elif 127 < byte < 255:  # big diff
                red, green, blue, pixel_position = Decoder.decode_big_diff(suite_donnees, pixel_position, premier_pix)
            pixel = Pixel(red, green, blue)
            pixels.append(pixel)
            premier_pix = Pixel(red, green, blue)
        return pixels


class Encoder:
    """
    Classe Encoder: Cette classe s'occuppe de sauvegarder avec ou sans compression une image.
    """

    def __init__(self, image, version=1, **kwargs):
        """
        initialisation des attributs de la classe Encoder.
        :param image: image à sauvegarder.
        :param version: version du fichier à sauvegarder.
        :param kwargs: profondeur, rle.
        """
        self.image = image
        self.version_ulbmp = version
        self.profondeur = kwargs.get("depth", None)
        self.rle = kwargs.get("rle", None)
        self.palette = self.creation_palette()

    def save_to(self, path):
        """
        sauvegarde l'image sur l'ordinateur grace a un chemin donné par l'utilisateur.
        :param path: chemin dans l'odinateur ou sauvegarder le fichier.
        :return: fichier sauvegardé ou une erreur.
        """
        try:
            byte_fichier = b"ULBMP"
            byte_fichier += self.to_bytes(self.version_ulbmp)
            byte_fichier += self.encode_header()
            byte_fichier += self.to_bytes(self.image.width, 2)
            byte_fichier += self.to_bytes(self.image.height, 2)
            dico_versions_encode = {1: self.encode_pixels_v1, 2: self.encode_pixels_v2, 3: self.encode_pixels_v3,
                                    4: self.encode_pixels_v4}
            byte_fichier += dico_versions_encode[self.version_ulbmp]()
            with open(path, "wb") as file:
                file.write(byte_fichier)
        except Exception as e:
            raise e

    @staticmethod
    def to_bytes(valeur, longueur=1, ordre_bytes="little"):
        """
        convertit une valeur en bytes.
        :param valeur: valeur à convertir.
        :param longueur: longueur des bytes.
        :param ordre_bytes: ordre des bytes.
        :return: valeur convertie en bytes.
        """
        return valeur.to_bytes(longueur, ordre_bytes)

    def encode_header(self):
        """
        encode le header du fichier ulbmp.
        :return: header encodé.
        """
        if self.version_ulbmp in [1, 2, 4]:
            return self.to_bytes(12, 2)
        elif self.version_ulbmp == 3:
            return self.to_bytes(14 + self.calcul_taille_palette, 2)

    def encode_pixels_v1(self):
        """
        encode les pixels de la version 1.
        :return: pixels encodés.
        """
        byte_fichier = bytearray()
        for pixel in self.image.pixels:
            byte_fichier.extend([pixel.red, pixel.green, pixel.blue])
        return byte_fichier

    def encode_pixels_v2(self):
        """
        encode les pixels de la version 2.
        :return: pixels encodés.
        """
        return self.encodage_rle_v2()

    def encode_pixels_v3(self):
        """
        commence l'encodage de la version 3 et fais appel au fonctions pour encoder les profondeurs.
        :return: pixels encodés.
        """
        byte_fichier = bytearray()
        byte_fichier += self.profondeur.to_bytes(1)
        byte_fichier += self.rle.to_bytes(1)
        total_couleurs = len(set((pixel.red, pixel.green, pixel.blue) for pixel in self.image.pixels))
        max_couleurs_possible = 2 ** self.profondeur
        if total_couleurs > max_couleurs_possible:
            raise ValueError
        if self.profondeur != 24:
            byte_fichier += self.encode_palette()
        # clé: (profondeur, rle), valeur: fonction d'encodage
        dico_encodage_profondeur = {(1, 0): lambda: self.encodage_profondeur_1(), (2, 0): lambda:
        self.encodage_profondeur_2(), (4, 0): lambda: self.encodage_profondeur_4(), (8, 0): lambda:
        self.encodage_profondeur_8(), (8, 1): lambda: self.encodage_profondeur_8_avec_rle(), (24, 0): lambda:
        self.encode_pixels_v1(), (24, 1): lambda: self.encodage_rle_v2()}
        byte_fichier += dico_encodage_profondeur[(self.profondeur, self.rle)]()
        return byte_fichier

    def encode_pixels_v4(self):
        """
        :return encode_pixels_v4_suite
        """
        return self.encode_pixels_v4_suite()

    def encode_palette(self):
        """
        encode la palette de l'image.
        :return: palette encodée.
        """
        byte_calcul_palette = bytearray()
        for pixel in self.palette:
            byte_calcul_palette.extend([pixel.red, pixel.green, pixel.blue])
        return byte_calcul_palette

    @property
    def calcul_taille_palette(self):
        """
        calcule la taille de la palette.
        :return: taille de la palette.
        """
        nombre_couleurs = len(set((pixel.red, pixel.green, pixel.blue) for pixel in self.image.pixels))
        taille = 0
        if self.profondeur == 1 or self.profondeur == 2 or self.profondeur == 4 or self.profondeur == 8:
            taille = nombre_couleurs * 3
        elif self.profondeur == 24:
            taille = 0
        return taille

    def encodage_rle_v2(self):
        """
        encode les pixels avec la compression RLE pour la version 2.
        :return: pixels encodés.
        """
        byte_fichier = bytearray()
        pixel_precedent = None
        compte = 0
        for pixel in self.image.pixels:
            if pixel != pixel_precedent or compte == 255:
                if pixel_precedent is not None:
                    byte_fichier.extend([compte, pixel_precedent.red, pixel_precedent.green, pixel_precedent.blue])
                pixel_precedent = pixel
                compte = 1
            else:
                compte += 1
        byte_fichier.extend([compte, pixel_precedent.red, pixel_precedent.green, pixel_precedent.blue])
        return bytes(byte_fichier)

    def creation_palette(self):
        """
        crée la palette de l'image.
        :return: palette de l'image.
        """
        palette = {}
        index = 0
        for pixel in self.image.pixels:
            if pixel not in palette:
                palette[pixel] = index
                index += 1
        return palette

    def index_palette(self, pixel):
        """
        retourne l'index d'un pixel dans la palette.
        :param pixel: pixel à chercher.
        :return: index du pixel.
        """
        return self.palette[pixel]

    def encodage_profondeur_1(self):
        """
        encode les pixels en profondeur 1.
        :return: pixels encodés.
        """
        byte_fichier = bytearray()
        palette = self.palette
        bit = 0
        compte = 0
        decalage = 1
        for pixel in self.image.pixels:
            pixel_value = palette[pixel]
            bit |= (pixel_value & decalage) << (7 - compte)
            compte += 1
            if compte == 8:
                byte_fichier.append(bit)
                bit = 0
                compte = 0
        if compte > 0:
            byte_fichier.append(bit)
        return bytes(byte_fichier)

    def encodage_profondeur_2(self):
        """
        encode les pixels en profondeur 2.
        :return: pixels encodés.
        """
        byte_file = bytearray()
        bit = 0
        compte = 0
        for pixel in self.image.pixels:
            valeur_pixel = self.index_palette(pixel)
            bit |= valeur_pixel << (6 - compte)
            compte += 2
            if compte == 8:
                byte_file.append((bit >> (compte - 8)) & 0xFF)
                compte = 0
                bit = 0
        if compte > 0:
            byte_file.append(bit << (8 - compte) & 0xFF)
        return bytes(byte_file)

    def encodage_profondeur_8(self):
        """
        encode les pixels en profondeur 8.
        :return: pixels encodés.
        """
        byte_fichier = bytearray()
        palette = self.palette
        for pixel in self.image.pixels:
            pixel_index = palette[pixel]
            byte_fichier.append(pixel_index)
        return bytes(byte_fichier)

    def encodage_profondeur_4(self):
        """
        encode les pixels en profondeur 4.
        :return: pixels encodés.
        """
        byte_fichier = bytearray()
        palette = self.palette
        pixels = self.image.pixels
        for i in range(0, len(pixels), 2):
            indice_pixel = [palette[pixels[i]], palette[pixels[i + 1]] if i + 1 < len(pixels) else 0]
            byte_fichier.append((indice_pixel[0] << 4) | indice_pixel[1])
        return bytes(byte_fichier)

    def encodage_profondeur_8_avec_rle(self):
        """
        encode les pixels en profondeur 8 avec la compression RLE.
        :return: pixels encodés.
        """
        byte_fichier = bytearray()
        palette = self.palette
        pixel_precedent = None
        repetition = 0
        for pixel in self.image.pixels:
            pixel_index = palette[pixel]
            if pixel_index != pixel_precedent or repetition == 255:
                if pixel_precedent is not None:
                    byte_fichier.extend([repetition, pixel_precedent])
                pixel_precedent = pixel_index
                repetition = 1
            else:
                repetition += 1
        if repetition > 0:
            byte_fichier.extend([repetition, pixel_precedent])
        return bytes(byte_fichier)

    @staticmethod
    def calcul_diff_rgb(pixel, pixel_precedent):
        """
        calcule la différence entre les valeurs RGB de deux pixels.
        :param pixel: pixel actuel.
        :param pixel_precedent: pixel précédent.
        :return: différence entre les valeurs RGB.
        """
        return pixel.red - pixel_precedent.red, pixel.green - pixel_precedent.green, pixel.blue - pixel_precedent.blue

    def encode_pixels_v4_suite(self):
        """
        encode les pixels de la version 4.
        :return:
        """
        byte_fichier = bytearray()
        pixel_precedent = Pixel(0, 0, 0)
        for pixel in self.image.pixels:
            diff_r, diff_g, diff_b = self.calcul_diff_rgb(pixel, pixel_precedent)
            diff_rg = diff_r - diff_g
            diff_gb = diff_g - diff_b
            diff_rb = diff_r - diff_b
            if -2 <= diff_r <= 1 and -2 <= diff_g <= 1 and -2 <= diff_b <= 1:  # small diff
                byte_diff = [0 | ((diff_r + 2) << 4) | ((diff_g + 2) << 2) | (diff_b + 2)]  # byte 1
            elif -8 <= diff_rg <= 7 and -32 <= diff_g <= 31 and -8 <= diff_gb <= 7:  # intermediate diff
                byte_diff = [0b01000000 | (diff_g + 32) & 0b00111111,  # byte 1
                             ((diff_r - diff_g + 8) & 0b1111) << 4 | (diff_b - diff_g + 8)]  # byte 2
            elif -128 <= diff_r <= 127 and -32 <= diff_gb <= 31 and -32 <= diff_rb <= 31:  # big diff r
                byte_diff = [0b10000000 | ((diff_r + 128) & 0b11110000) >> 4,  # byte 1
                             (((diff_r + 128) & 0b1111) << 4) | (((diff_g - diff_r) + 32) >> 2),  # byte 2
                             (((diff_g - diff_r) + 32) & 0b11) << 2 | ((diff_b - diff_r) + 32) & 0b00111111]  # byte 3
            elif -128 <= diff_g <= 127 and -32 <= diff_rg <= 31 and -32 <= diff_rb <= 31:  # big diff g
                byte_diff = [0b10010000 | ((diff_g + 128) & 0b11110000) >> 4,  # byte 1
                             (((diff_g + 128) & 0b1111) << 4) | (((diff_r - diff_g) + 32) >> 2),  # byte 2
                             (((diff_r - diff_g) + 32) & 0b11) << 2 | ((diff_b - diff_g) + 32) & 0b00111111]  # byte 3
            elif -128 <= diff_b <= 127 and -32 <= diff_rg <= 31 and -32 <= diff_gb <= 31:  # big diff b
                byte_diff = [0b10100000 | ((diff_b + 128) & 0b11110000) >> 4,  # byte 1
                             (((diff_b + 128) & 0b1111) << 4) | (((diff_r - diff_b) + 32) >> 2),  # byte 2
                             (((diff_r - diff_b) + 32) & 0b11) << 2 | ((diff_g - diff_b) + 32) & 0b00111111]  # byte 3
            else:
                byte_diff = [255, pixel.red, pixel.green, pixel.blue]  # new pix
            byte_fichier.extend(byte_diff)
            pixel_precedent = pixel
        return bytes(byte_fichier)

"""
NOM : LIEFFERINCKX
PRÉNOM : Romain
SECTION : INFO
MATRICULE : 000591790
"""

from pixel import Pixel


class Image:
    """
    Classe Image: cette classe représente une image.
    """
    val_min_dim = 0
    len_pos = 2

    def __init__(self, width, height, pixels):
        """
        initialisation des attributs de la classe Image et condition de fonctionnement
        :param width: largeur de l'image en pixels.
        :param height: hauteur de l'image en pixels.
        :param pixels: liste de pixels qui sont dans l'image.
        """
        if width <= self.val_min_dim or height <= self.val_min_dim or pixels == [] or len(pixels) != width * height:
            raise Exception

        if not isinstance(pixels, list) or not all(isinstance(p, Pixel) for p in pixels):
            raise TypeError

        else:
            for p in pixels:
                if not isinstance(p, Pixel):
                    raise ValueError
        self.__width = width
        self.__height = height
        self.__pixels = pixels
        self.unique_colors = set((pixel.red, pixel.green, pixel.blue) for pixel in pixels)

    def set_pixel(self, index, pixel):
        """
        déplacer un pixel à un index donné
        :param index: index du pixel à modifier.
        :param pixel: nouveau pixel.
        """
        self.pixels[index] = pixel
        self.unique_colors.add((pixel.red, pixel.green, pixel.blue))

    def get_unique_color_count(self):
        """
        retourne le nombre de couleurs uniques dans l'image.
        :return: Le nombre de couleurs uniques.
        """
        return len(self.unique_colors)

    @property
    def pixels(self):
        """
        retourne la liste des pixels de l'image.
        :return: liste des pixels.
        """
        return self.__pixels

    @property
    def width(self):
        """
        retourne la largeur de l'image.
        :return: largeur de l'image.
        """
        return self.__width

    @property
    def height(self):
        """
        retourne la hauteur de l'image.
        :return: hauteur de l'image.
        """
        return self.__height

    @property
    def palette(self):
        """
        retourne la palette de couleurs de l'image.
        :return:  palette de couleurs.
        """
        return self.__palette

    def __getitem__(self, pos):
        """
        retourne le pixel à la position spécifiée. et lève une erreur si la position n'est pas valide.
        :param pos: tuple contenant les coordonnées (x, y) du pixel.
        :return: pixel à la position spécifiée.
        """
        if len(pos) != self.len_pos or not all(isinstance(i, int) for i in pos): # vérifie si i est un entier
            raise IndexError
        x, y = pos
        if self.val_min_dim <= x <= self.__width and self.val_min_dim <= y <= self.__height:
            return self.__pixels[y * self.__width + x]  # surcharge de l'opérateur []
        else:
            raise IndexError

    def __setitem__(self, pos, pix):
        """
        modifie le pixel à la position spécifiée et lève une erreur si la position n'est pas valide.
        :param pos:  tuple contenant les coordonnées (x, y) du pixel.
        :param pix:  nouveau pixel.
        """
        if len(pos) != self.len_pos or not all(isinstance(i, int) for i in pos):  # vérifie si i est un entier
            raise IndexError
        x, y = pos
        if not isinstance(pix, Pixel):  # vérifie si le pixel est un objet de la classe Pixel
            raise TypeError
        if self.val_min_dim <= x < self.__width and self.val_min_dim <= y < self.__height:
            self.__pixels[y * self.__width + x] = pix  # pix = nouveau pixel à la position spécifiée dans l'image
        else:
            raise IndexError

    def __eq__(self, other):
        """
        compare cette image à une autre pour voir si ce sont les mêmes.
        :param other: autre image à comparer.
        :return: True si les images sont les meme, sinon False.
        """
        if not isinstance(other, Image):  # vérifie si l'autre objet est une image
            return False
        return self.__width == other.__width and self.__height == other.__height and self.__pixels == other.__pixels

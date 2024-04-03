"""
NOM : LIEFFERINCKX
PRÉNOM : Romain
SECTION : INFO
MATRICULE : 000591790
"""


class Pixel:
    """
    Classe Pixel: Cette classe représente un pixel.
    """
    val_min_couleur = 0  # initialisation de la variable val_min_couleur qui va servir a délimiter les valeurs de pixel
    val_max_couleur = 255 # initialisation de la variable val_max_couleur qui va servir a délimiter les valeurs de pixel
    # valeurs entre 0 et 255

    def __init__(self, red, green, blue):
        """
        initialisation des attributs de la classe Pixel
        :param red: red entier entre 0 et 255 qui va faire varier la couleur de la composante rouge du pixel
        :param green: green entier entre 0 et 255 qui va faire varier la couleur de la composante verte du pixel
        :param blue: blue entier entre 0 et 255 qui va faire varier la couleur de la composante bleue du pixel
        """
        self.red = red
        self.green = green
        self.blue = blue

    def val_correcte(self, val_pix):
        """

        :param val_pix: valeur de la composante
        :return: une ValueError si oui ou non la composante respecte la condition (est un entier entre 0 et 255)
        """
        if not isinstance(val_pix, int) or val_pix < self.val_min_couleur or val_pix > self.val_max_couleur:
            raise ValueError

    @property
    def red(self):
        """
        :return: self.__red
        """
        return self.__red

    @red.setter
    def red(self, value):
        """
        :param value: vérifie que red est correcte et utilisable
        """
        self.val_correcte(value)
        self.__red = value

    @property
    def green(self):
        """
        :return: self.__green
        """
        return self.__green

    @green.setter
    def green(self, value):
        """
        :param value: vérifie que green est correcte et utilisable
        """
        self.val_correcte(value)
        self.__green = value

    @property
    def blue(self):
        """
        :return: self.__blue
        """
        return self.__blue

    @blue.setter
    def blue(self, value):
        """
        :param value: vérifie que blue est correcte et utilisable
        """
        self.val_correcte(value)
        self.__blue = value

    def __eq__(self, other):
        """
        méthode qui permet de comparer deux pixels
        :param other: un autre objet Pixel.
        :return: True si les deux pixels sont les meme, sinon False.
        """
        if not isinstance(other, Pixel):
            return False
        return self.__red == other.__red and self.__green == other.__green and self.__blue == other.__blue

    def __hash__(self):
        """
        méthode qui permet d'avoir la valeur de hachage d'un pixel
        :return: la valeur de hachage d'un pixel
        """
        return hash((self.__red, self.__green, self.__blue))

    def __repr__(self):
        """
        méthode qui permet de représenter un pixel
        :return: la représentation d'un pixel en chaine de caractère
        """
        return f"Pixel({self.__red}, {self.__green}, {self.__blue})"

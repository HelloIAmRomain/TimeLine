from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import csv
import numpy as np


class Classement(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('classement.ui', self)
    
    def valeur(self):
        return self.nom_joueur.text()
    

# Programme test
if __name__=="__main__":
    app = QApplication([])
    page = Classement()
    page.show()
    app.exec_()
    print(page.valeur())
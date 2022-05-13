from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
import numpy as np
import csv
from random import randint, shuffle
import classement

class Quizlet(QDialog):
    def __init__(self,cartes):
        super().__init__()
        self.mode="question"
        self.nom_joueur = ''
        loadUi('quizlet.ui', self)
        self.cartes = cartes
        self.creer_reponses()
        self.reponses = [["",""], ["",""], ["",""]]
        self.tableau = np.array(self.melanger(self.cartes)) # [question, rep1(vraie), rep2, rep3, tolerance, info]
        self.btn1.clicked.connect(self.rep1)
        self.btn2.clicked.connect(self.rep2)
        self.btn3.clicked.connect(self.rep3)
        self.total_points = 0
        self.score = 0
        self.termine = False
        

    def creer_reponses(self):
        """
        Modifie le paquet pour ajouter les deux autres propositions de reponses
        =======
        Le paquet est maintenant composé de cartes ayant comme informations:
            [question, reponse1(correcte), reponse2, reponse3, tolerance, infromation, image]
        """
        coeff = [-5,-4,-3,-2,-1,1,2,3,4,5] # On créée les questions à partir de la date et des tolérances
        liste_question1=[]
        liste_question2=[]
        for n in range(len(self.cartes)):
            coeff_rep = self.melanger(coeff)
            coeff_rep1 = coeff_rep[0]
            coeff_rep2 = coeff_rep[1]
            rep1 = int(self.cartes[n][1]) + int(self.cartes[n][2]) * coeff_rep1
            rep2 = int(self.cartes[n][1]) + int(self.cartes[n][2]) * coeff_rep2
            liste_question1.append(str(rep1))
            liste_question2.append(str(rep2))
        self.cartes = np.insert(self.cartes, 2, np.array(liste_question1), axis=1)
        self.cartes = np.insert(self.cartes, 3, np.array(liste_question2), axis=1)


    def rep1(self):
        if self.btn1.text() == "":
            pass
        elif self.reponses[0][1] == 1:  #la bonne reponse
            self.resultat.setText("Bravo, bonne réponse !")
            self.score += 1
        else:
            self.resultat.setText("Dommage, mauvaise réponse")
        self.suivant(1)

    def rep2(self):
        if self.btn1.text() == "":
            pass
        elif self.reponses[1][1] == 1: #la bonne reponse
            self.resultat.setText("Bravo, bonne réponse !")
            self.score += 1
        else:
            self.resultat.setText("Dommage, mauvaise réponse")
        self.suivant(2) 

    def rep3(self):
        if self.btn1.text() == "":
            self.resultat.setText("")
        elif self.reponses[2][1] == 1: #la bonne reponse
            self.resultat.setText("Bravo, bonne réponse !")
            self.score += 1
        else:
            self.resultat.setText("Dommage, mauvaise réponse")
        self.suivant(3)


    def melanger(self, cartes):
        liste = list(a for a in range(len(cartes)))
        melange = []
        for i in range(20*len(liste)):
            shuffle(liste)
        for i in liste:
            melange.append(cartes[i])
        return melange


    def suivant(self, num_reponse):
        if len(self.tableau)>0:
            if self.mode=="question":
                last = self.tableau[-1]
                self.reponses = [[last[1],1], [last[2],2], [last[3],3]]
                self.im = QPixmap(last[6])
                self.image.setPixmap(self.im)
                for k in range(10):
                    shuffle(self.reponses)
                self.question.setText(last[0])
                self.btn1.setText(self.reponses[0][0])
                self.btn2.setText(self.reponses[1][0])
                self.btn3.setText(self.reponses[2][0])
                self.total_points += 1 # Nombre de questions posées
                self.mode="reponse"
                
            
            elif self.mode=="reponse":
                last = self.tableau[-1]
                self.question.setText(last[1])
                self.mode="info"
                self.btn1.setText("")
                self.btn2.setText("Suivant")
                self.btn3.setText("")

            elif self.mode=="info":
                last, self.tableau = self.tableau[-1], self.tableau[:-1] # equivalent du list.pop en np
                self.question.setText(last[5])
                self.mode="question"
                self.btn1.setText("")
                self.btn2.setText("Suivant")
                self.btn3.setText("")

        else:
            if self.termine:
                self.close()
                fenetre_classement = classement.Classement()
                fenetre_classement.exec_()
                self.nom_joueur = fenetre_classement.valeur()
            else:
                self.question.setText("Fin\nScore: " + str(self.score) + " / " + str(self.total_points))
                self.termine = True




# Programme test
if __name__=="__main__":
    cartes = np.array([["question1",100,5,"info1","./Banque Image/Aristote.jpg"],
                       ["question2",100,2,"info2","./Banque Image/Avicenne.jpg"],
                       ["question3",100,1,"info3","./Banque Image/1er milliard d_humain.jpg"]])

    app = QApplication([])
    quiz = Quizlet(cartes)
    quiz.show()
    app.exec_()

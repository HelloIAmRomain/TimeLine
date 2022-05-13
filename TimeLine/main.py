from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import csv
import numpy as np
import quizlet
import classement

class Main(QMainWindow):
    """
       # **TimeLine** #
    
    Bienvenue sur le logiciel d'education !
    
    Avec ce programme, vous pourrez:
     - [x] Apprendre rapidement vos cours
     - [x] Améliorer votre culture générale
     - [x] Vous amuser!
    
    Pour jouer, rien de plus simple! 
    Il suffit d'executer le fichier nommé **"jouer.bat"**
    
    Le programme propose un fichier CSV fourni, mais vous pouvez tout-à-fait créer le vôtre sur Excel, ou directement sur le python.
    
    Nous espérons que vous en ferez un bon usage!
    
    Ce code a été réalisé par trois étudiants de l'Icam Toulouse
    https://www.icam.fr/
    
    Bonne visite!

    """
    def __init__(self):
        super(Main,self).__init__()
        loadUi('main.ui',self)
        self.im_ajout = ''
        self.modif_flag = False
        self.btnAjouter.clicked.connect(self.ajouterCarte)
        self.btnJouer.clicked.connect(self.jouer)
        self.btnSupprimer.clicked.connect(self.supprimer)
        self.btnSupp_classement.clicked.connect(self.supprimer_classement)
        self.btnEnregistrer.clicked.connect(self.enregistrer)
        self.btnOuvrir.clicked.connect(self.ouvrir)
        self.btnSelectImage.clicked.connect(self.selectionner_image)
        self.btnTout_cocher.clicked.connect(self.tout_cocher)
        self.btnTout_decocher.clicked.connect(self.tout_decocher)
        self.toutes_les_cartes.clicked.connect(self.filtre)
        self.filtrer_les_cartes.clicked.connect(self.filtre)
        self.filtre_themes.stateChanged.connect(self.filtre)
        self.filtre_continent.stateChanged.connect(self.filtre)
        self.tableau = np.array([])
        self.afficher()
        self.ouvrir_classement()
        self.tabWidget.setCurrentIndex(0) # Affiche le premier onglet
        self.filtre()

    def afficher(self):
        self.tableWidget.setRowCount(len(self.tableau))
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setHorizontalHeaderLabels(("Item","Dates","Tolerance","Ere historique","Protagonistes","Aire geographique","Rubrique","Detail","Sources documentaires","Enjeux","Auteur du doc"))
        ligne = 0
        if len(self.tableau)>0:
            for p in range(len(self.tableau)):
                self.tableWidget.setItem(ligne,0, QTableWidgetItem(str(self.tableau[p][0])))
                self.tableWidget.setItem(ligne,1, QTableWidgetItem(str(self.tableau[p][1])))
                self.tableWidget.setItem(ligne,2, QTableWidgetItem(str(self.tableau[p][2])))
                self.tableWidget.setItem(ligne,3, QTableWidgetItem(str(self.tableau[p][3])))
                self.tableWidget.setItem(ligne,4, QTableWidgetItem(str(self.tableau[p][4])))
                self.tableWidget.setItem(ligne,5, QTableWidgetItem(str(self.tableau[p][5])))
                self.tableWidget.setItem(ligne,6, QTableWidgetItem(str(self.tableau[p][6])))
                self.tableWidget.setItem(ligne,7, QTableWidgetItem(str(self.tableau[p][7])))
                self.tableWidget.setItem(ligne,8, QTableWidgetItem(str(self.tableau[p][8])))
                self.tableWidget.setItem(ligne,9, QTableWidgetItem(str(self.tableau[p][9])))
                self.tableWidget.setItem(ligne,10, QTableWidgetItem(str(self.tableau[p][10])))
                ligne += 1
        if (len(self.tableau))>0:
            self.btnJouer.setText("Jouer!")
            self.btnJouer.setEnabled(True)
        else:
            self.btnJouer.setText("Pas de cartes à jouer")
            self.btnJouer.setEnabled(False)
            
    def ajouterCarte(self):
        item = self.item.text()
        date = self.date.text()
        erehistorique = self.erehistorique.currentText()
        protagoniste = self.protagoniste.text()
        airegeographique = self.airegeographique.currentText()
        rubrique = self.rubrique.currentText()
        details = self.details.text()
        sources = self.sources.text()
        enjeux = self.enjeux.text()
        auteurdoc = self.auteur.text()
        toleranceAnnee = self.tolerance.text()
        image = self.im_ajout
        # Maintenant on les rassemble en une ligne et on le met dans le CSV
        nouvelle_carte = [item, date, toleranceAnnee, erehistorique, protagoniste, airegeographique, rubrique, details, sources, enjeux, auteurdoc, image]
        if len(self.tableau) == 0:
            self.tableau = np.array([nouvelle_carte])
        else:
            self.tableau = np.append(self.tableau, [nouvelle_carte], axis=0)
        self.resultat.setText('Insertion réussie')
        self.modif_flag = True
        self.afficher()
        self.raz_ajout()
        
    
    def afficher_classement(self):
        self.classement.setRowCount(len(self.tableau_classement))
        self.classement.setColumnCount(2)
        self.classement.setHorizontalHeaderLabels(("Nom","Score"))
        self.classement.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        ligne = 0
        if len(self.tableau_classement)>0:
            for p in range(len(self.tableau_classement)):
                self.classement.setItem(ligne,0, QTableWidgetItem(str(self.tableau_classement[p][0])))
                self.classement.setItem(ligne,1, QTableWidgetItem(str(self.tableau_classement[p][1])))
                ligne += 1
    
    def raz_ajout(self):
        self.visualisation_image.setPixmap(QPixmap())
        for editable in [self.item,self.date,self.tolerance, self.protagoniste, self.details, self.sources, self.enjeux, self.auteur]:
            editable.clear()
            self.erehistorique.setCurrentIndex(0)
            self.airegeographique.setCurrentIndex(0)
            self.rubrique.setCurrentIndex(0)


    def selectionner_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', directory='.')
        chemin_image = fname[0]
        if len(chemin_image)>4 and chemin_image[-4:]==".jpg":
            self.im_ajout = chemin_image
            self.visualisation_image.setPixmap(QPixmap(chemin_image))
        else:
            pass # rien ne se passe si le fichier n'est pas un JPG


    def filtre(self):
        filtre_general = self.filtrer_les_cartes.isChecked()
        activer_theme = self.filtre_themes.isChecked()
        activer_continent = self.filtre_continent.isChecked()
        
        self.accord.setEnabled(filtre_general and activer_theme)
        self.architecture.setEnabled(filtre_general and activer_theme)
        self.culture.setEnabled(filtre_general and activer_theme)
        self.evenement.setEnabled(filtre_general and activer_theme)
        self.fondation.setEnabled(filtre_general and activer_theme)
        self.geographie.setEnabled(filtre_general and activer_theme)
        self.invention.setEnabled(filtre_general and activer_theme)
        self.personnage.setEnabled(filtre_general and activer_theme)
        self.religion.setEnabled(filtre_general and activer_theme)
        self.rivalites.setEnabled(filtre_general and activer_theme)
        self.transports.setEnabled(filtre_general and activer_theme)

        self.afrique.setEnabled(filtre_general and activer_continent)
        self.amerique_nord.setEnabled(filtre_general and activer_continent)
        self.amerique_sud.setEnabled(filtre_general and activer_continent)
        self.asie.setEnabled(filtre_general and activer_continent)
        self.europe.setEnabled(filtre_general and activer_continent)
        self.proche_orient.setEnabled(filtre_general and activer_continent)
        
        self.filtre_continent.setEnabled(filtre_general)
        self.filtre_themes.setEnabled(filtre_general)
        self.btnTout_cocher.setEnabled(filtre_general)
        self.btnTout_decocher.setEnabled(filtre_general)
        

    def tout_cocher(self):
        self.tout_cocher_decocher(True)
    def tout_decocher(self):
        self.tout_cocher_decocher(False)
    def tout_cocher_decocher(self, state):
        self.accord.setChecked(state)
        self.architecture.setChecked(state)
        self.culture.setChecked(state)
        self.evenement.setChecked(state)
        self.fondation.setChecked(state)
        self.geographie.setChecked(state)
        self.invention.setChecked(state)
        self.personnage.setChecked(state)
        self.religion.setChecked(state)
        self.rivalites.setChecked(state)
        self.transports.setChecked(state)
        self.afrique.setChecked(state)
        self.amerique_nord.setChecked(state)
        self.amerique_sud.setChecked(state)
        self.asie.setChecked(state)
        self.europe.setChecked(state)
        self.proche_orient.setChecked(state)
        self.filtre_themes.setChecked(True)
        self.filtre_continent.setChecked(True)


    def supprimer(self):
        sup = self.tableWidget.selectedItems()
        liste_sup = [sup[k].row() for k in range(len(sup))]
        liste_garder = [k for k in range(len(self.tableau))]
        for k in liste_sup:
            liste_garder.remove(k)
        self.tableau = self.tableau[liste_garder,:]
        if len(self.tableau)>0:
            self.modif_flag = True
        else:
            self.modif_flag = False
        # On rafraichit le TableWidget
        self.afficher()


    def supprimer_classement(self):
        sup = self.classement.selectedItems()
        liste_sup = [sup[k].row() for k in range(len(sup))]
        liste_garder = [k for k in range(len(self.tableau_classement))]
        for k in liste_sup:
            liste_garder.remove(k)
        self.tableau_classement = self.tableau_classement[liste_garder,:]
        # On rafraichit le TableWidget
        self.afficher_classement()


    def jouer(self):
        paquet = self.creer_paquet()
        self.hide()
        jeu = quizlet.Quizlet(paquet)
        jeu.exec_()
        self.show()
        if jeu.nom_joueur != '':
            total_points = jeu.total_points
            score = jeu.score
            nom = jeu.nom_joueur
            nouveau_score = [str(nom), str(score)+" / "+str(total_points)]
            if len(self.tableau_classement) == 0:
                self.tableau_classement = np.array([nouveau_score])
            else:
                self.tableau_classement = np.append(self.tableau_classement, [nouveau_score], axis=0)
            self.afficher_classement()


    def creer_paquet(self) :
        """
        Un paquet est composé de cartes ayant comme informations:
            [question, date, tolerance, infromation, image]
        l'image sert à illustrer la question
        """
        themes = []
        continent = []
        paquet=[]
        
        if self.filtre_themes.isChecked():
            if self.accord.isChecked():
                themes.append('accord')
            if self.architecture.isChecked():
                themes.append('architecture')
            if self.culture.isChecked():
                themes.append('culture')
            if self.evenement.isChecked():
                themes.append('evenement')
            if self.fondation.isChecked():
                themes.append('fondation')
            if self.geographie.isChecked():
                themes.append('geographie')
            if self.invention.isChecked():
                themes.append('invention')
            if self.personnage.isChecked():
                themes.append('personnage')
            if self.religion.isChecked():
                themes.append('religion')
            if self.rivalites.isChecked():
                themes.append('rivalites')
            if self.transports.isChecked():
                themes.append('transports')
        else:
            themes = ["%"]
        if self.filtre_continent.isChecked():
            if self.asie.isChecked():
                continent.append("Asie")
            if self.europe.isChecked():
                continent.append("Europe")
            if self.amerique_nord.isChecked():
                continent.append("Amerique du Nord")
            if self.amerique_sud.isChecked():
                continent.append("Amerique du Sud")
            if self.afrique.isChecked():
                continent.append("Afrique")
            if self.proche_orient.isChecked():
                continent.append("Proche-Orient")
        else:
            continent = ["%"]
        # On creee le paquet de cartes a jouer avec les contraintes de theme et continent
        for ligne in range(len(self.tableau)):
            if  self.tableau[ligne][2]!="0" and (self.toutes_les_cartes.isChecked() or (self.tableau[ligne][5] in continent or continent == ["%"]) and (self.tableau[ligne][6] in themes or themes == ["%"])):
                carte = [self.tableau[ligne][0], self.tableau[ligne][1], self.tableau[ligne][2], self.tableau[ligne][7], self.tableau[ligne][11]]
                paquet.append(carte)
        if len(paquet)==0:
            paquet = [["Pas de cartes",0,0,"Pas de cartes","./Banque Image/pas de carte.jpg"]]
        return paquet
    

    def ouvrir(self):
        fname = QFileDialog.getOpenFileName(self, 'Ouvrir votre document', directory='.')
        if fname[0] != "": # il faut que un fichier soit selectionne sinon rien ne se passe
            if fname[0][-4:]==".csv":
                with open(fname[0],"r") as doc:
                    val = list(csv.reader(doc, delimiter=';'))
                self.tableau = np.array(val)
                self.modif_flag = False
        else:
            pass # rien ne se passe si le fichier n'est pas un CSV
        self.afficher()


    def ouvrir_classement(self):
        with open('classement.csv',"r") as doc:
            val = list(csv.reader(doc, delimiter=';'))
        self.tableau_classement = np.array(val)
        self.afficher_classement()

    def enregistrer(self):
        fname = QFileDialog.getSaveFileName(self, 'Enregistrer votre document', directory='.', filter="*.*")
        if fname[0] != "": # il faut que un fichier soit selectionne sinon rien ne se passe
            if len(fname[0])<=4 or fname[0][-4:]!=".csv":
                fname[0] += '.csv'
            with open(fname[0], 'w', newline='') as file:
                mywriter = csv.writer(file, delimiter=';')
                mywriter.writerows(self.tableau)
            self.modif_flag = False


    def enregistrer_classement(self):
        with open('classement.csv', 'w', newline='') as file:
            mywriter = csv.writer(file, delimiter=';')
            mywriter.writerows(self.tableau_classement)

    def closeEvent(self, event):
        self.enregistrer_classement()
        if self.modif_flag:
            reply = QMessageBox.question(self, 'Fermeture', 'Voulez-vous enregistrer vos données?',
            QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Discard,QMessageBox.Save)
            if reply == QMessageBox.Save:
                self.enregistrer()            
                event.accept() # let the window close
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()



# Programme principal  
if __name__=="__main__":
    app = QApplication([])
    monAppli = Main()
    monAppli.showMaximized()
    app.exec_()
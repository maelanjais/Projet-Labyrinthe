#imports

import matplotlib.pyplot as plt
from pileNonBornee import *
from random import randint



class Case:
    
    """
Cette classe représente les cases d'un labyrinthe sous forme de quadrillage. Chaque case a quatre directions (nord, sud, est, ouest),
 indiquées par des valeurs booléennes pour la présence de murs. L'état de la case indique si elle a été explorée (True) ou non (False)
 """

    def __init__(self):

        self.Nord = False
        self.Sud = False
        self.Est = False
        self.Ouest = False

        self.etat = False


class Labyrinthe:
    
    """Cette class représente le labyrinthe. Il a n * m cases (n est sa longueur, m sa largeur) qui sont
    contenues chacune dans un tableau bidimensionnel afin de créer un labyrinthe en 2-Dimensions."""


    def __init__(self, n = 25, m = 25):
        
        """
        Ce constructeur prend en compte la longueur 
        et la largeur fournies par l'utilisateur pour créer le labyrinthe.
        """

        self.ligne = n
        self.colonne = m
        self.tab = [[Case() for _ in range(n)] for _ in range(m)]


    def show(self):
        
        """Cette méthode utilise la bibliothèque matplotlib pour afficher le labyrinthe.
          Elle parcourt toutes les cases du labyrinthe et trace des 
        traits pour représenter les murs à droite ou au-dessus de chaque case. Bien qu'elle ne renvoie aucune valeur,
          elle génère un affichage visuel du labyrinthe."""
        
        
        for x in range(self.ligne):
            for y in range(self.colonne):
                if self.tab[y][x].Est == False : # vérifie si la case a un mur à sa droite (Est)
                    plt.plot([x + 1, x + 1], [y, y +1], color="#8000ff")

                if self.tab[y][x].Nord == False : # vérifie si la case a un mur au-dessus (Nord)
                    plt.plot([x, x + 1], [y + 1, y + 1], color="#8000ff")
                    


        plt.plot([0, self.ligne, self.ligne, 0, 0], [self.colonne, self.colonne, 0, 0, self.colonne], color="#8000ff")
        # trace les bords du labyrinthe
        
        plt.show() # affiche le tracé
        


    def solution(self):
        
        """Cette méthode permet d'afficher la solution d'un labyrinthe. Pour cela, elle utilise la fonction "explorer"
        afin de récupérer un tableau de duplets contenant le parcours de valeurs pour atteindre la sortie à partir de
        l'arrivée.
        Ce tableau de duplets est ensuite séparé en deux tableaux correspondant aux coordonnées des cases explorées.
        Ces deux nouveaux tableaux "X" et "Y" sont alors intégrées dans la fonction "plot" de matplotlib qui permet
        de tracer entre chaque point (définis par les coordonnées X et Y)"""
        
        t = explorer(self) # créer une variable pour avoir le chemin à la sortie
        
        X = [t[i][0] + 0.5 for i in range(len(t))]
        Y = [t[i][1] + 0.5 for i in range(len(t))]
        # les valeurs des coordonnées sont décalées de 0.5 pour que le tracé ne se confond pas avec les murs du labyrinthe
        
        plt.plot(X, Y, color="#ffbf00") # trace la solution
            
        self.show() # affiche la solution
             

def creation(n, m):
    
    """
Cette fonction crée de manière aléatoire un labyrinthe de taille n * m (longueur * largeur). 
Elle parcourt toutes les cases du labyrinthe, et pour chaque case,
 elle casse les murs dans des directions choisies de manière aléatoire."""

    l = Labyrinthe(n, m) # crée un labyrinthe vide de taille n * m


    p = Pile(None) # traitement de toutes les cases du labyrinthe effectué par la structure de données LIFO

    i = randint(0, n - 1) 
    j = randint(0, m - 1)
    # coordonnées du point de départ du labyrinthe

    p.empile([i, j]) # empile la pos de départ du labyrinthe dans p


    l.tab[j][i].etat = True 

    while p.est_vide() == False :

        i = p.sommet()[0]
        j = p.sommet()[1]
        # définie les coordonnées de la case qui va être vérifiée (il s'agit des coordonnées en tête de pile)

        t = []

        if i != n - 1 and l.tab[j][i + 1].etat == False :
            t.append("Est")

        if j != 0 and l.tab[j - 1][i].etat == False :
            t.append("Sud")

        if j != m - 1 and l.tab[j + 1][i].etat == False :
            t.append("Nord")


        if i != 0 and l.tab[j][i - 1].etat == False :
            t.append("Ouest")       
       


        if len(t) == 0 :

            p.depile()
        
        # retire de la pile la case vérifiée si toutes les cases juxtaposées à celle-ci ont leur état à True
        # (s'il n'y a donc plus de possibilité de chemin à créer)



        else :

            dir = t[randint(0, len(t) - 1)]    # utilise le module random pour prendre une direction aléatoire parmi les directions possibles stockées dans le tableau t

            
                # casse le mur dans la direction choisie 
                
            if dir == "Nord" :

                l.tab[j][i].Nord = True
                j += 1
                l.tab[j][i].Sud = True

            elif dir == "Ouest" :
                
                l.tab[j][i].Ouest = True
                i -= 1
                l.tab[j][i].Est = True

            elif dir == "Est" :
            
                l.tab[j][i].Est = True
                i += 1
                l.tab[j][i].Ouest = True
            
            elif dir == "Sud" :

                l.tab[j][i].Sud = True
                j -= 1
                l.tab[j][i].Nord = True

            
            l.tab[j][i].etat = True
            p.empile([i, j]) # ajoute à la pile la nouvelle case et passe son état à True
            


    l.show() #affiche le labyrinthe
    
    return l



def explorer(l):
    
    """ Cette fonction explore le labyrinthe en enregistrant son chemin jusqu'à atteindre la sortie. 
    Elle utilise une pile pour suivre son parcours, empilant chaque étape et dépilant les étapes inutiles."""
    
    p = Pile(None)
    
    n = l.ligne
    m = l.colonne
    
    l.tab[0][n - 1].etat = False # passe l'état de la case de départ à False
    l.tab[m - 1][n - 1].etat = False # passe l'état de la case d'arrivée à False
    
    p.empile([0, m - 1]) # empile la case de départ

    
    while not p.est_vide():     
        i = p.sommet()[0]
        j = p.sommet()[1]
        # récupère les coordonnées de la case en tête de file
        
        if (i == n - 2 and j == 0 and l.tab[j][i].Est == True and l.tab[j][i + 1].Ouest == True) or (i == n - 1 and j == 1 and l.tab[j][i].Sud == True and l.tab[j - 1][i].Nord == True):
            # vérifie les cases voisines et regarde si il est possible de s'y rendre   
            t = [[n - 1, 0]]           
            while not p.est_vide():               
                t.append(p.depile()) # dépile la case                
            return t
        

        if i != n - 1 and l.tab[j][i + 1].etat == True and l.tab[j][i].Est == True and l.tab[j][i + 1].Ouest == True : 
            i += 1
            p.empile([i, j])
            l.tab[j][i].etat = False
            

        elif j != -1 and l.tab[j - 1][i].etat == True and l.tab[j][i].Sud == True and l.tab[j - 1][i].Nord == True : 
            p.empile([i, j])
            l.tab[j][i].etat = False
            
        elif i != -1 and l.tab[j][i - 1].etat == True and l.tab[j][i].Ouest == True and l.tab[j][i - 1].Est == True : 
            i -= 1
            p.empile([i, j])
            l.tab[j][i].etat = False    
            
        elif j != m - 1 and l.tab[j + 1][i].etat == True and l.tab[j][i].Nord == True and l.tab[j + 1][i].Sud == True : 
            j += 1
            p.empile([i, j])
            l.tab[j][i].etat = False


        else :
            p.depile()
  
  
def verif(l):
    
    """ Vérifie la valabilité du labyrinthe.
    Renvoit True s'il est valable. Sinon, renvoit un tableau contenant les cases non valables"""
    
    t = []
    
    for x in range(l.ligne):
        for y in range(l.colonne):
            if l.tab[x][y].etat == False:
                # vérifie l'état des cases et stocke dans un tableau celles qui ont leur état à False              
                t.append(l.tab[x][y])
             
        # si le tableau est vide, le labyrinthe est valable et ne possède pas de case non valides
             
    if t == [] :       
        return True    
        
    return t  # renvoie le tableau contenant les cases non valides
                
      
#Zone de test :    

    

l = creation(20, 30)
 

#l = creation(randint(2,30), randint(5,30)) # on peut aussi faire des labyrinthes avec des longueur et largeur aléatoires
#On peut aussi créer de plus grand labyrinthe mais leur temps d'exécution est plus long 
#print(verif(l))   
print(explorer(l))


l.solution()     #Commande pour afficher la solution du labyrinthe, il faut fermer la première fenêtre pour que celle de la solution apparaisse 
        








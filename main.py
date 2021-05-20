import random
import numpy as np
from numpy import inf


alfa =1 # parametr sterujący ważnością intesywności śladu feromonowego
beta =2 #parametr sterujacy waznoscia widocznosci nastepnego miasta
vaporizationValue = 0.3

iloscMiast=4
miasta = [1,2,3,4]

distanceMatrix=np.matrix([
    [0,1,15,4], #start - 1 miasto
    [1,0,4,8],
    [15,4,0,5],
    [4,8,5,0]
])

routes=np.matrix([
    [1,0,0,0,0], #kazda mrowka startuje w miescie numer 1
    [1,0,0,0,0],
    [1,0,0,0,0],
    [1,0,0,0,0]
])




PheromoneValues = np.full((4,4),1.0)
visibilityMatrix = np.matrix((distanceMatrix.shape))
visibilityMatrix = 1/distanceMatrix             #podzielone przez zero zmienia sie na "inf"
visibilityMatrix[visibilityMatrix == inf] = 0    #wstawiamy tam zera


iteracje =1
numOfAnts = 4
przejscie =1 # okresla miasto w ktorym aktualnie jest mrowka


class Ant:

    def __init__(self, i):
        self.id = i
        self.PathLength =0


    def find(self):
        global przejscie
        actualPropabilities =[]
        for ite in range(iteracje):
            PathLength=0
            tempVisibilityMatrix = visibilityMatrix.copy()
            for iloscPrzejsc in miasta:#przejscie z miasta do miasta
                if iloscPrzejsc >= iloscMiast: #uwidaczniamy miasto numer 1
                    tempVisibilityMatrix[:,0] = visibilityMatrix[:,0]
                tempVisibilityMatrix[:, przejscie-1] = 0  # wylaczamy widocznosc dla odwiedzonych miast
                for miasto in miasta: #sprawdzenie drog w aktualnym miescie
                    print("MIASTO:")
                    print(miasto)
                    goraWzoru = (pow(PheromoneValues[przejscie-1, miasto-1], alfa) * pow(tempVisibilityMatrix[przejscie-1, miasto-1],beta))
                    print("GORA WZORU : ")
                    print(goraWzoru)
                    dolWzoru = np.multiply(np.power(PheromoneValues[przejscie-1,:],alfa), np.power(tempVisibilityMatrix[przejscie-1,:],beta))
                    dolWzoru[dolWzoru == inf] = 0
                    print("DOL WZORU : ")
                    print(dolWzoru)
                    print(np.sum(dolWzoru))
                    propability = goraWzoru/np.sum(dolWzoru)
                    actualPropabilities.append(propability)
                    print("PROPABILITY: ")
                    print(propability)
                print(
                    "LIST OF PROBPSPSP"
                )
                print(actualPropabilities)
                cumulativeSum =[]
                availableCities =[]
                availableCities.clear()
                cumulativeSum.clear()

                # liczenie cumulative sum i dodawanie dostepnych miast do listy
                cumulativeSum.append(1)
                whileIterator=0
                while len(actualPropabilities)>0:
                    x = actualPropabilities.pop(0)
                    if x != 0:
                        cumulativeSum.append(sum(actualPropabilities))
                        availableCities.append(whileIterator)
                        whileIterator += 1
                    elif( x == 0 ):  # usuwanie wszystkich zer
                            whileIterator += 1

                    #whileIterator +=1
                cumulativeSum.pop(-1) #usuniecie nadmiarowego zera


                r = random.uniform(0, 1)


                tempIterator=0
                for i in availableCities:
                    if tempIterator == len(availableCities)-1:
                        routes[self.id, iloscPrzejsc] = i + 1
                        przejscie = i + 1  # zmiana aktualnie badanego miasta
                        break
                    if (cumulativeSum[tempIterator] >= r and r > cumulativeSum[tempIterator+1]):
                        routes[self.id,iloscPrzejsc] = i+1
                        przejscie= i+1   # zmiana aktualnie badanego miasta
                        break
                    tempIterator += 1

                print(cumulativeSum)
                print(routes)

                aktualnaPozycja = routes[self.id, iloscPrzejsc-1]
                nowaPozycja = routes[self.id,iloscPrzejsc]

                PathLength += distanceMatrix[aktualnaPozycja-1,nowaPozycja-1]

            for miasto in range(routes.shape[1]-1): # aktualizacja feromonów
                PheromoneValues[routes[self.id,miasto]-1,routes[self.id,miasto+1]-1] +=1/PathLength
                PheromoneValues[routes[self.id,miasto+1]-1,routes[self.id,miasto]-1] +=1/PathLength



                actualPropabilities.clear()


a1=Ant(0)
a2=Ant(1)
a3=Ant(2)
a4=Ant(3)
a1.find()
a2.find()
a3.find()
a4.find()


print ("*********************")
print (routes)


#[wiersz,kolumna]



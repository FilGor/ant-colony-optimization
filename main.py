import random
import numpy as np
from numpy import inf


alfa =1 # parametr sterujący ważnością intesywności śladu feromonowego
beta =1 #parametr sterujacy waznoscia widocznosci nastepnego miasta

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

PheromoneValues = np.full((4,4),1)
visibilityMatrix = 1/distanceMatrix             #podzielone przez zero zmienia sie na "inf"
visibilityMatrix[visibilityMatrix == inf] = 0    #wstawiamy tam zera


iteracje =1
numOfAnts = 1


def find():
    actualPropabilities =[]
    for ite in range(iteracje):
        #aktualizacja feromonow
        tempVisibilityMatrix = visibilityMatrix
        for przejscie in miasta:#przejscie z miasta do miasta
            for miasto in miasta: #sprawdzenie drog w aktualnym miescie
                print("MIASTO:")
                print(miasto)
                goraWzoru = (pow(PheromoneValues[przejscie-1, miasto-1], alfa) * pow(tempVisibilityMatrix[przejscie-1, miasto-1],beta))
                print("GORA WZORU : ")
                print(goraWzoru)
                dolWzoru = np.multiply(PheromoneValues[przejscie-1,:], tempVisibilityMatrix[przejscie-1,:])
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
            test = np.cumsum(actualPropabilities)

            print(test)
            for prob in range(len(actualPropabilities)): #wylaczamy widocznosc dla odwiedzonych miast
                if actualPropabilities[prob] == 0:
                    tempVisibilityMatrix[przejscie, prob] = 0
                elif actualPropabilities[prob]< #tofinish
                    pass
            r = random.uniform(test[0], test[-1])
            actualPropabilities.clear()










              



find()
print ()
print (distanceMatrix[1,1])
print (PheromoneValues)


#[wiersz,kolumna]



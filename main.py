import random
import numpy as np
from numpy import inf


alfa =2 # parametr sterujący ważnością intesywności śladu feromonowego
beta =3 #parametr sterujacy waznoscia widocznosci nastepnego miasta
vaporizationValue = 0.3

iloscMiast=13
miasta = [1,2,3,4,5,6,7,8,9,10,11,12,13]

distanceMatrix=np.matrix([
        [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
        [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
        [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
        [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
        [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
        [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
        [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
        [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
        [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
        [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
        [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
        [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
        [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],

])

PheromoneValues = np.full((iloscMiast,iloscMiast),1.0)
visibilityMatrix = np.matrix((distanceMatrix.shape))
visibilityMatrix = 1/distanceMatrix             #podzielone przez zero zmienia sie na "inf"
visibilityMatrix[visibilityMatrix == inf] = 0    #wstawiamy tam zera


iteracje =10
numOfAnts = 10
przejscie =1 # okresla miasto w ktorym aktualnie jest mrowka

lengthsOfPaths =[]
class Ant:

    def __init__(self, i):
        self.id = i
        self.PathLength =0


    def find(self):
        global lengthsOfPaths
        global przejscie
        global PheromoneValues
        actualPropabilities =[]

        PheromoneValues = PheromoneValues * (1-vaporizationValue)
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
            actualPropabilities.clear()
        lengthsOfPaths.append(PathLength)
        for miasto in range(routes.shape[1]-1): # aktualizacja feromonów
            PheromoneValues[routes[self.id,miasto]-1,routes[self.id,miasto+1]-1] +=1/PathLength
            PheromoneValues[routes[self.id,miasto+1]-1,routes[self.id,miasto]-1] +=1/PathLength


def start():
    ants = [Ant(i) for i in range(numOfAnts) ]
    global routes
    routes = np.full((numOfAnts,iloscMiast+1),1)
    for ite in range(iteracje):
        for ant in ants:
            ant.find()
            print(ant.PathLength)

    print("*********************")
    print(routes)
    print(lengthsOfPaths)

start()




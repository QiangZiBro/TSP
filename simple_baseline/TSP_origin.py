# -*- coding: utf-8 -*-

import argparse
import operator
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser("TSP solver using GA")
parser.add_argument('--filename',default='./data/a280.tsp')
parser.add_argument('--show_figure',action='store_true',default='False') #False也能判断为真
parser.add_argument('--pop_size',type=int,default=100)
parser.add_argument('--elite_size',type=int,default=20)
parser.add_argument('--generations',type=int,default=500)
parser.add_argument('--mutation_rate',type=float,default=0.01)
parser.add_argument('--answer_filename',default='./data/a280.opt.tour')
args = parser.parse_args()



class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness

def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route

def initialPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population

def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults


def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
    
    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute

def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations,show_figure=True):
    pop = initialPopulation(popSize, population)
    distance = 1 / rankRoutes(pop)[0][1]
    min_distance = distance
    progress = []
    progress.append(distance)
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        distance = 1 / rankRoutes(pop)[0][1]
        progress.append(distance)

        if distance < min_distance:
            min_distance = distance
            print("----------Find shorter distance----------")
            print("Route:")
            bestRouteIndex = rankRoutes(pop)[0][0]
            bestRoute = pop[bestRouteIndex]
            print(bestRoute)
            print("Route Length")
            print(min_distance)


        if show_figure is True:

            #动态画图
            plt.cla()
            plt.title('TSP problem')
            plt.ylabel('Distance')
            plt.xlabel('Generation')
            plt.plot(progress)
            plt.pause(0.000000001)

    if show_figure is True: 
        plt.ioff()
        plt.show()

def process_input(s):
    s = ''.join(s.split('\n'))
    s = s.split(' ')
    s = [int(i) for i in s if i != ''][1:]
    return s[0],s[1]

def input_answers(cityList,filename=None):
    if filename is None:
        return None
    ans = []
    with open(filename,'r') as f:
        line = f.readline().split('\n')[0]
        line = int(line)
        while line != -1:
            ans.append(line)
            line = f.readline().split('\n')[0]
            line = int(line)

    return [cityList[i-1] for i in ans]


def input_cities(filename):
    cityList = []
    with open(filename,'r') as f:
        line = f.readline()
        while line != "EOF\n":
            x,y = process_input(line)
            cityList.append(City(x,y))
            line = f.readline()
    return cityList

if __name__ == "__main__":
    cityList = input_cities(args.filename)
    answer_route = input_answers(cityList, args.answer_filename)
    answer_distance = Fitness(answer_route).routeDistance()
    print("best answer ever:",answer_distance)

    geneticAlgorithmPlot(population=cityList, popSize=args.pop_size, eliteSize=args.elite_size, mutationRate=args.mutation_rate, generations=args.generations,show_figure=args.show_figure)

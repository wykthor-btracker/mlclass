#!/usr/bin/python # -*- coding: utf-8 -*-
#imports#
from math import sqrt
from requests import get
from random import randint,random
from operator import attrgetter as attget
from copy import deepcopy
#imports

#variables#

#variables

#classes#
class individual:
	def __init__(self,pairs):
		self.pairs = pairs
		self.fitness = 0
		self.nodes = []
		self.speed = 5
		self.expected = 0
		self.__class__ = individual
		return None
	def __eq__(self,other):
		if isinstance(self,other.__class__):
			return self.__dict__ == other.__dict__
		return False
	def __ne__(self,other):
		return not self.__eq__(other)

	def rand(self):
		for i in range(3):
			for u in range(2):
				self.pairs[i][u] = randint(0,360)
		
	def findNodes(self):
		self.nodes = []
		if(self.speed<=0):
			return 0
		for k in range(3):
			flag = 1
			pairsL = []			
			for i in range(2):
				attempt = [self.pairs[k][0]+flag*self.speed,self.pairs[k][1]+flag*self.speed]
				if(attempt[0] >= 0 and attempt[1] >= 0):
					pairsL.append(attempt)
				attempt = [self.pairs[k][0]+flag*self.speed,self.pairs[k][1]-flag*self.speed]
				if(attempt[0] >= 0 and attempt[1] >= 0):
					pairsL.append(attempt)
				flag*=-1
			self.nodes.append(pairsL)
	
	def testNodes(self):
		if(self.speed<=0): 
			return 0
		maxFitness = self.fitness
		maxChange=[]
		flag = 0
		for i in range(len(self.nodes)):
			for u in range(len(self.nodes[i])):
				self.pairs[i] = self.nodes[i][u]
				self.getFitness()
				if self.fitness>maxFitness:
					maxFitness = self.fitness
					maxChange = deepcopy(self)
					flag=1
		if(flag==1):
			self.pairs = maxChange.pairs
		else:
			self.speed-=1
		self.getFitness()
				

	def getFitness(self):
	        resp = get("http://localhost:8080/antenna/simulate?phi1=%d&theta1=%d&phi2=%d&theta2=%d&phi3=%d&theta3=%d" % (self.pairs[0][0],self.pairs[0][1],self.pairs[1][0],self.pairs[1][1],self.pairs[2][0],self.pairs[2][1])).text
		resp = resp.split('\n')[0]
		resp = float(resp)
		self.fitness = resp
			

	def mutate(self,chance):
		if(randint(0,1000) < chance):
			self.pairs[randint(0,2)][randint(0,1)]+=randint(0,10)
			self.getFitness()
	
	def show(self):
		print("pair1:(%d,%d)\npair2:(%d,%d)\npair3:(%d,%d)\nfitness:%f\n" % (self.pairs[0][0],self.pairs[0][1],self.pairs[1][0],self.pairs[1][1],self.pairs[2][0],self.pairs[2][1],self.fitness))
	def export(self):
		return "pair1:(%d,%d)\npair2:(%d,%d)\npair3:(%d,%d)\nfitness:%f\n" % (self.pairs[0][0],self.pairs[0][1],self.pairs[1][0],self.pairs[1][1],self.pairs[2][0],self.pairs[2][1],self.fitness)

class generation:
	def __init__(self,size):
		self.pop = [individual([[0,0],[0,0],[0,0]]) for i in range(size)]
		for i in range(size):
			self.pop[i].rand()
			self.pop[i].getFitness()
		self.sort()
		self.size = size
		self.average = average(self.pop)
		self.staDev = standardDeviation(self.pop)
		self.sumFit = sumFit(self.pop)
		self.best = self.pop[-1] 
		return None

	def update(self):
		self.sort()
		self.average = average(self.pop)
		self.staDev = standardDeviation(self.pop)
		self.sumFit = sumFit(self.pop)
		self.best = self.pop[-1]
		
	def findBreeders(self,bestS,luckyF):
		size = int(len(self.pop)/2)
		bestSample = int(size*bestS)
		luckyFew = int(size*luckyF)
		while(bestSample+luckyFew!=size):
			luckyFew+=1
		self.sort()
		breeders = []
		for i in range(bestSample):
			while(self.pop[-i] in breeders):
				i+=1
			breeders.append(self.pop[-i])
		Lucky = 0
		for i in range(luckyFew):
			while(self.pop[Lucky] in breeders):
				Lucky = randint(0,self.size-1)
			breeders.append(self.pop[Lucky])
		return breeders

	def sort(self):
		self.pop = sorted(self.pop, key=attget('fitness'))

	def nextGen(self,breeders):
		newGen = []
		size = len(breeders)
		while len(newGen)<size*2:
			parent1, parent2 = 0,0
			while parent1==parent2:
				parent1 = randint(0,size-1)
				parent2 = randint(0,size-1)
			child = makeLove((breeders[parent1],breeders[parent2]))
			newGen.append(child[0])
			newGen.append(child[1])
			self.pop = newGen
	def mutateGen(self,chance):
		for i in self.pop:
			i.mutate(chance)
			
#classes

#functions#
def flip(what):
	if what==0:
		return 1
	else:
		return 0
def makeLove(parents):
	pair1 = randint(0,1)
	pair2 = randint(0,1)
	pair3 = randint(0,1)
	child = []
	child.append(individual([parents[pair1].pairs[0],parents[pair2].pairs[1],parents[pair3].pairs[2]]))
	child.append(individual([parents[flip(pair1)].pairs[0],parents[flip(pair2)].pairs[1],parents[flip(pair3)].pairs[2]]))
	if (child[0] == parents[0] and child[0] == parents[1]):
		child[0].rand()
	if (child[1] == parents[0] and child[1] == parents[1]):
		child[1].rand()
	child[0].getFitness()
	child[1].getFitness()
	if(child[0]==child[1]):
		print("Oops, duplicate")
		child[1].rand()
	return child
def domination(child,parent1,parent2):
	if(child.fitness>parent1.fitness and child.fitness>parent2.fitness):
		return 2
	elif(child.fitness>parent1.fitness or child.fitness>parent2.fitness):
		return 1
	else:
		return 0
def average(gen):
	sumOfFit = sumFit(gen)
	return sumOfFit/len(gen)
def standardDeviation(gen):
	sumOfDistancesSquared = 0
	for i in gen:
		sumOfDistancesSquared+=(average(gen)-i.fitness)**2
	sumOverSize = sumOfDistancesSquared/len(gen)
	standardDeviation = sqrt(sumOverSize)
	return standardDeviation
def sumFit(gen):
	x = 0
	for i in gen:
		x+=i.fitness
	return x
#functions

#main#
def main():
	size = int(input("Choose initial generation size: "))
	gens = int(input("Choose number of generations to run: "))
	chance = int(input("Choose chance of mutation(0-1000): "))
	luckyF, bestS = 0,0
	gen = generation(size)
	bestS = float(input("Input the percentage of the population that should breed because they're good. The remainder will be\n comprised of random individuals: "))
	luckyF = 1-bestS
	maxind = gen.best
	step = 0
	best = []
	for i in range(gens):
		gen.update()
		best.append(gen.best)
	 	breeders = gen.findBreeders(bestS,luckyF)
		gen.nextGen(breeders)
		gen.mutateGen(chance)
		gen.update()
		print("Some measure: %f" % (gen.best.fitness-gen.average))
		print("Best of generation %d" % i)
		print("Mutation chance: %.1f%%" % (float(chance)/10))
		gen.best.show()
		if gen.best.fitness > maxind.fitness:
			maxind = gen.best
		if(gen.best.fitness-gen.average<0.5 and i%10==0):
			print("Mixing it up!")
			for i in gen:
				i.rand()
			gen.best = maxind
		if(step):
			choice = raw_input("Do you want to (c)ontinue, (s)ave the curr\nent generation, or (q)uit?")
			if(choice=='c'):
				continue
			elif(choice=='s'):
				with open('log.txt','w') as f:
					for i in gen.pop:
						f.write(g.export())
			elif(choice == 'q'):
				resp = get("https://aydanomachado.com/mlclass/02_Optimization.php?phi1=%d&theta1=%d&phi2=%d&theta2=%d&phi3=%d&theta3=%d&dev_key=%s" % (maxind.pairs[0][0],maxind.pairs[0][1],maxind.pairs[1][0],maxind.pairs[1][1],maxind.pair[2][0],maxind.pair[2][1],"Tô%20de%20ouvinte"))
				print(resp.text)
				break
	best = maxind
	resp = get("https://aydanomachado.com/mlclass/02_Optimization.php?phi1=%d&theta1=%d&phi2=%d&theta2=%d&phi3=%d&theta3=%d&dev_key=%s" % (best.pairs[0][0],best.pairs[0][1],best.pairs[1][0],best.pairs[1][1],best.pairs[2][0],best.pairs[2][1],"Tô%20de%20ouvinte"))
	print(resp.text)	
	return 0
	
if __name__ == "__main__":
	main()
#main

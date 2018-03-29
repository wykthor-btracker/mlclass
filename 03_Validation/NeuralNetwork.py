# -*- encoding:utf-8 -*-
#imports#
import math
import os
import pandas as pd
import random
#imports

#variables#
#variables

#classes#
class Perceptron:
	def __init__(self,activation): #Only define activation on input layers
		self.weight = 0
		self.bias = 0
		self.activationVal = activation
		self.slope = 0
		self.errorGradient = 0
		self.delta = 0
		
	def rand(self):
		self.weight = random()
		self.bias = random()
		
	def updateBias(self, bias):
		self.bias = bias
		
	def updateWeight(self, weight):
		self.weight = weight
	
	def activation(self, x): #Activation is done through a sigmoid function
		result = x*self.weight+self.bias
		self.activationVal = 1/(1+np.exp(-result))
	
	def getSlope(self): #Derivative of the sigmoid
		self.slope = self.activationVal*(1-self.activationVal)
		
	def getError(self,real):#Only used on the output layer
		self.errorGradient = real-activationVal
		
	def getDelta(self,error,learningRate):#Learning Rate = 1 when resolving for hidden layers
		self.delta = error*self.slope*learningRate
		
class Layer:
	def __init__(self,learningRate,inputLayer):
		self.neurons = []#List of the neurons for this layer
		self.inputLayer = []#The preceeding layer's neurons
		self.sumOfInputActivations = 0
		self.sumOfNeuronActivations = 0
		self.learningRate = learningRate #learningRate = 1 everywhere but output layers
		
	def applyActivations(self):
		self.sumOfInputActivations = 0
		for node in self.inputLayer:#sums the activations
			self.sumOfInputActivations+=node.activationVal
			
		for neuron in self.neurons:#applies the sigmoid function on the sum
			neuron.activation(self.sumOfInputActivations
			self.sumOfNeuronActivations+=neuron.activationVal
			
	def updateWeights(self,sumOfActivations,learningRate,expectedOutput):
		for neuron in self.neurons:
			neuron.getError(expctedOutput)			
			for node in self.inputLayer:
				neuron.weight+= node.activationVal*neuron.errorGradient*learningRate
				
	def applyDeltas(self,error):
		for neuron in self.neurons:
			neuron.getSlope()
			neuron.getDelta(error,self.learningRate)
			
	def updateBias(self,error):
			for neuron in self.neurons:
				neuron.bias+=neuron.delta
			
#classes

#functions#
#functions

#main#
def main():
	database = pd.read_csv('abalone_app.csv')
	
	return None
#main

if __name__=="__main__":
	main()

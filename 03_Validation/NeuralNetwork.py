# -*- encoding:utf-8 -*-
#imports#
import math
import os
import pandas as pd
from random import random
#imports

#variables#
#variables

#classes#
class Perceptron:
	def __init__(self,activation,numberOfInputs): #Only define activation on input layers
		self.weights = []
		self.bias = 0
		self.numbOfInputs = numberOfInputs
		self.activationVal = activation
		self.slope = 0
		self.errorGradient = 0
		self.delta = 0
		
	def rand(self):
		self.weight = [random() for i in range(self.numbOfInputs)]
		self.bias = random()
		
	def updateBias(self, bias):
		self.bias = bias
		
	def updateWeights(self, weights):
		self.weights = weights
	
	def activation(self, x): #Activation is done through a sigmoid function, x should be the sum of the activations*respectiveWeights+bias
		self.activationVal = 1/(1+np.exp(-x))
	
	def getSlope(self): #Derivative of the sigmoid
		self.slope = self.activationVal*(1-self.activationVal)
		
	def getErrorOutput(self,real):#Only used on the output layer
		self.errorGradient = real-activationVal
	
	def getErrorHidden(self,weight,delta):
		self.errorGradient = weight*delta
		
	def getDelta(self,error,learningRate):#Learning Rate = 1 when resolving for hidden layers
		self.delta = error*self.slope*learningRate
		
class Layer:
	def __init__(self,numberOfNeurons,inputLayer,learningRate):
		self.neurons = []#List of the neurons for this layer
		self.inputLayer = inputLayer#The preceeding layer's neurons
		self.sumOfInputActivations = 0
		self.learningRate = learningRate #learningRate = 1 everywhere but output layers
		for neuron in range(numberOfNeurons):
			self.neurons.append(Perceptron(0))
		for neuron in self.neurons:
			neuron.rand()
			
	def applyActivations(self):
		for neuron in self.neurons:#applies the sigmoid function on the sum
			self.sumOfInputActivations = 0		
			for i in range(len(self.inputLayer)):#len(neuron.weights)==len(self.inputLayer), else it borks
				self.sumOfInputActivations+= self.inputLayer[i].activationVal*neuron.weights[i]+neuron.bias#neuron.weights is organized in a way such that it should align with the incoming neurons, to give them their weights
			neuron.activation(self.sumOfInputActivations)
			
	def getSlope(self):
		for neuron in self.neurons:
			neuron.getSlope()
			
	def applyDeltas(self):
		for neuron in self.neurons:
			neuron.getDelta(self.errorGradient,self.learningRate)
			
	def updateWeights(self):
		
	def updateBias(self):
			for neuron in self.neurons:
				neuron.bias+=neuron.delta
			
#classes

#functions#
#functions

#main#
#  
#  name: main
#  @param
#  @return
#  
def main():
	database = pd.read_csv('abalone_dataset.csv')
	database.sex.replace(['M','F','I'],[2,1,0],inplace=True)
	inputLayer = []
	numberOfInputs = 8
	numberOfOutputs = 3
	learningRate = 0.1
	epoch = 5000
	inputs = {'sex':1,'length':1,'diameter':1,'height':1,'whole_weight':1,'shucked_weight':1,'viscera_weight':1,'shell_weight':1}
	output = 'type'
	for item,key in inputs.items():
		if(key):
			inputLayer.append(database[item][0])
	hiddenLayer = Layer(((numberOfInputs+numberOfOutputs)/2),inputLayer,1) 	#Creates hidden neurons and randomizes them as this is the first epoch
	hiddenLayer.applyActivations()											#Calculates the input*weight+bias for all neurons, and saves it to each neurons activationVal, ergo, their outputs
	outputLayer = Layer(numberOfOutputs,hiddenLayer,learningRate) 			#Creates output neurons and randomizes them too
	outputLayer.applyActivations()											#Calculates the input*weight+bias for all neurons, outputs it, as this is the 'answer' of the NN
	for neuron in outputLayer:
		if(outputLayer[database[output][0]]-1==neuron):						#Database[output] ranges from 1-3, so we subtract one to map them to the indexes of the output layer list
			neuron.getError(1)												#Calculates Real-predicted, on the output layer, we have each neuron firing up if it is the correspondent to the answer
		else:
			neuron.getError(0)
	hiddenLayer.getSlope()													#Calculates the derivative of the activation function
	outputLayer.getSlope()
	outputLayer.applyDeltas()
	for node in hiddenLayer:
		node.getErrorHidden(
	
	return None
#main

if __name__=="__main__":
	main()

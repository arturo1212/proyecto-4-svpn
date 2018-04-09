# Script que permite crear casos de prueba para los tableros.
import random
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import scipy.misc
from scipy.misc import imshow
import pickle

def picture_russel_maze(maze, filename):
	# Filename tiene el nombre del archivo de salida
	#f = open("Results/SAToutput/" + filename + '.txt', 'r')	# Abrir archivo
	plt.imsave("Results/Images/PDF/image_" + filename + ".pdf", (1-np.array(data)).reshape(maze.height, maze.width), cmap=cm.gray)
	f.close()

class russel_maze_inst():
	def __init__(self, n, m, obstacleN = 2):
		self.vector = [0] * n*m
		self.obstacles = []
		self.goal_plus  = 0
		self.goal_minus = 0
		self.width  = n 
		self.height = m

		# Crear meta positiva
		self.obstacles = random.sample(range(0, n*m -1), obstacleN + 2)	
		self.goal_plus = random.choice (self.obstacles)

		# Crear meta negativa
		self.obstacles.remove(self.goal_plus)
		self.goal_minus = random.choice (self.obstacles)
		self.obstacles.remove(self.goal_minus)

		for pos in self.obstacles:
			self.vector[pos] = 10

		self.vector[self.goal_plus] = 1
		self.vector[self.goal_minus] = 5

def create_cases(width, height, obstacles, caseN):
	aux = 0
	cases = []
	while(aux < caseN):
		data = russel_maze_inst(width, height, obstacles)
		if(not data in cases ):
			#print(data)
			cases.append(data)
			aux+=1
	return cases

def create_test_file(width, height, cases):
	result = str(width) + " " + str(height) + "\n"
	for case in cases:
		result+= ' '.join(str(e) for e in case.vector) + "\n"
		
	#print(result)
	file_name = "test/Russel-maze/" + str(width) + "x" + str(height) + "_maze.cases"
	f = open(file_name, 'w')
	f.write(result)

width, height = 20, 10
cases = create_cases(width, height, 7, 20)
create_test_file(width, height, cases)
#imshow((1-np.array(data.vector)).reshape(data.height, data.width))

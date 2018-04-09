from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import scipy.misc
import generator

def directory_files(mypath):
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	filenames = [(f.split("."))[0] for f in onlyfiles]
	return filenames

class maze_case():
	def __init__(self, data, width, height):
		self.width, self.height = width, height
		self.matrix = (np.array(data)).reshape(height, width)

def create_file_cases(filename):
	result = []
	f = open(filename, 'r')
	width, height = -1, -1
	for line in f:
		if(width == -1):
			[width,height] = line.split(' ')
		else:
			data = (line.strip()).split(' ')
			data = list(map(float, data))
			result.append(maze_case(data, int(width), int(height)))
	return result

def is_obstacle(pos):
	return pos == 10

def is_good(pos):
	return pos == 1

def is_bad(pos):
	return pos == 5

def solve_case(case):
	observs = []
	rewards = []
	transitions = {"n":[], "s":[], "w":[], "e":[]}
	# ------------------- Crear transiciones ------------------------- #
	# 						 (n, s, e, w)	
	for key, matrix in transitions.items(): # Crear transiciones para cada movimiento
		# FALTA CASO DE LOS ABSORBS
		print("KEY: " + key)
		for i in range(0, case.height):		# Crear transiciones para cada estado valido
			for j in range(0, case.width):	
				if(is_obstacle(case.matrix[i][j])):								# No calcular para los obstaculos
					continue
				if(is_good(case.matrix[i][j]) or is_bad(case.matrix[i][j])):	# Absorciones
					# Caso de restart
					continue

				aux_matrix = case.matrix.copy()
				aux_matrix[:][aux_matrix[:]<10] = 0

				# MOVIMIENTO NORMAL
				if(key == 'n'): 	# Arriba 0.8, A los lados  0.10
					# Casos de paredes (INTENCION)
					if(i-1 < 0 or aux_matrix[i-1][j] > 1):			# Intencion
						aux_matrix[i][j] += 0.8
					else:
						aux_matrix[i-1][j] += 0.8
				elif(key == "s"): 	# Abajo 0.8 , A los lados  0.10
					# Casos de paredes (Intencion y perpendiculares)
					if(i+1 >= case.height or aux_matrix[i+1][j] > 1):			# Intencion
						aux_matrix[i][j] += 0.8
					else:
						aux_matrix[i+1][j] += 0.8
				elif(key == "w"): 	# Izqui 0.8 , Arriba/Abajo 0.10
					if(j-1 < 0 or aux_matrix[i][j-1] > 1):
						aux_matrix[i][j] += 0.8
					else:
						aux_matrix[i][j-1] += 0.8
				elif(key == "e"): 	# Derec 0.8 , Arriba/Abajo 0.10
					if(j+1 >= case.width or aux_matrix[i][j+1] > 1):
						aux_matrix[i][j] += 0.8
					else:
						aux_matrix[i][j+1] += 0.8

				# MOVIMIENTO PERPENDICULAR
				if(key == 'n' or key == 's'):				# PERPENDICULARES horizontales
					if(j-1 < 0 or aux_matrix[i][j-1] > 1):			# Pared lateral
						aux_matrix[i][j] += 0.1
					else:
						aux_matrix[i][j-1] += 0.1
					if(j+1 >= case.width or aux_matrix[i][j+1] > 1):			# Pared lateral
						aux_matrix[i][j] += 0.1
					else:
						aux_matrix[i][j+1] += 0.1
				elif(key == 'w' or key == 'e'):				# PERPENDICULARES verticales
					if(i-1 < 0 or aux_matrix[i-1][j] > 1):
						aux_matrix[i][j] += 0.1
					else:
						aux_matrix[i-1][j] += 0.1
					if(i+1 >= case.height or aux_matrix[i+1][j] > 1):
						aux_matrix[i][j] += 0.1
					else:
						aux_matrix[i+1][j] += 0.1

				line = aux_matrix.ravel()
				line = [e for e in line if e <= 1]
				transitions[key].append(line)
				print(line)
			
	# ------------------- Crear observaciones ------------------------ #
	#            (left, right, neither, both, good, bad)			   #
	for row in case.matrix:
		for i in range(0, len(row)):
			if(row[i] == 10):	# No crear para los obstaculos.
				continue
			# CASOS	
			if(is_good(row[i])):
				observs.append("0.0 0.0 0.0 0.0 1.0 0.0")		# Estados finales
			elif(is_bad(row[i])):						
				observs.append("0.0 0.0 0.0 0.0 0.0 1.0")
			elif(i-1 < 0 or is_obstacle(row[i-1]) and (i+1 >= case.width or is_obstacle(row[i+1]))):
				observs.append("0.0 0.0 0.0 1.0 0.0 0.0")# Pared a ambos lados
			elif(i-1 < 0 or is_obstacle(row[i-1])):				# Caso ver a la izquierda
				observs.append("1.0 0.0 0.0 0.0 0.0 0.0")	
			elif(i+1 >= case.width or is_obstacle(row[i+1])):	# Caso pared a la derecha
				observs.append("0.0 1.0 0.0 0.0 0.0 0.0")
			else:											# No ver paredes
				observs.append("0.0 0.0 1.0 0.0 0.0 0.0")

	# ------------------ Crear costos/recompensas -------------------- #
	for row in case.matrix:
		for value in row:
			if(value == 1):
				rewards.append(1)
			elif(value == 5):
				rewards.append(-1)
			elif(value == 0):
				rewards.append(-0.04)
	return rewards, observs, transitions


test_files = directory_files("test/Russel-maze") # Extraer los archivos del directorio test
file_cases = create_file_cases("test/Russel-maze/" + test_files[0] + ".cases")
# FALTA: CREAR ARCHIVO POMDP Y Guardar .pomdp en directorio POMDP
for case in file_cases:
	rewards, observs, transitions = solve_case(case)	# EN PROCESO: TRANSICIONES
	print("#############")
	#print(case.matrix)
	#print(observs)
print(len(file_cases))
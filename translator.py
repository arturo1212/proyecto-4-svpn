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

def create_start(case):
	obstacles = np.count_nonzero(case.matrix == 10) # Contar peroles
	total_states = case.width*case.height - (obstacles + 2)
	value = 1.0/total_states 

	line = case.matrix.ravel()
	line = [e for e in line if e < 7]	# Quitar los obstaculos
	line = [value if e!=5 and e!=1 else 0.0 for e in line]
	return line # FALTA CASO EN EL QUE LA DIVISION NO DA EXACTA	

def solve_case(case):
	observs = []
	rewards = []
	transitions = {"n":[], "s":[], "w":[], "e":[]}
	# ------------------- Crear transiciones ------------------------- #
	# 						 (n, s, e, w)	
	for key, matrix in transitions.items(): # Crear transiciones para cada movimiento
		# FALTA CASO DE LOS ABSORBS
		for i in range(0, case.height):		# Crear transiciones para cada estado valido
			for j in range(0, case.width):	
				if(is_obstacle(case.matrix[i][j])):								# No calcular para los obstaculos
					continue
				if(is_good(case.matrix[i][j]) or is_bad(case.matrix[i][j])):	# Absorciones
					transitions[key].append(create_start(case))# Caso de restart
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
				#print(line)
			
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

def print_maze(case):
	result = "#  "+ "#"*case.width*2+"#\n"
	for line in case.matrix:
		string = " ".join(str(int(e)) for e in line)
		string = string.replace("10","#")
		string = string.replace("5", "-")
		string = string.replace("1", "+")
		result += "#  #" + string   + '#\n'
	result+= "#  "+ "#"*case.width*2+"#\n"
	return result

def translate_pomdp(filename, case):
	obstacles = np.count_nonzero(case.matrix == 10) # Contar peroles
	discount, total_states =0.95, case.width*case.height - obstacles
	rewards, observs, transitions = solve_case(case)
	str_rewards, str_observations, str_trans = "", "O: *\n", ""
	f = open("POMDP/" + filename+".POMDP", 'w')
	Header = """########################################
# FILENAME: %s
#CASE: (0, white) ; (# , Wall) ; (+ , reward) ; (-, penalty)
%s
discount: %f
values: reward
states: %d
actions: s e w n
observations: left right neither both good bad
\n""" % (filename,print_maze(case), discount, total_states)

	for key, value in transitions.items():
		str_trans+= "T: %s \n" % (key)
		for line in value:
			#aux = line.tolist()
			aux = " ".join(str(e) for e in line)
			str_trans += aux + "\n"
		str_trans+= "\n"

	for i in range(0,total_states):
		str_observations += observs[i] + "\n"
		str_rewards += "R: * : %d : * : * %f\n" % (0, rewards[i])
	result = Header + str_trans + str_observations + "\n" + str_rewards
	f.write(result)
	print(result)
	f.close()

test_files = directory_files("test/Russel-maze") # Extraer los archivos del directorio test
for file in test_files:
	file_cases = create_file_cases("test/Russel-maze/" + file + ".cases")
	# FALTA: CREAR ARCHIVO POMDP Y Guardar .pomdp en directorio POMDP
	count = 1
	for case in file_cases:
		translate_pomdp(file+"case"+str(count), case)	# EN PROCESO: TRANSICIONES
		print_maze(case)
		count+= 1
	#print(len(file_cases))

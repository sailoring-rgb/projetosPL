from asyncore import read
from fileinput import filename
import re
import sys
from typing import List, Tuple

######### IMPORTS NEEDED FOR TESTING #########
import json 
import csv 

# FUNÇÃO RESPONSÁVEL POR PROCESSAR O CABEÇALHO DO FICHEIRO CSV
def header(line) -> Tuple[str, List[str]]:

	columnNames = []                                    # contem o nome das colunas
	columnOperations = []                               # contem as funções de agreg. que serão feitas para cada campo se este corresponder a uma lista
	functions = ["sum","media","min","max","count"]     # as funções de agreg. possíveis

	semicolon = re.match(r'(?:(.*?));',line)
	if semicolon:
		separator = ";"
	else:	
		comma = re.match(r'(?:(.*?)),',line)
		if comma:
			separator = ","

	elements = re.findall(r'([^;:,{]+)(?:{(.*?)})?(?:\:\:(.*?)(?:;|,))?', line)
	
	for i in elements:
		columnNames.append(i[0])
		if len(list(filter(None,i))) == 1:
			t = (i[0],0,"none")
			columnOperations.append(t)
		elif len(list(filter(None,i))) == 2:
			t = (i[0],i[1],"none")
			columnOperations.append(t)
		else:
			# a função de agregação passada não é reconhecida
			if i[2] not in functions:
				raise NameError
			else:
				t = (i[0],i[1],i[2])
				columnOperations.append(t)
	return separator,columnOperations


# FUNÇÃO RESPONSÁVEL POR CALCULAR O MÁXIMO COMPRIMENTO DE UMA LISTA -- CASO EM QUE TEMOS UM INTERVALO DE VALORES {3,5}
def calculateLength(string: str):
	res = string.split(",")
	if len(res) == 1:
		length = res[0]
	else:
		length = res[1]
	return length


# FUNÇÃO RESPONSÁVEL POR APLICAR A FUNÇÃO DE AGREGAÇÃO PASSADA NO CABEÇALHO À RESPETIVA UMA COLUNA
def executeFunction(columnName:str, function: str, values: List[int]):
	if function == "sum":
		res = f'"{columnName}_sum": {sum(values)}'
	elif function == "media":
		res = f'"{columnName}_media": {sum(values)/len(values)}'
	elif function == "min":
		res = f'"{columnName}_min": {min(values)}'
	elif function == "max":
		res = f'"{columnName}_max": {max(values)}'
	elif function == "count":
		res = f'"{columnName}_count": {len(values)}'
	elif function == "none":
		res = f'"{columnName}": {values}'
	return res


# FUNÇÃO RESPONSÁVEL POR PROCESSAR UMA LINHA DO FICHEIRO CSV (SEM SER O CABEÇALHO)
def processLine(separator: str, columnOperations: List[str], line: str):
	# expressão para apanhar apenas keys e values: (\d+|(?i)([a-zà-ü]+(?-i)\s*)*)

	result = []                         # exemplo: result = ["Número": "12334", "Nome": "Cândida", "Curso": "Desporto", "Notas_media": 15.3]
	pos = 0

	if separator == ";":
		elements = line.split(";")
	else:
		elements = line.split(",")

	# i : (Column Name, Length if List, Fuction Name)
	for op in columnOperations:

		length = int(calculateLength(str(op[1])))
		list = []

		if length > 0:
			if separator == ";":
				for i in elements[pos].split(","):
					if re.match(r'^-?\d+(?:\.\d+)?$', i):
						list.append(i)
			else:    														# se o separador for uma vírgula
				for i in elements[pos:(pos+length)]:
					if re.match(r'^-?\d+(?:\.\d+)?$', i):
						list.append(i)
						
			values = [int(value) for value in list]
			
			res = executeFunction(op[0],op[2],values)
			result.append(res)
		else:
			result.append(f'"{op[0]}": {elements[pos]}')

		pos = pos + 1
	#print(result)
	return result


# FUNÇÃO RESPONSÁVEL POR CONVERTER PARA JSON
def prepareJSON(dicionario, columnOperations):
	res = "[\n" # Incío do ficheiro JSON
	for dic_entry in dicionario:
		res += "\t{\n" # Incío de um dicionário
		for i in range(len(columnOperations)):
			name = columnOperations[i][0]
			if dic_entry[name] == "": # Caso não exista nenhum valor, a chave não é introduzida no dicionário
				break
			elif "_" in dic_entry[name]:
				
				name_regex = re.compile(r'(\w+_\w+)')
				func_name = name_regex.match(dic_entry[name])
				if func_name:
					res += "\t\t\""+ func_name.group() + "\": "
				value = re.compile(r'\d+((.|,)\d+)?')
				val = re.search(value, dic_entry[name])
				if val:
					res += val.group()				
			else:
				res += "\t\t\""+ name + "\": "
				if "," in dic_entry[name]: # Verifica se o valor é uma lista
					res += dic_entry[name].replace(" ","") # Remove os espaços da lista
				else:
					res += "\"" + dic_entry[name] + "\"" # Coloca o valor da chave entre aspas
			if i == len(columnOperations) - 1:
				res += "\n"	# Se for a última chave do dicionário não se acresventa a vírgula
			else:
				res += ",\n"
		res += "\t},\n" # Fim de um dicionário
	res = res[:-2]
	res += "\n]" # Final do ficheiro JSON
	return res

#################################################### MAIN ####################################################

# ABRIR E LER O FICHEIRO
file_name = input("Inserir nome do ficheiro a converter: ")

try:
	file = open("../input/"+file_name+".csv")
	lines = file.read().splitlines()
	file.close()

	# REMOVER LINHAS VAZIAS DO INPUT
	for line in lines:
		if line == '':
			lines.remove(line)

	# PROCESSAR O HEADER -- SE A FUNÇÃO DE AGREGAÇÃO NÃO EXISTIR, É LANÇADA UMA EXCEÇÃO
	try:
		separator,columnOperations = header(lines[0])
		lines.remove(lines[0])
	except NameError:
		print("Unsupported function")

	# PROCESSAR AS RESTANTES LINHAS DO FICHEIRO
	rule = re.compile(r'(?!"([a-zà-ü]+":))( .*)') # RegEx used to access the value of each column
	full_dic = [] # List to contain the several dictionaries generated by CSV file

	for line in lines: # Loop cicle to create a dictionary for each entry of the CSV file
		dicionario = {}
		res = processLine(separator,columnOperations,line)
		for i in range(len(columnOperations)):
			m = re.search(rule,res[i])
			if m:
				dicionario[columnOperations[i][0]] = m.group()[1:]
		full_dic.append(dicionario.copy())

	outData = prepareJSON(full_dic,columnOperations)
	print(outData)

	# GUARDAR O OUTPUT GERADO fileOUTPUT ......
	#outputTest = open("../output/test.json","w")
	#outputFile = open("../output/work.json","w")
	#json.dump(full_dic,outputTest,indent=6) 		# for testing
	#outputFile.write(outData)

except FileNotFoundError as e:
    print(f"Ficheiro inválido: o \"{file_name}\" não foi encontrado!")
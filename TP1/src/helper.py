import re
import os
from typing import List

# MENUS A APRESENTAR
menu_file = {
    1: 'CSV file',
    2: 'JSON file',
    0: 'Exit',
}

menu_initial = {
    1: 'Convert file',
    2: 'View file',
    0: 'Exit',
}

# IMPRESSÃO DO MENU
def print_menu(menu_opts):
    for key in menu_opts.keys():
        print(key, '::', menu_opts[key])

# LIMPAR A CONSOLA
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

# FUNÇÃO PARA PROCESSAMENTO INICIAL DO INPUT
def cleanInput(lines):
	lines = list(map(lambda st: re.sub(r';|\||\t',r',',st), lines))
	# REMOVER LINHAS VAZIAS DO INPUT
	for line in lines:
		if line == '':
			lines.remove(line)
	return lines

# FUNÇÃO RESPONSÁVEL POR PROCESSAR O CABEÇALHO DO FICHEIRO CSV
def header(line):

	columnOperations = []                               # contem as funções de agreg. que serão feitas para cada campo se este corresponder a uma lista
	functions = ["sum","media","min","max","count"]     # as funções de agreg. possíveis

	elements = re.findall(r'([^;:,{]+)(?:{(.*?)})?(?:\:\:(.*?)(?:;|,))?', line)
	
	for i in elements:
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
	return columnOperations


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
		result = round(sum(values)/len(values),2)
		res = f'"{columnName}_media": {result}'
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
def processLine(columnOperations: List[str], line: str):
    
	result = []                         # exemplo: result = ["Número": "12334", "Nome": "Cândida", "Curso": "Desporto", "Notas_media": 15.3]
	pos = 0

	components = line.split(",")

    # i : (Column Name, Length if List, Fuction Name)
	for op in columnOperations:

		length = int(calculateLength(str(op[1])))
		list = []

		if length > 0:
			for i in components[pos:(pos+length)]:
				if re.match(r'^-?\d+(?:\.\d+)?$', i):
					list.append(i)
                                
			values = [int(value) for value in list]
			res = executeFunction(op[0],op[2],values)
			result.append(res)
			pos = pos + length
		else:
			result.append(f'"{op[0]}": {components[pos]}')
			pos = pos + 1

	return result

# FUNÇÃO REPOSNSÁVEL POR CRIAR OS DICIONÁRIOS
def geraDicionario(columnOperations, lines):
	
	rule = re.compile(r'(?!"([a-zà-ü]+":))( .*)') # RegEx usada para aceder ao valor de cada coluna
	full_dic = [] # Lista para guardar todos os dicionários gerados
	
	# CRIAÇÃO ITERATIVA DE DICIONÁRIOS
	for line in lines: 
		dicionario = {}
		res = processLine(columnOperations,line)
		for i in range(len(columnOperations)):
			m = re.search(rule,res[i])
			if m:
				dicionario[columnOperations[i][0]] = m.group()[1:]
		full_dic.append(dicionario.copy())
	return full_dic


# FUNÇÃO RESPONSÁVEL POR CONVERTER PARA JSON
def prepareJSON(dicionario, columnOperations):
	res = "[\n" # Incío do ficheiro JSON
	for dic_entry in dicionario:
		res += "\t{\n" # Incío de um dicionário
		for i in range(len(columnOperations)):
			name = columnOperations[i][0]
			if dic_entry[name] == "": # Caso não exista nenhum valor, a chave não é introduzida no dicionário
				break
			elif not "none" in columnOperations[i][2]: # Verifica se existe uma função de agregação
				res += "\t\t\""+ name + "_"+ columnOperations[i][2] +"\": "
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
				# Verifica se a posição atual é a última
				res += "\n"
			else:
				res += ",\n"
		res += "\t},\n" # Fim de um dicionário
	res = res[:-2]
	res += "\n]" # Final do ficheiro JSON
	return res

# ABRIR FICHEIROS
def openFile(opt):
    clear()
    # LEITURA DE INPUT PARA O NOME DO FICHEIRO
    file_name = input("Insert file name to read (extension included): ")
    try:
    # LEITURA DO FICHEIRO
        if opt == 1:
            file = open(os.path.expanduser("../input/"+file_name))
        else:
            file = open(os.path.expanduser("../output/"+file_name))
        lines = file.read().splitlines()
        print("[File opened successfully]")
        file.close()
        return lines
    except FileNotFoundError:
        clear()
        if opt == 1:
            print(f"[ERROR] Invalid file name: cannot locate CSV file \"{file_name}\".\n")
        elif opt == 2:
            print(f"[ERROR] Invalid file name: cannot locate JSON file \"{file_name}\".\n")
        else:
            print(f"[ERROR] Invalid file name: cannot locate file \"{file_name}\".\n")
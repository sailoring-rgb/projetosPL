import re
from typing import List, Tuple
from xmlrpc.client import Boolean

"""
# PARA TESTES RÁPIDOS
h = "Número;Nome;Curso;Notas{5}::a;;;;;Idade;Contas{3};;;"
h1 = "Número,Nome,Curso,Notas{5}::media,,,,,Idade,Contas{3},,,"
h2 = "Número;Nome;Curso;Notas{5},,,,,"
l = "12334;Ana Júlia;Desporto;10,12,11,,"
l1 = "12334,Ana Júlia,Desporto,10,12,11,,"
"""

# FUNÇÃO RESPONSÁVEL POR PROCESSAR O CABEÇALHO DO FICHEIRO CSV
def header(line) -> Tuple[str, List[str]]:

	# columnNames = []                                    # contem o nome das colunas
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
	# print(elements)
	
	for i in elements:
		# columnNames.append(i[0])
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
def executeFunction(columnName:str, function: str, values: List[float]):
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
				for i in elements[pos:(pos+length-1)]:
					if re.match(r'^-?\d+(?:\.\d+)?$', i):
						list.append(i)
						
			values = [float(value) for value in list]

			res = executeFunction(op[0],op[2],values)
			result.append(res)
		else:
			result.append(f'"{op[0]}": {elements[pos]}')

		pos = pos + 1
	# print(result)
	return result


# FUNÇÃO RESPONSÁVEL POR CONVERTER PARA JSON
def convertToJSON(separator: str, columnOperations: List[str], lines: List[str]):

	for line in lines:
		res = processLine(separator,columnOperations,line)
		print(res)
	
	# ...........................................................................


#################################################### MAIN ####################################################


# ABRIR E LER O FICHEIRO
path = input("Insira o path do ficheiro input: ")     # SOLUÇÃO PROVISÓRIO PARA ABRIR O PATH CORRETO
file = open(path)
lines = file.read().splitlines()
file.close()


# PROCESSAR O HEADER -- SE A FUNÇÃO DE AGREGAÇÃO NÃO EXISTIR, É LANÇADA UMA EXCEÇÃO
try:
	separator,columnNames,columnOperations = header(lines[0])
	lines.remove(lines[0])
except NameError:
    print("Unsupported function")


########## fileOUTPUT ......
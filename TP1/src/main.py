import re
import sys
from typing import List, Tuple

h = "Número;Nome;Curso;Notas{5}::media;;;;;Idade;Contas{3};;;"
h1 = "Número,Nome,Curso,Notas{5}::media,,,,,Idade,Contas{3},,,"

def header(line) -> Tuple[List[str],List[Tuple]]:

	columns = []                                        # contem o nome das colunas
	operations = []                                     # contem as funções de agreg. que serão feitas para cada campo se este corresponder a uma lista
	functions = ["sum","media","min","max","count"]     # as funções de agreg. possíveis

	"""	
	elements vai buscar todos os campos do cabeçalho e devolve uma lista de tuplos, em que cada tuplo contém três valores:
		- primeiro: nome da coluna (que se encontra antes de uma vírgula ou de um valor N ou de uma função)
		- segundo: valor de N (pode ser nulo)
		- terceiro: função de agregação (pode ser nulo)
	"""
	elements = re.findall(r'([^;:,{]+)(?:{(.*?)})?(?:\:\:(.*?)(?:;|,))?', line)
	# print(elements)
	
	for i in elements:
		columns.append(i[0])
		if len(list(filter(None,i))) == 1:
			t = (0,"none")
			operations.append(t)
		elif len(list(filter(None,i))) == 2:
			t = (i[1],"none")
			operations.append(t)
		else:
			t = (i[1],i[2])
			operations.append(t)
	# print(operations)
	# print(columns)
	return columns,operations

# header(h)

"""
# o nome das columas do ficheiro
	print(header(h)[0])
# as operações para cada campo se este corresponder a uma lista
	print(header(h)[1])
"""
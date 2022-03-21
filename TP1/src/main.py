import re
from helper import *

#################################################### MAIN ####################################################

# LEITURA DE INPUT PARA O NOME DO FICHEIRO
file_name = input("Inserir nome do ficheiro a converter, com a respetiva extensão: ")

try:
	# LEITURA DO FICHEIRO
	file = open("../input/"+file_name)

except FileNotFoundError as e:
    print(f"Ficheiro inválido: o ficheiro \"{file_name}\" não foi encontrado!")

if file:
	lines = file.read().splitlines()
	file.close()
	output_name = input("Inserir nome do ficheiro destino, com a respetiva extensão: ")
	
	# PROCESSAMENTO INICAL DO INPUT
	lines = clenInput(lines)

	# PROCESSAR O HEADER
	try:
		columnOperations = header(lines[0])
		lines.remove(lines[0])
	except NameError: # SE A FUNÇÃO DE AGREGAÇÃO NÃO EXISTIR, É LANÇADA UMA EXCEÇÃO
		print("Unsupported function")

	# PROCESSAR AS RESTANTES LINHAS DO FICHEIRO
	full_dic = geraDicionario(columnOperations, lines)

	# PREPAR O OUTPUT PARA JSON
	outData = prepareJSON(full_dic,columnOperations)

	# GUARDAR O OUTPUT
	outputFile = open("../output/"+output_name,"w")
	outputFile.write(outData)
	outputFile.close
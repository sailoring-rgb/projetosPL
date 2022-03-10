import re
import sys

header = "Número,Nome,Curso,Notas{5}::avg,,,,,Idade"

columns = []
list_or_not = []
functions = ["sum","media","min","max","count"]

# elements vai buscar todos os campos do cabeçalho e devolve uma lista de tuplos, em que cada tuplo contém três valores:
# primeiro: nome da coluna (que se encontra antes de uma vírgula ou de um valor N ou de uma função)
# segundo: valor de N (pode ser nulo)
# terceiro: função de agregação (pode ser nulo)
elements = re.findall(r'([^:{},]+)(?:{(.*)})?(?:\:\:(.*?)(?:,))?', header)
print(elements)

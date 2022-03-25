from helper import *

# CONVERTER UM FICHEIRO
def convertFile():
    lines = openFile(1)
    if lines:
        output_name = input("Inserir nome do ficheiro destino, com a respetiva extensão: ")
        
        # PROCESSAMENTO INICAL DO INPUT
        lines = cleanInput(lines)

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
        outputFile = open("../output/"+output_name,'w')
        outputFile.write(outData)
        outputFile.close

# VISUALIZAÇÃO DE FICHEIROS
def viewFile():
    clear()
    run = True
    while(run):
        print("\n\n\t* Select file extension *\n")
        print_menu(menu_file)
        opt = input("\nSelect option: ")
        print()
        if (str(opt) == '1' or str(opt) == '2'):
            lines = openFile(int(opt))
            if lines:
                print()
                for l in lines:
                    print(l)
        elif str(opt) == '0':
            run = False
        else:
            pass

# EXECUTAR O MENU
def runMenu():
    run = True
    while(run):
        clear()
        print("\n\n\t**** CSV TO JSON CONVERTER ****\n")
        print_menu(menu_initial)
        option = input('\nEnter your choice: ')
        print()
        if str(option) == '1':
            convertFile()
        elif str(option) == '2':
            viewFile()
        elif str(option) == '0':
            run = False
            print("\n\n\t**** LEAVING ****\n")
        else:
            pass

#################################################### MAIN ####################################################
runMenu()
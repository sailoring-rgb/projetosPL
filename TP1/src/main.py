from helper import *

# CONVERTER UM FICHEIRO
def convertFile():
    lines = openFile(1)
    if lines == - 1:
        return -1
    if lines:
        output_name = input("[JSON] Insert file name (extension included): ")
        
        # PROCESSAMENTO INICAL DO INPUT
        lines = cleanInput(lines)

        # PROCESSAR O HEADER
        try:
            columnOperations = header(lines[0])
            lines.remove(lines[0])
        except NameError: # SE A FUNÇÃO DE AGREGAÇÃO NÃO EXISTIR, É LANÇADA UMA EXCEÇÃO
            print("[ERROR] Unsupported function on CSV file.")
            input("[PRESS ENTER TO CONTINUE]")
            clear()
            return -2

        # PROCESSAR AS RESTANTES LINHAS DO FICHEIRO
        full_dic = geraDicionario(columnOperations, lines)

        # PREPAR O OUTPUT PARA JSON
        outData = prepareJSON(full_dic)

        # GUARDAR O OUTPUT
        outputFile = open("../output/"+output_name,'w')
        outputFile.write(outData)
        outputFile.close
        print("[FILE] Converted successfully.")
        input("[PRESS ENTER TO CONTINUE]")
        clear()
        return 0

# VISUALIZAÇÃO DE FICHEIROS
def viewFile():
    clear()
    run = True
    while(run):
        print("\n\n\t* Select file extension *\n")
        print_menu(menu_file)
        opt = input("\n> Option: ")
        if (str(opt) == '1' or str(opt) == '2'):
            lines = openFile(int(opt))
            if lines == - 1: # CHECKING FOR FILE NOT FOUND
                pass
            elif lines:
                clear()
                for l in lines:
                    print(l)
                input("[PRESS ENTER TO CONTINUE]")
                clear()
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
        option = input('\n> Option: ')
        print()
        if str(option) == '1':
            val = convertFile()
            if val == - 2: # CHECKING FOR ERRORS ON FUNCTIONS
                pass
        elif str(option) == '2':
            viewFile()
        elif str(option) == '0':
            run = False
            clear()
            print("\n\n\t**** LEAVING ****\n")
        else:
            pass


#################################################### MAIN ####################################################

runMenu()
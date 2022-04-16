from helper import *

def open_file():
    file_name = input("[CSV] Insert file name (extension included): ")
    try:	
        file = open("../input/"+file_name)
    except OSError:
        print(f"[ERROR] Can't locate CSV file \"{file_name}\".\n")
        input("[PRESS ENTER TO CONTINUE]")
        return -1

    if file:
        lines = file.read().splitlines()
        print("[FILE] Opened successfully.")
        input("[PRESS ENTER TO CONTINUE]")
        file.close()
        return lines

lines = open_file()
lines_for_LEX, lines_for_YACC = lex_or_yacc(lines)


print("-------------------------------------FOR LEX---------------------------------------------")
for line in lines_for_LEX:
    print(line)
print("-------------------------------------FOR YACC---------------------------------------------")
for line in lines_for_YACC:
    print(line)

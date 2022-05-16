def open_file(input_name:str):
    file = open("../input/"+input_name)
    
    if not file:
        raise FileNotFoundError

    lines = file.read().splitlines()
    file.close()
    print("\033[96m[" + input_name[:-4] + "]\033[0m\033[92m opened successfully.\033[0m")
    return lines
import json
from random import sample
from time import sleep
from math import pow
from tkinter import filedialog as fd

global Keyword_key, keyword_list, Variable_list, Variable_dict, Def_function_list, Def_function_dict, temp_val, i, config_file


def config_stuff() -> None:
    global Keyword_key, keyword_list, Variable_list, Variable_dict, Def_function_list, Def_function_dict, temp_val, i, config_file
    Keyword_key = ["(", ")", "{", "}", ":", ";", ",", ".", " ", "'", "\"", "\n", "#", "=", "True", "False", # symbols
                   "print", "exit", "let:", "input", "type", "int", "string", "boolean", "none",# variable stuf / other stuf
                   "define", "->", # function stuf
                   "if", "while", "fornumb", "isequal", "isgreater", "islesser", # loops and logic stuf
                   "join", "remove", "substring", "shuffle", "slice", # string stuf
                   "not", "and", "or", "xor", # boolean stuf
                   "add", "subtr", "multi", "divi", "pow", "mod", # arethmetic stuf
                   "sleep"] # python modules
    keyword_list = []
    
    Variable_list = []
    Variable_dict = {}
    
    Def_function_list = []
    Def_function_dict = {}
    
    temp_val = ""
    i = -1
    
    try:
        config_f = open("config.json", "r")
        config_file = config_f.read()
        config_f.close()
    except FileNotFoundError:
        print("""Config file not found.
Please create a file named "config.json" in the "Ether interpreter" directory.
{"Debug":0, "File_picker":1, "Default_file":"Test_program.etr", "Announce_comments":0, "Error_length":10}
should be inside the file.
Using a default config file.""")
        config_file = '{"Debug":0, "File_picker":1, "Default_file":"Test_program.etr", "Announce_comments":0, "Error_length":10}'

    config_file = json.loads(config_file)
    if config_file["Debug"] == 1:
        print(f"--- Config file contents: ---\n{config_file}")


def file_setup() -> None:
    global file
    if config_file["File_picker"] == 1:
        path: str = fd.askopenfilename()
        if not(path.endswith(".etr")):
            print("File needs to have \".etr\" extension.")
            exit(1)
    else:
        # path = "Program.spp"
        path = config_file["Default_file"]

    try:
        file_details = open(path, "r")
    except FileNotFoundError:
        if config_file["File_picker"] != 1:
            print(f"""\"{config_file['Auto_picker_file']}\" File not found in the Ether interpreter directory.
Please check \"Config.json\" to make sure the \"Auto_picker_file\" value is correct.
If you want to choose the file when running, set \"File_picker\" equal to 1.""")
            exit(1)
        print("File not found")
        exit(1)

    file = file_details.read()
    file_details.close()
    if config_file["Debug"] == 1:
        print(f"---Program file contents: ---\n{file}")
        print(f"---File is {len(file)} character(s) long---")


def keyword_parser(f: str) -> list:
    global temp_val, i, keyword_list, file
    file = f
    i = -1
    temp_val = ""
    keyword_list = []
    while True:
        i += 1
        temp_val += file[i]

        # Let: var = "value";
        if temp_val == "let:":
            keyword_list.append(temp_val)
            temp_val = ""
            if file[i + 1] == " ":
                keyword_list.append(" ")
                i += 1
            i += 1
            temp_val += file[i]
            while temp_val.join(file[i+1]).isidentifier():
                i += 1
                temp_val += file[i]
            keyword_list.append(temp_val)
            Variable_list.append(temp_val)
            temp_val = ""
            i += 1
            temp_val += file[i]
            temp_val = ""

            i += 1
            temp_val += file[i]
            if temp_val == "=":
                keyword_list.append(temp_val)
                temp_val = ""
            else:
                print(f"ERROR: Expected \"=\" at character {i}")
                exit(f"Expected \"=\" at character {i}")

            if file[i + 1] == " ":
                keyword_list.append(" ")
                i += 1
            if file[i + 1] == "=":
                keyword_list.append("=")
                i += 1

        # Defining functions
        if temp_val == "define":
            keyword_list.append(temp_val)
            temp_val = ""

            if file[i + 1] == " ":
                keyword_list.append(" ")
                i += 1
            
            while temp_val.join(file[i+1]).isidentifier():
                i += 1
                temp_val += file[i]

            keyword_list.append(temp_val)
            Def_function_list.append(temp_val)
            temp_val = ""

        # Comments
        if temp_val == "#":
            # Since python automatically skips every other check in an or statement when the first one is true,
            # putting the end of file check first removes the risk of index errors when parsing for keywords.
            while not (i+1 >= len(file)
                       or file[i+1] == "\n"
                       or file[i+1] == "#"):
                i += 1
                temp_val += file[i]
            keyword_list.append(temp_val)
            temp_val = ""

        # Numbers
        if temp_val.isnumeric():
            while file[i + 1].isnumeric():
                i += 1
                temp_val += file[i]
            keyword_list.append(temp_val)
            temp_val = ""

        # Strings
        if temp_val == '"' or temp_val == "'":
            quote_style = temp_val
            keyword_list.append(temp_val)
            temp_val = ""
            while not (file[i + 1] == quote_style):
                i += 1
                temp_val += file[i]
            keyword_list.append(temp_val)
            i += 1
            keyword_list.append(quote_style)
            temp_val = ""

        # Keywords
        if temp_val in Keyword_key:
            keyword_list.append(temp_val)
            temp_val = ""

        # Variables
        if temp_val in Variable_list:
            if not (file[i + 1].isalnum()):
                keyword_list.append(temp_val)
                temp_val = ""

        # Functions
        if temp_val in Def_function_list:
            if not (file[i + 1].isalnum()):
                keyword_list.append(temp_val)
                temp_val = ""

        # End of file check
        if len(file) <= i + 1:
            if temp_val != "":
                print(f'---Mistyped kword(s), expect errors.---\n{temp_val}\n')
            else:
                if config_file["Debug"] == 1:
                    print("---No errors while compiling---")
            return keyword_list


###############################################################


class Var:

    def __init__(self, name, value, v_type) -> None:
        self.Var_name = name
        self.Var_value = value
        self.Var_type = v_type

    def get_value(self) -> object:
        return self.Var_value

    def get_type(self) -> str:
        return self.Var_type


def check_for_kword(value: str) -> None:
    global index
    
    index += 1
    if Keyword_list[index] == value:
        return
    else:
        print(f"Error: Expected '{value}' at keyword {index} but found \"{Keyword_list[index]}\"")
        Err_len = config_file["Error_length"]
        Error_keywords = "".join(Keyword_list[index-Err_len:index-1])
        print(f"Behind the error: {Error_keywords}")
        exit(1)


def skip_kword_if_present(value: str) -> bool:
    global index
    if Keyword_list[index+1] == value:
        index += 1
        return True
    else:
        return False


def value_parser(string: bool = False,
                 integer: bool = False,
                 boolean: bool = False) -> tuple[str, str]:
    '''
    The return tuple is formatted like this:
    (Value, Type)
    '''
    global index
    index += 1
    if keyword_list[index] in Variable_list:
        var_val = Variable_dict.get(keyword_list[index])
        if (var_val[1] == "Integer") & integer:
            return var_val
        elif (var_val[1] == "String") & string:
            return var_val
        elif (var_val[1] == "Boolean") & boolean:
            return var_val
    elif Keyword_list[index].isnumeric() & integer:
        return (Keyword_list[index], "Integer")
    
    elif (Keyword_list[index] == "'" or Keyword_list[index] == "\"") & string:
        index += 2
        return (Keyword_list[index - 1], "String")
    
    elif (Keyword_list[index] == "False" or Keyword_list[index] == "True") & boolean:
        return (Keyword_list[index], "Boolean")
    
    function_ret = function_parser()
    if function_ret is not None:
        if type(function_ret) == tuple:
            return function_ret
        if function_ret.isnumeric() & integer:
            return (function_ret, "Integer")
        elif (function_ret == "True" or function_ret == "False") & boolean:
            return (function_ret, "Boolean")
        elif string:
            return (str(function_ret), "String")
    if string:
        params = "string, "
    if integer:
        params = params + "int, "
    if boolean:
        params = params + "bool, "
    if params == "":
        params = params + "none"
    print(f"Error: Expected {params}at index {index}, but instead found {keyword_list[index]}")
    Err_len = config_file["Error_length"]
    Error_keywords = "".join(Keyword_list[index-Err_len:index-1])
    print(f"Behind the error: {Error_keywords}")
    exit(1)


def variable_stuff() -> None:
    global index
    var_name = keyword_list[index]
    index += 1

    if keyword_list[index+1] == "=":
        index += 1
        variable_reassignment(var_name)
    elif keyword_list[index] == "=":
        variable_reassignment(var_name)


def variable_reassignment(var_name) -> None:
    global index
    
    index += 1
    skip_kword_if_present(" ")
    value_1 = value_parser(string=True, integer=True, boolean=True)
    check_for_kword(";")
    
    Variable_dict[var_name] = value_1


def function_stuff() -> object:
    ...


def function_define_func() -> None:
    global index    

    check_for_kword(" ")
    index += 1
    func_name = keyword_list[index]
    check_for_kword("(")
    check_for_kword(")")
    
    if skip_kword_if_present(" ") and skip_kword_if_present("->"):
        skip_kword_if_present(" ")
        index += 1
        return_type = keyword_list[index]
    else:
        return_type = "None"
    
    check_for_kword(":")
    skip_kword_if_present(" ")
    check_for_kword("{")

    func_index = index
    Def_function_dict[func_name] = (func_index, return_type)

    while keyword_list[index] != "}":
        index += 1

def function_int() -> tuple[str, str]:
    check_for_kword("(")
    value, val_type = value_parser(string=True, integer=True, boolean=True)
    check_for_kword(")")
    
    if val_type == "Boolean":
        if value == "True":
            return ("1", "Integer")
        else:
            return ("0", "Integer")
    elif val_type == "String":
        if value.isnumeric():
            return (value[0], "Integer")
        else:
            raise ValueError
    elif val_type == "Integer":
        return (value, "Integer")


def function_string() -> tuple[str, str]:
    check_for_kword("(")
    value = value_parser(string=True, integer=True, boolean=True)[0]
    check_for_kword(")")
    
    return (value, "String")


def function_boolean() -> tuple[str, str]:
    check_for_kword("(")
    value, val_type = value_parser(string=True, integer=True, boolean=True)
    check_for_kword(")")
    
    if val_type == "Boolean":
        return (value, "Boolean")
    elif val_type == "Integer":
        if int(value) == 0:
            return ("False", "Boolean")
        else:
            return ("True", "Boolean")
    elif val_type == "String":
        if value != "":
            return ("True", "Boolean")
        else:
            return ("False", "Boolean")

def function_print() -> None:
    check_for_kword("(")
    value_1 = value_parser(string=True, integer=True, boolean=True)[0]
    check_for_kword(")")
    
    print(value_1)


def exit_program() -> None:
    check_for_kword("(")
    exit_code = value_parser(string=True, integer=True, boolean=False)[0]
    check_for_kword(")")
    
    print(f"---Program exited at index {index}, with exit code \"{exit_code}\"---")
    exit(exit_code)


def function_join() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=True, integer=True, boolean=True)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=True, integer=True, boolean=True)[0]
    check_for_kword(")")
    
    return str(value_1) + str(value_2)


def functions_remove() -> str:
    global index
    if keyword_list[index + 1] == ".":
        index += 1
        if keyword_list[index + 1] == "substring":
            index += 1
            return function_remove_substring()


def function_remove_substring() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=True, integer=False, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    substring = value_parser(string=True, integer=False, boolean=False)[0]
    check_for_kword(")")
    
    return value_1.replace(substring, "")


def function_shuffle() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=True, integer=True, boolean=True)[0]
    check_for_kword(")")
    
    return "".join(sample(value_1, len(value_1)))


def function_slice() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=True, integer=False, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    start = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    end = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    step = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(")")
    
    return value_1[int(start):int(end):int(step)]


def function_add() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(")")
    
    return str(int(value_1) + int(value_2))


def function_subtr() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(")")
    
    return str(int(value_1) - int(value_2))


def function_multi() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(")")
    return str(int(value_1) * int(value_2))


def function_divi() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(")")
    
    return str(int(value_1) // int(value_2))


def function_pow() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(")")

    # Int is used before string conversion because it rounds the value.
    return str(int(pow(int(value_1), int(value_2))))


def function_mod() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(")")
    
    return str(int(value_1) % int(value_2))


def function_if() -> None:
    global Keyword_list, index
    
    check_for_kword("(")
    value_1 = value_parser(string=False, integer=False, boolean=True)[0]
    check_for_kword(")")
    check_for_kword(":")
    skip_kword_if_present(" ")
    if value_1 == "True":
        check_for_kword("{")
        while Keyword_list[index] != "}":
            index += 1
            function_parser()
    else:
        while Keyword_list[index] != "}":
            index += 1
    

def function_while() -> None:
    global Keyword_list, index
    
    check_for_kword("(")
    condition_index = int(index)
    condition = value_parser(string=False, integer=False, boolean=True)[0]
    check_for_kword(")")
    check_for_kword(":")
    skip_kword_if_present(" ")
    if condition == "True":
        check_for_kword("{")
        while True:
            while Keyword_list[index] != "}":
                index += 1
                function_parser()
            index = int(condition_index)
            condition = value_parser(string=False, integer=False, boolean=True)[0]
            if condition == "True":
                pass
            else:
                break

    else:
        while Keyword_list[index] != "}":
            index += 1


def function_fornumb() -> None:
    global Keyword_list, index, Variable_list
    
    check_for_kword("(")
    iteration_amount: int = int(value_parser(string=False, integer=True, boolean=False)[0])
    check_for_kword(",")
    skip_kword_if_present(" ")
    var_name: str = value_parser(string=True, integer=False, boolean=False)[0]
    check_for_kword(")")
    check_for_kword(":")
    skip_kword_if_present(" ")
    
    Variable_dict[var_name] = ("0", "Integer")
    
    current_iterations = 0
    loop_index: int = index
    check_for_kword("{")
    while True:
        while Keyword_list[index] != "}":
            index += 1
            function_parser()

        current_iterations += 1
        Variable_dict[var_name] = (str(current_iterations), "Integer")
        if iteration_amount <= current_iterations:
            break   
        index = loop_index


def function_isequal() -> tuple[str, str]:
    check_for_kword("(")
    value_1 = value_parser(string=True, integer=True, boolean=True)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=True, integer=True, boolean=True)[0]
    check_for_kword(")")
    
    return "True" if value_1 == value_2 else "False"


def function_isgreater() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=True, integer=True, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=True, integer=True, boolean=False)[0]
    check_for_kword(")")
    
    try:
        return "True" if int(value_1) > int(value_2) else "False"
    except ValueError:
        return "True" if value_1 > value_2 else "False"


def function_islesser() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=True, integer=True, boolean=False)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=True, integer=True, boolean=False)[0]
    check_for_kword(")")
    
    try:
        return "True" if int(value_1) < int(value_2) else "False"
    except ValueError:
        return "True" if value_1 < value_2 else "False"
    

def function_sleep() -> None:
    check_for_kword("(")
    value = value_parser(string=False, integer=True, boolean=False)[0]
    check_for_kword(")")
    
    sleep(int(value))


def function_not() -> str:
    check_for_kword("(")
    value = value_parser(string=False, integer=False, boolean=True)[0]
    check_for_kword(")")
    
    if value == "True":
        return "False"
    elif value == "False":
        return "True"


def function_and() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=False, integer=False, boolean=True)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=False, integer=False, boolean=True)[0]
    check_for_kword(")")
    if value_1 == "True":
        if value_2 == "True":
            return "True"
        else:
            return "False"
    else:
        return "False"


def function_or() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=False, integer=False, boolean=True)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=False, integer=False, boolean=True)[0]
    check_for_kword(")")
    
    if value_1 == "True" or value_2 == "True":
        return "True"
    else:
        return "False"


def function_xor() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=False, integer=False, boolean=True)[0]
    check_for_kword(",")
    skip_kword_if_present(" ")
    value_2 = value_parser(string=False, integer=False, boolean=True)[0]
    check_for_kword(")")

    # XOR function i took from the first result on google
    if ((value_1 == "True") and (value_2 == "False")) or ((value_1 == "False") and (value_2 == "True")):
        return "True"
    else:
        return "False"
    

def function_input() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=True, integer=True, boolean=True)[0]
    check_for_kword(")")
    return input(value_1)


def function_type() -> str:
    check_for_kword("(")
    val_type = value_parser(string=True, integer=True, boolean=True)[1]
    check_for_kword(")")
    return val_type


def function_let() -> None:
    global index, Variable_dict
    skip_kword_if_present(" ")
    index += 1
    if Keyword_list[index] in Variable_list:
        var_name = Keyword_list[index]
    else:
        print(f"Error: Expected a variable name at keyword {index}")
        exit(1)
    skip_kword_if_present(" ")
    check_for_kword("=")
    skip_kword_if_present(" ")
    value_1 = value_parser(string=True, integer=True, boolean=True)
    check_for_kword(";")
    Variable_dict[var_name] = value_1


def function_parser() -> object:
    global Def_function_list
    
    """
    If a function doesn't have return in front of it, it simply doesnt have a return value.
    """
    
    function_dict = {
    # Variable functions
    "let:": function_let,
    "type": function_type,
    "input": function_input,
    "int": function_int,
    "string": function_string,
    "boolean": function_boolean,

    # User defined functions
    "define": function_define_func,
    
    # Comparison functions
    "isequal": function_isequal,
    "isgreater": function_isgreater,
    "islesser": function_islesser,
    "if": function_if,

    # Loop functions
    "while": function_while,
    "fornumb": function_fornumb,
    
    # Boolean functions
    "not": function_not,
    "and": function_and,
    "or": function_or,
    "xor": function_xor,

    # String functions
    "join": function_join,
    "remove": functions_remove,
    "shuffle": function_shuffle,
    "slice": function_slice,

    # arithmetic functions
    "add": function_add,
    "subtr": function_subtr,
    "multi": function_multi,
    "divi": function_divi,
    "mod": function_mod,
    "pow": function_pow,
    
    # python module stuf
    "sleep": function_sleep,

    #other funcs
    "print": function_print,
    "exit": exit_program
    }
    
    keyword = keyword_list[index]
    
    # Variable functions
    if keyword in Variable_list:
        variable_stuff()
    elif keyword in Def_function_list:
        return function_stuff()
    elif keyword in function_dict:
        return function_dict[keyword]()


def run_program() -> None:
    global Keyword_list, index
    index = -1
    while True:
        index += 1
        if index >= len(Keyword_list):
            print("---Exited program naturally---")
            exit()
        if Keyword_list[index][0] == "#":
            if config_file["Announce_comments"] == 1:
                print(f"- Passed over comment: {Keyword_list[index]}")
            continue
        function_parser()


def main() -> None:
    global Keyword_list

    config_stuff()
    file_setup()
    Keyword_list = keyword_parser(file)
    if config_file["Debug"] == 1:
        # print("testing for classes in the future")
        # a = [Var("the", 123, "integer")]
        # print(f"{a[0].get_value() = }, {a[0].get_type() = }")
        print(f"---Keyword list: ---\n{Keyword_list}")
    print("---Running program---")
    run_program()


if __name__ == "__main__":
    main()

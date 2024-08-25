import json
import random
from tkinter import filedialog as fd

global Keyword_key, keyword_list, Variable_list, Variable_dict, temp_val, i, config_file


def config_stuff() -> None:
    global Keyword_key, keyword_list, Variable_list, Variable_dict, temp_val, i, config_file
    Keyword_key = ["(", ")", ";", ",", ".", " ", "'", "\"", "\n", "#", "=", "True", "False",
                   "print", "exit", "let:", "input", "type", "isequal", "isgreater", "islesser",
                   "join", "remove", "substring", "shuffle", "slice", "not", "and", "or"]
    keyword_list = []
    Variable_list = []
    Variable_dict = {}
    temp_val = ""
    i = -1
    
    try:
        config_f = open("config.json", "r")
    except FileNotFoundError:
        print("""Config file not found.
Please create a file named \"config.json\", and put it in the \"Ether interpreter\" directory.
{"Debug":1, "File_picker":0, "Default_file":"Program.spp", "Announce_comments":1}
should be inside the file.""")
        exit(1)

    config_file = config_f.read()
    config_f.close()
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

        if temp_val == "#":
            # Since python automatically skips every other check in an or statement when the first one is true,
            # putting the end of file check first removes the risk of index errors when parsing for keywords.
            while not (i+1 >= len(file) or file[i+1] == "\n" or file[i+1] == "#"):
                i += 1
                temp_val += file[i]
            keyword_list.append(temp_val)
            temp_val = ""

        if temp_val.isnumeric():
            while file[i + 1].isnumeric():
                i += 1
                temp_val += file[i]
            keyword_list.append(temp_val)
            temp_val = ""

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

        if temp_val in Keyword_key:
            keyword_list.append(temp_val)
            temp_val = ""

        if temp_val in Variable_list:
            if not (file[i + 1].isalnum()):
                keyword_list.append(temp_val)
                temp_val = ""

        if len(file) <= i + 1:
            if temp_val != "":
                print(f'---Mistyped kword(s), expect errors.---\n(\n{temp_val}\n)')
            else:
                if config_file["Debug"] == 1:
                    print("---No errors while compiling---")
            return keyword_list


##################################


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


def skip_kword_if_present(value: str) -> None:
    global index
    if Keyword_list[index+1] == value:
        index += 1
        return


def value_parser(string: bool = False,
                 integer: bool = False,
                 boolean: bool = False) -> tuple:
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
    return "".join(random.sample(value_1, len(value_1)))


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


def function_isequal() -> str:
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


def function_not() -> str:
    check_for_kword("(")
    value_1 = value_parser(string=False, integer=False, boolean=True)[0]
    check_for_kword(")")
    if value_1 == "True":
        return "False"
    elif value_1 == "False":
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
    """
    If a function doesn't have return in front of it, it simply doesnt have a return value.
    """
    
    # Variable functions
    if Keyword_list[index] in Variable_list:
        variable_stuff()
    elif Keyword_list[index] == "let:":
        function_let()
    elif keyword_list[index] == "type":
        return function_type()
    elif keyword_list[index] == "input":
        return function_input()
    
    # Comparison functions
    elif Keyword_list[index] == "isequal":
        return function_isequal()
    elif Keyword_list[index] == "isgreater":
        return function_isgreater()
    elif Keyword_list[index] == "islesser":
        return function_islesser()
    
    # Boolean functions
    elif Keyword_list[index] == "not":
        return function_not()
    elif Keyword_list[index] == "and":
        return function_and()
    elif Keyword_list[index] == "or":
        return function_or()
    
    # String functions
    elif Keyword_list[index] == "join":
        return function_join()
    elif Keyword_list[index] == "remove":
        return functions_remove()
    elif Keyword_list[index] == "shuffle":
        return function_shuffle()
    elif keyword_list[index] == "slice":
        return function_slice()

    # Other functions
    elif Keyword_list[index] == "print":
        function_print()
    elif Keyword_list[index] == "exit":
        exit_program()


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

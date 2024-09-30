from json import loads
from random import sample, randint
from math import pow, sqrt
from tkinter import filedialog as fd
from sys import setrecursionlimit
from datetime import datetime
import time


def config_stuff() -> None:
  """Sets up configuration file and global variables"""
  global Keyword_key, keyword_list, Variable_list, Variable_dict, Def_function_list, Def_function_dict, temp_val, i, config_file, loop_break, _timer
  
  setrecursionlimit(100_000) # Set the recursion limit to 100k; so recursion is easier to make without throwing an error
  
  Keyword_key = ["(", ")", "{", "}", ":", ";", ",", ".", " ", "'", "\"", "\n", "#", "=", "++", "--", "True", "False", # symbols
                "println", "exit", "throw", "let:", "input", "type", "integer", "string", "boolean", "none", "len", # variable stuf / other stuf
                "define", "->", "return", "args", # function stuf
                "if", "while", "fornumb", "break", "isequal", "isgreater", "islesser", # loops and logic stuf
                "join", "remove", "substring", "shuffle", "slice", "getchar", "repchar", # string stuf
                "not", "and", "or", "xor", # boolean stuf
                "add", "subtr", "multi", "divi", "pow", "mod", "sqrt", # arethmetic stuf
                "sleep", "msleep", "datetime", "timer", "start", "restart", "get", "stop", "randint"] # python stuff
  keyword_list = []
  
  Variable_list = []
  Variable_dict = {}
  
  Def_function_list = []
  Def_function_dict = {}
  
  temp_val = ""
  i = -1
  
  loop_break = False
  _timer = Timer()
  
  try:
    with open("config.json", "r") as config_f:
      config_file = config_f.read()
  except FileNotFoundError:
    print("""Config file not found.
Please create a file named "config.json" in the "Ether interpreter" directory.
{"Debug":0, "File_picker":1, "Default_file":"Test_program.etr", "Announce_comments":0, "Error_length":10}
should be inside the file.
Using a default config file.""")
    config_file = '{"Debug":0, "File_picker":1, "Default_file":"Test_program.etr", "Announce_comments":0, "Error_length":10}'
  
  config_file = loads(config_file) # Turns json file into python dictionary
  if config_file["Debug"] == 1:
    print(f"--- Config file contents: ---\n{config_file}")


def file_setup() -> None:
  """Loads the file into the interpreter"""
  global file
  if config_file["File_picker"] == 1:
    path: str = fd.askopenfilename()
  else:
    # path = "Program.spp"
    path = config_file["Default_file"]
  
  if not(path.endswith(".etr")):
    print("File needs to have \".etr\" extension.")
    exit(1)
  
  try:
    with open(path, "r") as file_details:
      file = file_details.read()
  except FileNotFoundError:
    if config_file["File_picker"] != 1:
      print(f"""\"{config_file['Auto_picker_file']}\" File not found in the Ether interpreter directory.
Please check \"Config.json\" to make sure the \"Auto_picker_file\" value is correct.
If you want to choose the file when running, set \"File_picker\" equal to 1.""")
      exit(1)
    
    print("File not found")
    exit(1)
  
  
  if config_file["Debug"] == 1:
    print(f"---Program file contents: ---\n{file}")
    print(f"---File is {len(file)} character(s) long---")


def parser_let() -> None:
  global temp_val, i, keyword_list, file

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
      print(f"ERROR: Expected \"=\" at character {i} (file up to {file[:i]})")
      exit(f"Expected \"=\" at character {i}")

    if file[i + 1] == " ":
      keyword_list.append(" ")
      i += 1
    if file[i + 1] == "=":
      keyword_list.append("=")
      i += 1

def keyword_parser() -> list[str]:
  """Parses the input file for keywords, returning a list of keywords."""
  global temp_val, i, keyword_list, file
  i = -1
  temp_val = ""
  keyword_list = []
  if config_file["Debug"] == 1:
    parser_timer = Timer()
    parser_timer.start()
  while True:
    i += 1
    temp_val += file[i]

    # Let: var = "value";
    parser_let()

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
          parser_timer.stop()
          print(f"Time to parse: {parser_timer.get_time()} seconds")
      return keyword_list


###############################################################


class KeywordExpectedError(Exception): 
  """The error that gets thrown when a keyword is expected in Keyword_list."""
  ...


class UserDefinedError(Exception):
  """The error that gets thrown when throw() is used, with the input value as the error code."""
  ...


class UnexpectedType(Exception):
  """The error that gets thrown when a specific type of value is expected in a function"""
  ...


class Timer:
  def __init__(self):
    self.start_time = None
    self.is_running = False
  
  def start(self):
    if not self.is_running:
      self.start_time = time.time()
      self.is_running = True
  
  def restart(self):
    self.start()
  
  def get_time(self): # If the timer is stopped, it will return the value when stopped
    return time.time() - self.start_time
  
  def stop(self): # Stops the timer
    self.is_running = False


def check_for_kword(value: str) -> None:
  """Checks for [value] being equal to the next keyword. If a value is not found, an error is thrown."""
  
  increment_top_of_stack()
  # print(Keyword_list[top_from_stack()])
  if Keyword_list[top_from_stack()] == value:
    return
  else:
    Err_len = config_file["Error_length"]
    Error_keywords = "".join(Keyword_list[top_from_stack()-Err_len:top_from_stack()-1])
    print(f"Behind the error: {Error_keywords}")
    raise KeywordExpectedError(f"Expected '{value}' at line {get_current_line(top_from_stack())} but found \"{Keyword_list[top_from_stack()]}\"")


def skip_kword_if_present(value: str) -> bool:
  """If {value} is the next keyword, increment the stack by one.
  
  returns:
    True if {value} is found in Keyword_list, else returns False."""
  
  if Keyword_list[top_from_stack()+1] == value:
    increment_top_of_stack()
    return True
  else:
    return False


def top_from_stack() -> int:
  """
  Replaces "stack[len(stack)-1]", gets the value from the top of the stack.
  """
  
  return stack[len(stack)-1]


def increment_top_of_stack(number: int = 1) -> None:
  """
  Replaces "stack[len(stack)-1] += N", increments the value by [number].
  """
  
  stack[len(stack)-1] += number
  return


def set_top_of_stack(number: int) -> None:
  """
  Replaces "stack[len(stack)-1] = N", sets the value at the top of the stack to [number].
  """
  
  stack[len(stack)-1] = number


def get_current_kword(index: int = None) -> str:
  """Replaces "keyword_list[top_from_stack()]", gets the current keyword."""
  if index is None:
    index = top_from_stack()
  return keyword_list[index]


def get_current_line(index: int) -> int:
  """Used for error messages, gets the line currently being executed."""
  global keyword_list
  
  keywords = keyword_list[:index]
  lines: int = 1 # start at line 1
  for i in keywords:
    if i == "\n":
      lines += 1
  
  return lines

def value_parser(string: bool = False,
                integer: bool = False,
                boolean: bool = False) -> tuple[str, str]:
  """ Parses through keyword_list to find a value of type string, integer, or boolean.
  The return tuple is formatted like this:
  (Value, Type)"""
  global keyword_list
  
  increment_top_of_stack()
  keyword = keyword_list[top_from_stack()]
  
  # Variable parsing
  if keyword in Variable_list:
    var_val = Variable_dict.get(keyword)
    
    if (var_val[1] == "Integer") and integer:
      return var_val
    elif (var_val[1] == "String") and string:
      return var_val
    elif (var_val[1] == "Boolean") and boolean:
      return var_val
  
  # Literal values
  elif keyword.isnumeric() and integer:
    return (keyword, "Integer")
  
  elif (keyword == "'" or keyword == "\"") and string:
    increment_top_of_stack(2)
    return (Keyword_list[top_from_stack() - 1], "String")
  
  elif (keyword == "False" or keyword == "True") and boolean:
    return (keyword, "Boolean")
  
  # Function Parsing
  function_ret = function_parser()
  if function_ret is not None:
    if type(function_ret) == tuple:
      return function_ret
    if function_ret.isnumeric() and integer:
      return (function_ret, "Integer")
    elif (function_ret == "True" or function_ret == "False") and boolean:
      return (function_ret, "Boolean")
    elif string:
      return (str(function_ret), "String")
  
  params = ""
  # Error Handling
  if string:
    params = "string, "
  if integer:
    params = params + "int, "
  if boolean:
    params = params + "bool, "
  if params == "":
    params = params + "none" # not sure if this will ever get used but its nice to have it just in case
  
  print(f"Error: Expected {params}at line {get_current_line(top_from_stack())}, but instead found {keyword}")
  Err_len = config_file["Error_length"]
  Error_keywords = "".join(Keyword_list[top_from_stack()-Err_len:top_from_stack()-1])
  print(f"Behind the error: {Error_keywords}")
  exit(1)


def variable_stuff() -> object:  
  var_name = keyword_list[top_from_stack()]
  increment_top_of_stack()
  
  if keyword_list[top_from_stack()+1] == "=":
    increment_top_of_stack()
    variable_reassignment(var_name)
  elif keyword_list[top_from_stack()] == "=":
    variable_reassignment(var_name)
  
  elif keyword_list[top_from_stack()] == "++":
    if Variable_dict[var_name][1] == "Integer":
      return function_increment(var_name)
    else:
      UnexpectedType(f"The increment function requires an integer.\nError location: {top_from_stack()}")
  elif keyword_list[top_from_stack()] == "--":
    if Variable_dict[var_name][1] == "Integer":
      return function_decrement(var_name)
    else:
      UnexpectedType(f"The decrement function requires an integer.\nError location: {top_from_stack()}")


def variable_reassignment(var_name) -> None:
  increment_top_of_stack()
  skip_kword_if_present(" ")
  value_1 = value_parser(string=True, integer=True, boolean=True)
  # check_for_kword(";")
  
  Variable_dict[var_name] = value_1


def function_decrement(var_name) -> str:
  var = int(Variable_dict[var_name][0]) - 1
  Variable_dict[var_name] = (str(var), "Integer")
  return str(var)


def function_increment(var_name) -> str:
  var = int(Variable_dict[var_name][0]) + 1
  Variable_dict[var_name] = (str(var), "Integer")
  return str(var)

def function_stuff() -> tuple[str, str]:
  func_name = keyword_list[top_from_stack()]
  
  check_for_kword("(")
  if len(Def_function_dict[func_name][2]) > 0:
    input_args = []
    
    for _ in range(len(Def_function_dict[func_name][2])):
      input_args.append(value_parser(string=True, integer=True, boolean=True))
      if keyword_list[top_from_stack()+1] != ")":
        check_for_kword(",")
        skip_kword_if_present(" ")
  
    for arg in range(len(input_args)):
      Variable_dict[Def_function_dict[func_name][2][arg]] = input_args[arg]
  check_for_kword(")")
  
  stack.append(Def_function_dict[func_name][0])
  
  while ((keyword_list[top_from_stack()] != "return") and
        (keyword_list[top_from_stack()] != "}")):
    increment_top_of_stack()
    function_parser()
  
  if Def_function_dict[func_name][1] == "none":
    function_return = ("none", "none")
  else:
    # while keyword_list[top_from_stack()] != "return":
    #   increment_top_of_stack(-1)
    check_for_kword(" ") # what the FUCK
    # okay i found the problem; its with using the fornumb function inside of user defined functions
    # never mind its a problem with all functions with brackets surrounding code
    # I GET IT; its a problem with every bracketed fn because the code thinks the bracket is the ending bracket!!!
    function_return = value_parser(string=True, integer=True, boolean=True)
  func_return_type = function_return[1]
  
  stack.pop()
  if (Def_function_dict[func_name][1] == func_return_type.lower()):
    return function_return 
  else:
    raise UnexpectedType(f"Expected type {Def_function_dict[func_name][1]} to return from {func_name}, but got {func_return_type} instead.")


def function_define_func() -> None:
  
  check_for_kword(" ")
  increment_top_of_stack()
  func_name: str = keyword_list[top_from_stack()]
  # check_for_kword(")")
  # check_for_kword("(")
  
  if func_name in Def_function_dict:
    print(f"Error: Function {func_name} already defined.")
    exit(1)
  
  # TODO: Add support for input values, in the format args("value", "value"...)
  if skip_kword_if_present(" ") and skip_kword_if_present("args"): # Checks for " " and "args"
    check_for_kword("(")
  
    func_arguments: list = []
    while keyword_list[top_from_stack()] != ")":
      func_arguments.append(value_parser(string=True, integer=False, boolean=False)[0])
      if keyword_list[top_from_stack()+1] != ")":
        check_for_kword(",")
        skip_kword_if_present(" ")
      else:
        increment_top_of_stack()
  else:
    increment_top_of_stack(-1)
  
  if skip_kword_if_present(" ") and skip_kword_if_present("->"): # Checks for " " and "->"
    skip_kword_if_present(" ")
    increment_top_of_stack()
    return_type: str = keyword_list[top_from_stack()]
  else:
    return_type: str = "none"
  
  check_for_kword(":")
  skip_kword_if_present(" ")
  check_for_kword("{")
  
  func_index: int = top_from_stack()
  Def_function_dict[func_name] = (func_index, return_type, func_arguments)
  
  while keyword_list[top_from_stack()-1] != "}":
    increment_top_of_stack()


def function_integer() -> tuple[str, str]:
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
      return (value, "Integer")
    else:
      raise ValueError("Expected a numeric value for int function.")
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


def function_len() -> str:
  check_for_kword("(")
  value = value_parser(string=True, integer=True, boolean=False)[0]
  check_for_kword(")")
  
  return str(len(value))


def function_println() -> None:
  check_for_kword("(")
  value_1 = value_parser(string=True, integer=True, boolean=True)[0]
  check_for_kword(")")
  
  print(value_1)


def exit_program() -> None:
  check_for_kword("(")
  exit_code = value_parser(string=True, integer=True, boolean=False)[0]
  check_for_kword(")")
  
  if config_file["Debug"] == 1:
    print(f"---Program exited at index {top_from_stack()}, with exit code \"{exit_code}\"---")
  exit(exit_code)

def function_throw() -> None:
  # throw is a funnier word than raise so thats why i used it
  check_for_kword("(")
  error_code = value_parser(string=True, integer=False, boolean=False)[0]
  check_for_kword(")")
  
  raise UserDefinedError(error_code)

def function_join() -> str:
  check_for_kword("(")
  value_1 = value_parser(string=True, integer=True, boolean=True)[0]
  check_for_kword(",")
  skip_kword_if_present(" ")
  value_2 = value_parser(string=True, integer=True, boolean=True)[0]
  check_for_kword(")")
  
  return str(value_1) + str(value_2)


def functions_remove() -> str:
  if keyword_list[top_from_stack() + 1] == ".":
    increment_top_of_stack()
    if keyword_list[top_from_stack() + 1] == "substring":
      increment_top_of_stack()
      return function_remove_substring()


def function_remove_substring() -> str:
  check_for_kword("(")
  value = value_parser(string=True, integer=False, boolean=False)[0]
  check_for_kword(",")
  skip_kword_if_present(" ")
  substring = value_parser(string=True, integer=False, boolean=False)[0]
  check_for_kword(")")
  
  return value.replace(substring, "")


def function_shuffle() -> str:
  check_for_kword("(")
  value = value_parser(string=True, integer=True, boolean=False)[0]
  check_for_kword(")")
  
  return "".join(sample(value, len(value)))


def function_slice() -> str:
  check_for_kword("(")
  value = value_parser(string=True, integer=False, boolean=False)[0]
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
  
  return value[int(start):int(end):int(step)]


def function_getchar() -> str:
  check_for_kword("(")
  string = value_parser(string=True, integer=False, boolean=False)[0]
  check_for_kword(",")
  skip_kword_if_present(" ")
  index = int(value_parser(string=False, integer=True, boolean=False)[0])
  check_for_kword(")")
  
  return string[index]


def function_repchar() -> str:
  check_for_kword("(")
  string = value_parser(string=True, integer=False, boolean=False)[0]
  check_for_kword(",")
  skip_kword_if_present(" ")
  index = int(value_parser(string=False, integer=True, boolean=False)[0])
  check_for_kword(",")
  skip_kword_if_present(" ")
  replacement = value_parser(string=True, integer=False, boolean=False)[0]
  check_for_kword(")")
  
  return f"{string[:index]}{replacement}{string[index+1:]}"


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
  
  # Int() is used before string conversion because it rounds the value,
  # as pow() returns a floating point value.
  return str(int(pow(int(value_1), int(value_2))))


def function_mod() -> str:
  check_for_kword("(")
  value_1 = value_parser(string=False, integer=True, boolean=False)[0]
  check_for_kword(",")
  skip_kword_if_present(" ")
  value_2 = value_parser(string=False, integer=True, boolean=False)[0]
  check_for_kword(")")
  
  return str(int(value_1) % int(value_2))


def function_sqrt() -> str:
  check_for_kword("(")
  value = value_parser(string=False, integer=True, boolean=False)[0]
  check_for_kword(")")
  
  return str(int(sqrt(int(value))))

def function_if() -> None:
  global Keyword_list, stack
  
  check_for_kword("(")
  value_1 = value_parser(string=False, integer=False, boolean=True)[0]
  check_for_kword(")")
  check_for_kword(":")
  skip_kword_if_present(" ")
  if value_1 == "True":
    check_for_kword("{")
    while Keyword_list[top_from_stack()-1] != "}":
      increment_top_of_stack()
      function_parser()
  else:
    while Keyword_list[top_from_stack()-1] != "}":
      increment_top_of_stack()


def function_break() -> None:
  """Sets the loop_break variable to True, causing loops to end."""
  global loop_break
  loop_break = True


# TODO: make "function_return" function for user defined functions, to make sure that return statements inside of loops/if statements work as intended.


def function_while() -> None:
  global Keyword_list, loop_break
  
  check_for_kword("(")
  condition_index = int(top_from_stack())
  condition = value_parser(string=False, integer=False, boolean=True)[0]
  check_for_kword(")")
  check_for_kword(":")
  skip_kword_if_present(" ")
  if condition == "True":
    check_for_kword("{")
    while True:
      while Keyword_list[top_from_stack()] != "}":
        increment_top_of_stack()
        function_parser()
        if loop_break:
          break
      
      if loop_break:
        loop_break = False
        while Keyword_list[top_from_stack()-2] != "}":
          increment_top_of_stack()
        break
      
      set_top_of_stack(condition_index)
      condition = value_parser(string=False, integer=False, boolean=True)[0]
      
      if condition == "True":
        pass
      else:
        break
  
  else:
    while Keyword_list[top_from_stack()-1] != "}":
      increment_top_of_stack()
  
  while get_current_kword(top_from_stack()-1) != "}":
    increment_top_of_stack() # HOW DID THIS FIX IT????? WHAT THE FUCK??


def function_fornumb() -> None:
  global Keyword_list, Variable_list, loop_break
  
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
  loop_index: int = top_from_stack()
  check_for_kword("{")
  while True:
    while Keyword_list[top_from_stack()] != "}":
      increment_top_of_stack()
      function_parser()
      if loop_break:
        break
    
    if loop_break:
      loop_break = False
      while Keyword_list[top_from_stack()-1] != "}":
        increment_top_of_stack()
      increment_top_of_stack()
      break
    
    current_iterations += 1
    Variable_dict[var_name] = (str(current_iterations), "Integer")
    if iteration_amount <= current_iterations:
      increment_top_of_stack()
      break
    set_top_of_stack(loop_index)



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


def function_sleep() -> None:
  check_for_kword("(")
  value = value_parser(string=False, integer=True, boolean=False)[0]
  check_for_kword(")")
  
  time.sleep(int(value))


def function_msleep() -> None:
  check_for_kword("(")
  value = value_parser(string=False, integer=True, boolean=False)[0]
  check_for_kword(")")
  
  time.sleep(int(value) / 1000)


def function_timer() -> object:
  if skip_kword_if_present("."):
    if skip_kword_if_present("start"):
      function_timerStart()
    elif skip_kword_if_present("restart"):
      function_timerRestart()
    elif skip_kword_if_present("get"):
      return function_timerGet()
    elif skip_kword_if_present("stop"):
      function_timerStop()


def function_timerStart() -> None:
  check_for_kword("(")
  check_for_kword(")")
  
  _timer.start()


def function_timerGet() -> str:
  check_for_kword("(")
  check_for_kword(")")
  
  return str(_timer.get_time())


def function_timerStop() -> None:
  check_for_kword("(")
  check_for_kword(")")
  
  _timer.stop()


def function_timerRestart() -> None:
  check_for_kword("(")
  check_for_kword(")")
  
  _timer.restart()


def function_datetime() -> str:
  check_for_kword("(")
  check_for_kword(")")
  
  return str(datetime.now())


def function_randint() -> tuple[str, str]:
  check_for_kword("(")
  floor = int(value_parser(string=False, integer=True, boolean=False)[0])
  check_for_kword(",")
  skip_kword_if_present(" ")
  ceiling = int(value_parser(string=False, integer=True, boolean=False)[0])
  check_for_kword(")")

  return (randint(floor, ceiling), "Integer")
  

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
  if (((value_1 == "True") and (value_2 == "False")) or
    ((value_1 == "False") and (value_2 == "True"))):
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
  global Variable_dict
  
  skip_kword_if_present(" ")
  increment_top_of_stack()
  if Keyword_list[top_from_stack()] in Variable_list:
    var_name = Keyword_list[top_from_stack()]
  else:
    print(f"Error: Expected a variable name at keyword {top_from_stack()}")
    exit(1)
  skip_kword_if_present(" ")
  check_for_kword("=")
  skip_kword_if_present(" ")
  value_1 = value_parser(string=True, integer=True, boolean=True)
  # check_for_kword(";")
  
  Variable_dict[var_name] = value_1


def function_parser() -> object:
  """The main way that functions are called. If a function returns None, the function has no return value."""
  
  global Def_function_list
  
  function_dict = { # Does this increase the time it takes to run?
  # Variable functions
  "let:": function_let,
  "type": function_type,
  "input": function_input,
  "integer": function_integer,
  "string": function_string,
  "boolean": function_boolean,
  "len": function_len,
  
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
  "break": function_break,
  
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
  "getchar": function_getchar,
  "repchar": function_repchar,
  
  # arithmetic functions
  "add": function_add,
  "subtr": function_subtr,
  "multi": function_multi,
  "divi": function_divi,
  "mod": function_mod,
  "pow": function_pow,
  "sqrt": function_sqrt,
  
  # python module stuf
  "sleep": function_sleep,
  "msleep": function_msleep,
  "datetime": function_datetime,
  "timer": function_timer,
  "randint": function_randint,
  
  #other funcs
  "println": function_println,
  "exit": exit_program,
  "throw": function_throw
  }
  
  keyword = keyword_list[top_from_stack()]
  
  # Variable functions
  if keyword in Variable_list:
    return variable_stuff()
  elif keyword in Def_function_list:
    return function_stuff()
  elif keyword in function_dict:
    return function_dict[keyword]()


def run_program() -> None:
  """The main loop for the interpreter."""
  global Keyword_list, stack
  stack = [-1] # the stack is a list of integers, use stack.append() and stack.pop() to add or remove values from it
  
  while True:
    increment_top_of_stack()
    if top_from_stack() >= len(Keyword_list):
      print("---Exited program naturally---")
      break
    if Keyword_list[top_from_stack()][0] == "#":
      if config_file["Announce_comments"] == 1:
        print(f"- Passed over comment: {Keyword_list[top_from_stack()]}")
      continue
    function_parser()


def main() -> None:
  global Keyword_list
  
  config_stuff()
  file_setup()
  Keyword_list = keyword_parser()
  if config_file["Debug"] == 1:
    # print("testing for classes in the future")
    # a = [Var("the", 123, "integer")]
    # print(f"{a[0].get_value() = }, {a[0].get_type() = }")
    print(f"---Keyword list: ---\n{Keyword_list}")
  print("---Running program---")
  run_program()


if __name__ == "__main__":
  main()

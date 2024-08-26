# Ether Documentation
my own programming language!! :D

(I'm just going to copy & paste my Obsidian docs into this file)



## Common formatting / Notes
* Functions, such as `print(n)`, will have parenthesis around arguments.
* Functions can be nested nearly infinitely.
* Spp is a zero-indexed language.
* Files in the Ether format will be denoted with the file ending ".etr".
* The Config.json file is necessary for the interpreter to function.
* Line breaks, spaces, and tabs are not neccessary for the program to run.

## Config.json
### "Debug"
* Enables multiple functionalities meant for debugging purposes.
* If the value of "Debug" is set to 1, the interpreter does the following:
	* Prints the whole Config.json file to the console upon loading it.
	* Prints the program file's contents to the console upon loading.
	* Prints the length of the file to the console.
	* Denotes when no errors occurred while parsing the file.
	* Shows the list of keywords after the file has been parsed.
### "File_picker"
* Enables or disables the file picker that appears when running Interpreter.py
* If the value is set to 0, Interpreter.py uses the file stored in "Default_file"
### "Default_file"
* Stores the path for the program file that Interpreter.py uses when "File_picker" is set to 0.
### "Announce_comments"
* Announces comments in the console when passing over them.
### "Error_length"
* Determines how many previous keywords are displayed when an error message is displayed.

## # Comments
* Starts with a hashtag.
* Can end with either a new line or another hashtag, whichever comes first.
* Comments can also go at the end of a file, even without a trailing hashtag or new line.
* If the "Announce_comments" value of Config.json is set to "1", they will be announced when passed over.

## Console functions
### Exit(n)
* Instantly exits the program, with n as the exit code.
* Prints the exit index & where
* n = A value of type string or int.
### Print(n)
* Prints n to the console.
* n = A value of any type
### Input(x)
* Asks the user for an input, then returns that input.
* Uses X as the stem when asking for the input.
* X = A value of any type. (but why wouldn't you use a string like what)

## Variable functions
### Let: x = n;
* Assigns variables
* x = The name of a variable
* n = A value of any type.
* Spaces are optional.
* The semicolon is neccesary.
* Variable reassignments don't need the "Let:" keyword
	* `let: x = 7;`
	* `let: y = x;`
	* `x = 3;`
	* `y = join(y, x);`
	* `print(y) # 73`
	* This is valid code.
### Type(x)
* Returns the type of X.
* X = a variable of any type

## String functions
### Join(x, y)
* Joins X & Y into one string.
* Returns a string.
* x & y = Values of any type
* Spaces are optional
### Slice(x, start, end, step)
* Slices X, like the built-in python function.
* X = the value to be sliced, of type string.
* start, end, & step = integers
* Spaces are optional
### Shuffle(x)
* Returns the shuffled version of X.
* x = A value of any type.
### Remove
#### Remove.substring(x, y)
* Removes Y from X, and returns the result.
* Y & X = Values of type string.
* Spaces are optional

## Boolean functions
### Not(x)
* Inverts the input & returns the result.
* x = a value of type boolean.
### And(x, y)
* Returns the && of x & y.
* x & y = values of type boolean.
* Spaces are optional
### Or(x, y)
* Returns the || of x & y.
* x & y = values of type boolean.
* Spaces are optional

## Arithmetic functions
### add(x, y)
* Adds X & Y, and returns the result.
* X & Y = values of type integer.
* Spaces are optional.

## Conditionals
### If(x): {}
* If X is true, code inside the brackets gets ran.
* Otherwise, skip to the closing bracket.
* Spaces are optional
* Line breaks are possible inside the brackets.
### Isequal(x, y)
* Checks if both values are equal
* Returns either True or False.
* x & y = Values of any type
* Spaces are optional
### Isgreater(x, y)
* Checks if X is greater than Y.
* Returns either True or False.
* x & y = Values of either int or string.
* Spaces are optional
### Islesser(x, y)
* Checks if X is less than Y.
* Returns either True or False
* x & y = Values of either int or string
* Spaces are optional

## Loops
### While(x): {}
* While X is true, repeat the code inside the loop.
* If X is false, the loop will end when the closing bracket is reached.
* Condition checks are only made when the closing bracket is reached.
* If X is false on the first check, no code inside the brackets will be ran.
* X = A value of type boolean.
* **WARNING:** Using this can lead to an infinite loop, only able to be broken out of with KeyboardInterrupt.
* Spaces are optional.
* Line breaks are possible inside the brackets.

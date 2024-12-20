# Ether Documentation
The most epic sauce programming language ever!!! :3

**If you find bugs, create an issue!**

## Common formatting / Notes
* Functions, such as `println(n)`, will have parenthesis around arguments.
* Functions can be nested nearly infinitely.
* Spp is a zero-indexed language.
* Files in the Ether format will be denoted with the file ending ".etr".
* The Config.json file is necessary for the interpreter to function.
* Line breaks, spaces, and tabs are not neccessary for the program to run.
  * An exception to this are comments.

## Config.json
### "Debug"
* Enables multiple functionalities meant for debugging purposes.
* If the value of "Debug" is set to 1, the interpreter does the following:
	* Prints the whole Config.json file to the console upon loading it.
	* Prints the program file's contents to the console upon loading it.
	* Prints the length of the file to the console.
	* Prints the amount of time it took for the file to be parsed for keywords.
	* Denotes when no errors occurred while parsing the file.
	* Shows the list of keywords after the file has been parsed.
 	* Prints to the console when `exit()` is used.
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
* Ends with a new line.
* Comments can also go at the end of a file, even without a trailing new line.
* If the "Announce_comments" value of Config.json is set to "1", they will be announced when passed over.

## Console functions
### Exit(n)
* Instantly exits the program, with n as the exit code.
* Prints the exit index & where
* n = A value of type string or int.
### Println(n)
* Prints n to the console in a line.
* n = A value of any type.
### Printnl(n)
* Prints n to the console, without a new line.
* n = A value of any type.
### Printvl(n, x)
* Prints n to the console, with x as the ending.
* n & x = Values of any type 
### Input(x)
* Asks the user for an input, then returns that input.
* Uses X as the stem when asking for the input.
* X = A value of any type.
### Throw(x)
* Raises an error with X as the error code.
* X = a value of type string

## Variable functions
### Let: x = n
* Assigns variables
* x = The name of a variable
* n = A value of any type.
* Spaces are optional.
* Variable reassignments don't need the "Let:" keyword
* Example:
```Ether
let: x = 7
let: y = x
x = 3
y = add(x, y)
print(y) # 10
```
### Type(x)
* Returns the type of X.
* X = a variable of any type
### Len(x)
* Returns the length of X.
* X = a variable of any type.
### var++
* Increments var by one.
* Faster when interpreting than saying `i = add(i, 1)`
### var--
* Decrements var by one.
* Faster when interpreting than saying `i = subtr(i, 1)`

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
### gtchar(x, y)
* Returns the Yth character of X.
	* (Zero-indexed)
* X = Value of type string.
* Y = Value of type integer.
### rpchar(x, y, z)
* Replaces the Yth character of X with Z.
	* (Zero-indexed)
* X & Z = Values of type string
* Y = value of type integer.
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
* Returns the logical AND of X & Y.
* x & y = values of type boolean.
* Spaces are optional
### Or(x, y)
* Returns the logical OR of X & Y.
* x & y = values of type boolean.
* Spaces are optional
### Xor(x, y)
* Returns the logical XOR of X & Y.
* X & Y = values of type boolean
* Spaces are optional

## Arithmetic functions
### eval(n)
* Evaluates the mathematical expression inside and returns the result.
* To use variables, use curly braces with the variable name inside, like `{index}`.
* Supported symbols:
  * `+` - Addition
  * `-` - Subtraction
  * `*` - Multiplication
  * `/` - Division
  * `%` - Modulus
  * `^` - Exponentiation
  * `()` - Parenthesis
  * `{}` - Variable usage
### add(x, y)
* Adds X & Y, and returns the result.
* X & Y = values of type integer.
* Spaces are optional.
### subtr(x, y)
* Subtracts Y from X, and returns the result.
* X & Y = values of type integer.
* Spaces are optional.
### multi(x, y)
* Multiplies X & Y together, and returns the result.
* X & Y = values of type integer.
* Spaces are optional.
### divi(x, y)
* Floor divides X by Y, and returns the result.
* X & Y = values of type integer.
* Spaces are optional.
### pow(x, y)
* Raises X to the power of Y, and returns the result.
* X & Y = values of type integer.
* Spaces are optional.
### mod(x, y)
* Modularly divides X by Y, and returns the result.
* X & Y = values of type integer.
* Spaces are optional.
### sqrt(x)
* Takes the square root of X and returns that value (rounded down).
* X = a value of type integer.

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
* **WARNING:** Using this can lead to an infinite loop, only able to be broken out of with Ctrl + C.
* Spaces are optional.
### Fornumb(x): {}
* Repeats code inside the brackets X amount of times
* X = a value of type integer
* Spaces are optional.
* Line breaks are possible inside the brackets.
### Break
* Breaks out of the highest level loop.
* Does not require any arguments or inputs.

## Functions
### Define foo args("bar", "baz") -> int: {}
* Defines a function with the name foo.
* Foo will take in two values as its inputs, bar and baz.
	* Input variables NEED to be defined before creating the function.
  * Input variables also need to be defined as a string in the function definition. (fix this later)
* Returns a value if `-> {type}` is included, otherwise it returns none.
* When called, the code inside the brackets will be run.
	* This example is called with the format `foo("argument 1", "argument 2")`
### Return x
* Only used inside of functions.
* Returns X out of the function.
	* Unless there's no `-> type` included OR if `-> none` is included when defining the function, then nothing should be included after it.
* Is required for any function to return from itself properly without breaking.
* Cannot be inside of a `while` or `for` loop, as it must be at the function's base level. (fix this later)
  * You can get around this by using a variable to store the function's return value before actually returning.
  * Example: (`rBoolean` is the return value)
```Ether
let: string = "";
let: character = "";
let: rBoolean = False;
let: indexOfChar = 0;
define isCharInString("string", "character") -> boolean: {
  indexOfChar = subtr(0, 1);
  rBoolean = False;
  fornumb(len(string)): {
    indexOfChar++
    if(isequal(gtchar(indexOfCharacter, string), character): {
      rBoolean = True;
      break
    }
  }
  return rBoolean
}
```

## Other functions
### Sleep(n)
* Pauses the program for n seconds.
* N = A value of type integer.
### MSleep(n)
* Pauses the program for n milliseconds.
* N = A value of type integer
### Timer
#### timer.start()
* Starts the timer, which runs until timer.stop() is called.
#### timer.restart()
* Restarts the timer.
#### timer.stop()
* Stops the timer.
* The timer value is frozen at the ending value, so you can still use `timer.get()` after stopping the timer.
#### timer.get()
* Gets the current timer value.
* Returns the current value as a string.
### randint(x, y)
* Returns a random integer between x & y, including both x & y.

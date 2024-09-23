# Demonstrates use of while loop in function (because i fixed it)
let: numb = 0
let: printWith = ""
define printNums args("numb", "printWith") -> string: {
  let: i = 0
  while(not(isequal(i, numb))): { # break out of the loop once i and numb are euqal
    i++
    println(join(printWith, i))
  }

  return "Done!"
}

println(printNums(200, "number: "))

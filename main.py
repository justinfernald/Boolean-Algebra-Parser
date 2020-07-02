# Author: Justin Fernald
# Date: 10/6/2019
# Description: A program that is very over complicated just to show a half-adder, full-adder, and binary number adder

# Copyright 2019 Justin Harold Fernald
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

operators = {  # Initialization of the operators used in the logic equations
    # This is the setting of the INVERT operation and what are the possible things you can enter to make it invert
    "INVERT": ['!', '~', 'NOT'],
    # This is the setting of the NAND operation and what are the possible things you can enter to make it not and
    "NAND": ['?', 'NAND'],
    # This is the setting of the NOR operation and what are the possible things you can enter to make it not or
    "NOR": ['/', 'NOR'],
    # This is the setting of the AND operation and what are the possible things you can enter to make it and
    "AND": ['^', '|', '.', 'AND'],
    # This is the setting of the XOR operation and what are the possible things you can enter to make it exclusive or
    "XOR": ['*', 'XOR'],
    # This is the setting of the OR operation and what are the possible things you can enter to make it or
    "OR": ['v', '+', 'OR'],
    # This is the setting of the IFONLY operation and what are the possible things you can enter to make it if and only if
    "IFONLY": ['#', '<->', 'IFONLY'],
    # This is the setting of the IF operation and what are the possible things you can enter to make it if
    "IF": ['@', '->', 'IF'],
    "TRUE": ['1', 'TRUE'],  # This is the setting of the TRUE value
    "FALSE": ['0', 'FALSE']  # This is the setting of the FALSE value
}


# The main function that parses a equation given the variables, all operators, and values
def parse(equation, variables, operators, values):
    # Runs the prepare function to make the equation ready to parse
    equation = prepare(equation, variables, operators, values)
    # Sets up so the paratheses can be gone through in order
    parsedSection = parseParentheses(equation)
    while (parsedSection != False):  # Loops if there is a section to loop through incased in parathese
        parsedEquationValue = parseStepLoop(
            equation[parsedSection[0] + 1:parsedSection[1]], operators)  # Does a parsing of a section in the parathesized section
        equation = equation[0:parsedSection[0]] + parsedEquationValue + \
            equation[parsedSection[1] + 1:len(
                equation)]  # Re-adds the value to the equation and removes the paratheses
        # Re-sets up so the paratheses can be gone through in order
        parsedSection = parseParentheses(equation)
    # Runs the parse loop one more time to finish the equation value
    equation = parseStepLoop(equation, operators)
    # Fixes the string values of 1 or 0 to True or False respectively
    return True if equation == "1" else (False if equation == "0" else equation)


# A functions the sets up the parsing loop so that the equation is broken down repetitively
def parseStepLoop(equation, operators):
    oldLength = 0  # Temporarily stores the old length of equation
    # Runs a loop if the length is not the same length as the previous ran equation and makes sure the length is greater than 1
    while (len(equation) != oldLength and len(equation) > 1):
        oldLength = len(equation)  # Resets the old length
        # Runs a step of the parsing and sets the equation to the value of the function
        equation = parseStep(equation, operators)
    return equation  # Returns the equation value for the parse loop


# A function that runs a single step through the parsing process
def parseStep(equation, operators):
    skip = False  # Sets a value for the skip to break out of the nested loop
    for operator in operators:  # Loops through all operators in order to set the order of operations
        # Loops through the equation and gives the index to set the order of operations from left to right
        for i in range(len(equation)):
            part = equation[i]  # Gets a single character of the equation
            # Checks to see if the character is a operation
            if (part == operators[operator][0]):
                # Gets the character to left of the operator
                left = equation[i - 1]
                # Gets the character to the right of the operator
                right = equation[i + 1]
                if (operator == "INVERT"):  # Checks to see if the operation character is the invert operation
                    # Checks to see if the character to the right is another invert operation
                    if (right == operators[operator][0]):
                        equation = equation[0:i] + \
                            equation[i + 2: len(
                                equation)]  # If it is another invert it just removes both inversions
                    elif (right == "0"):  # Checks to see if the right character is a 0
                        equation = equation[0:i] + "1" + \
                            equation[i + 2: len(equation)
                                     ]  # Sets the value of the operation to 1
                    elif (right == "1"):  # Checks to see if the right character is a 1
                        equation = equation[0:i] + "0" + \
                            equation[i + 2: len(equation)
                                     ]  # Sets the value of the operation to 0
                elif (operator == "NAND"):  # Checks to see if the operation character is the and operation
                    value = "1"  # Sets the value to 0 since it is 0 for most times
                    # Checks to see if both left and right are 1 or true
                    if (left == "1" and right == "1"):
                        value = "0"  # Sets the value to 1 or true
                    equation = equation[0:i-1] + value + \
                        equation[i + 2: len(equation)
                                 ]  # Sets the values of the operation to the value
                elif (operator == "NOR"):  # Checks to see if the operation character is the or operation
                    value = "0"  # Sets the value to 1 since it is 1 for most times
                    # Checks to see if both left and right are 0 or false
                    if (left == "0" and right == "0"):
                        value = "1"  # Sets the value to 0 or false
                    equation = equation[0:i-1] + value + \
                        equation[i + 2: len(equation)
                                 ]  # Sets the values of the operation to the value
                elif (operator == "AND"):  # Checks to see if the operation character is the and operation
                    value = "0"  # Sets the value to 0 since it is 0 for most times
                    # Checks to see if both left and right are 1 or true
                    if (left == "1" and right == "1"):
                        value = "1"  # Sets the value to 1 or true
                    equation = equation[0:i-1] + value + \
                        equation[i + 2: len(equation)
                                 ]  # Sets the values of the operation to the value
                elif (operator == "OR"):  # Checks to see if the operation character is the or operation
                    value = "1"  # Sets the value to 1 since it is 1 for most times
                    # Checks to see if both left and right are 0 or false
                    if (left == "0" and right == "0"):
                        value = "0"  # Sets the value to 0 or false
                    equation = equation[0:i-1] + value + \
                        equation[i + 2: len(equation)
                                 ]  # Sets the values of the operation to the value
                elif (operator == "XOR"):  # Checks to see if the operation character is the xor operation
                    value = "1"  # Sets the value to 1 but it could be 0 if the if statement was fully inverted
                    # Checks to see if the values are both 1's or trues; or both 0's or falses
                    if ((left == "1" and right == "1") or (left == "0" and right == "0")):
                        value = "0"  # Sets the value to 0 or false
                    equation = equation[0:i-1] + value + \
                        equation[i + 2: len(equation)
                                 ]  # Sets the value of the operation to the value
                # Checks to see if the operation character is the if only operation
                elif (operator == "IFONLY"):
                    value = "0"  # Sets the value to 0 but could be 1 if the if statement was fully inverted
                    # Checks to see if the values are both 1's or trues; or both 0's or falses
                    if ((left == "1" and right == "1") or (left == "0" and right == "0")):
                        value = "1"  # Sets the value to 1 or true
                    equation = equation[0:i-1] + value + \
                        equation[i + 2: len(equation)
                                 ]  # Sets the value of the operation to the value
                elif (operator == "IF"):  # Checks to see if the operation character is the if operation
                    value = "1"  # Sets the value to 1 since it is 1 for most times
                    # Checks to see if the left is 1 or true and the right is 0 or false
                    if (left == "1" and right == "0"):
                        value = "0"  # Sets the value to 0 or false
                    equation = equation[0:i-1] + value + \
                        equation[i + 2: len(equation)
                                 ]  # Sets the value of the operation to the value
                skip = True  # Skips the for loop since it found an operation
                break  # Breaks out of the 2nd level for loop
        if (skip):  # Checks to see if an operation was found
            break  # Breaks ouf the of the 1st level for loop since it did an operation
    return equation  # Returns the new equation value


# A function the parses parentheses and gets the next part of the equation to parse
def parseParentheses(s):
    lastOpen = False  # Sets that the parentheses have not been opened
    for i in range(len(s)):  # Loops through the equation
        c = s[i]
        if c == '(':  # Checks to see if there is an opening parathese
            lastOpen = i  # Sets the lastOpen value to the opening parathese
        # Checks to see if there is an closing parathese and if there is an opening parathese
        elif c == ')' and ((lastOpen != False) or (str(lastOpen) == "0")):
            # Returns the opening location and closing location of the parathese pair
            return (lastOpen, i)
    return False  # Returns false if no pairs are found


# A function that prepares an equation so it is ready for parsing
def prepare(equation, variables, operators, values):
    equation = equation.replace(" ", "")  # Removes all spaces in the equation
    for operator in operators:  # Loops through all operations
        # Loops through all the operation choices except the first one
        for o in operators[operator][1:]:
            # Replaces all operation choices to the first operation choice
            equation = equation.replace(o, operators[operator][0])
    # Loops through all the variables and gets the index value
    for index in range(len(variables)):
        equation = equation.replace(
            variables[index], "1" if values[index] else "0")  # Sets all the variables to their respective values
    return equation  # Returns the new prepared equation


def flipArray(input):  # Flips a 2d multi-dimensional array
    output = []  # Initialization and output array that will be added onto
    # Loops through the length of the 2nd level array's
    for i in range(len(input[0])):
        # Creates an array to bin the new values in the 2nd level
        output.append([])
        for j in range(len(input)):  # Lops through the 1st level of the input array
            # Sets values to the array bin with the inverse location
            output[i].append(input[j][i])
    return output  # Returns the flipped array


# A function that returns an array with all possible binary options for a certain number of inputs
def getPossibleValues(inputCount):
    outputCount = 2**inputCount  # Gets the number of outputs in total
    flipCount = outputCount  # Sets how ofter the truth values will be flipped
    output = []  # Sets up an array to be filled with the truth values
    # Loops through the input counts to get how many truth bins there will be
    for i in range(inputCount):
        flipped = False  # Sets the value to be false as start
        flipCount /= 2  # Sets a new flip count being half as much as it was before
        output.append([])  # Creates a new bin for a input
        for j in range(outputCount):  # Loops through the number of outputs
            if (j % flipCount == 0):  # Checks to see if it has run for the number of flip counts
                flipped = not flipped  # If it is at the flip count it will flip the value
            output[i].append(flipped)  # Appends the value in the truth bin
    return output  # Returns all the outputs for the possible binary options

# A function that sets up a table with given variables, equations ,inputs, and outputs


def formatTable(variables, equations, inputs, outputs, tableName):
    HEADERSPACE = 3  # sets up how much space should be between every element
    header = tableName + " " * 30  # sets up a value for the header line

    # adds a border line on top with the length of the header
    print("+" + "-" * (len(header) + 1) + "+")
    print("| " + header + "|")  # adds the header line
    # adds another border line to seperated the values from the headers
    print("+" + "-" * (len(header) + 1) + "+")
    for i in range(len(inputs)):  # loops through all the inputs and gets the index
        line = "| "  # Adds a starting cap to the table row
        # loop through all the variables to display the input truth values
        for j in range(len(variables)):
            variable = variables[j]  # gets the variable at the index
            # converts boolean value to T and F respectively
            value = variable + " = " + ("T" if inputs[i][j] else "F")
            # Adds variable's truth value to table row
            line += value + " " * (len(variable) + HEADERSPACE - 1)
        line = line[:-1] + "| "  # Adds seperator from variables to equations
        # Loops through all the equations to display the output values for the equation
        for k in range(len(equations)):
            equation = equations[k]  # gets the equation at the index
            # converts boolean value to T and F respectively
            value = equation + " = " + ("True" if outputs[i][k] else "False")
            # Adds equation's output value to table row
            line += value
            line += " " * ((len(header) - len(line)) + 2)
        line += "|"  # Adds cap to end of table row
        print(line)  # Prints the table row for the variables and equations
    # Prints a formatting line to close the table
    print("+" + "-" * (len(header) + 1) + "+")


def halfAdder(a, b): #a function that adds two binary digits together with no carry
    return fullAdder(a, b, 0) #returns a full adder without a carry value which is a half adder
    

def fullAdder(a, b, c): #a function that adds two binary digits together with a carry
    output = {} #initializes a variable that will contain the outputs for the function
    variables = ['a', 'b', 'c'] #sets the variables that will be inputted
    equations = {
        "C": "a AND b OR c AND (a XOR b)", #sets the equation that the carry will have
        "S": "(a XOR b) XOR c" #sets the equation that the sum will have
    }
    for i in equations: #loops through all equations
        value = parse(equations[i], variables, operators, [a, b, c]) #runs the equation parses to produce the outputs
        output[i] = value #sets the value from the parser for the outputs setting the key to the equation key
    return output #returns the output with the key value pairs of S and C for sum and carry

def binaryAdder(a, b): #a functions that adds two binary numbers together as a parallel adder
    longest = len(a) if len(a) > len(b) else len(b) #finders the longer value in digits count then sets the digit count
    a = "0" * (longest - len(a)) + a #makes variable value the same length by adding 0's
    b = "0" * (longest - len(b)) + b #makes variable value the same length by adding 0's
    c = 0 #sets the carry value to 0 since no carry is there for first digit
    output = "" #initializes the outputs to be nothing that is added on with binary digits

    for i in range(longest - 1, -1, -1): #loops and sets an index starting from the first digit which is the last index and goes to 0
        value = fullAdder(int(a[i]), int(b[i]), c) #gets the value of the full adder from the certain index and adds on the carry
        c = value["C"] #gets the carry value and sets it
        output = boolToBinary(value["S"]) + output #adds onto the output with the value first so it is in reversed order so it undoes the first reversion
    if (c): #checks if the carry exists
        output = boolToBinary(c) + output #if the carry exists it adds it to the end
    return output #returns the output

def boolToBinary(input): #a function that converts a boolean value to a binary string
    return "1" if input else "0" #converts bool value to respective binary value as string

def stringToTuple(input): #converts a string into a tuple value for each index for every character
    output = [] #sets up array to be added onto from string
    for i in range(len(input)): #loop through string
        output.append(int(input[i])) #convert char to int then add int to output array
    return tuple(output) #convert array to tuple then returns tuple

def getBinaryNumber(): #functions that gets a binary number and makes sure it is one
    value = input("Enter a Binary Number: ") # requests a binary number for input
    passes = True #sets up a variable that will be turned false if it doesn't pass
    for char in value: #loops through each digit in inputted value
        if (char not in "01"): #checks to see if value is a not a 1 or 0
            passes = False #sets that it does not pass
            break #breaks out of loop since no need to check further
    if passes: #if it passes it will return value
        return value #returns binary number
    print("Invalid input") #prints warning that input was not valid
    return getBinaryNumber() #tries to get binary number again

def main(): #the main function that is ran first
    SPACE = 2 #just a constant to make the space between different things displayed
    variables = ['i','j','k'] #all the variables that will be used passed to half adder and full adder

    print("Half-Adder") #just display what is going to be shown next
    inputs = flipArray(getPossibleValues(2)) #gets all possible values and flips array so it is ready for half adder function
    for inputValues in inputs: #loops through all the possible inputs
        for inputIndex in range(len(inputValues)): #loops through each input value to display it 
            print(variables[inputIndex] + " = " + boolToBinary(inputValues[inputIndex]), end=" " * SPACE) #displays variable with respective value
        print("|", end=" " * SPACE) #creates seperator between inputs and outputs
        output = halfAdder(*inputValues) #gets the output by sending input to the half adder function
        for outputIndex in output: #loops through output for each output
            print(outputIndex + " = " + boolToBinary(output[outputIndex]), end=" " * SPACE) #displays output variables with respective value
        print() #adds print for spacing
    print() #adds print for spacing

    print("Full-Adder") #just display what is going to be shown next
    inputs = flipArray(getPossibleValues(3)) #gets all possible values and flips array so it is ready for full adder function
    for inputValues in inputs: #loops through all the possible inputs
        for inputIndex in range(len(inputValues)): #loops through each input value to display it 
            print(variables[inputIndex] + " = " + boolToBinary(inputValues[inputIndex]), end=" " * SPACE) #displays variable with respective value
        print("|", end=" " * SPACE) #creates seperator between inputs and outputs
        output = fullAdder(*inputValues) #gets the output by sending input to the full adder function
        for outputIndex in output: #loops through output for each output
            print(outputIndex + " = " + boolToBinary(output[outputIndex]), end=" " * SPACE) #displays output variables with respective value
        print() #adds print for spacing
    print() #adds print for spacing
    
    num1 = getBinaryNumber() #gets a binary number for input to send to adder
    num2 = getBinaryNumber() #gets a binary number for inputs to send to adder

    print(num1 + " + " + num2 + " = " + binaryAdder(num1, num2)) #prints the values inputted along with parallel adder's output
    
main() #runs the main function

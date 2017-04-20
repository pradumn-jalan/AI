import string
import itertools
import copy

def AND( A, B ):
    solution = A and B
    return solution

def OR( A, B ):
    solution = A or B
    return solution

def CONDITIONAL( A, B ):
    solution = not(A) or B
    return solution

def BICONDITIONAL( A, B ):
    solution = (not(A) or B) and (not(B) or A)
    return solution

def NOT( A ):
    solution = not(A)
    return solution

def XOR( A, B):
    solution = (A and not(B)) or (not(A) and (B))
    return solution
# Helper precidence function
def priorityCheck( postfixStack, operandStack, OPERAND):
    # Pop operand from operand stack only if operand has lesser precidence the previos operands
    if OPERAND == "(":
        operandStack.append("(")
    if OPERAND == ")":
        while operandStack[-1]!="(":
            postfixStack.append(operandStack.pop())
        operandStack.pop()
    if OPERAND == "!":
        operandStack.append("!")
    if OPERAND == "+":
        while operandStack[-1]=="+" or operandStack[-1]=="!":
            postfixStack.append(operandStack.pop())
        operandStack.append("+")
    if OPERAND == "&":
        while operandStack[-1]=="&" or operandStack[-1]=="!" or operandStack[-1]=="+":
            postfixStack.append(operandStack.pop())
        operandStack.append("&")
    if OPERAND == "|":
        while operandStack[-1]=="&" or operandStack[-1]=="|" or operandStack[-1]=="!" or operandStack[-1]=="+":
            postfixStack.append(operandStack.pop())
        operandStack.append("|")
    if OPERAND == "-":
        while operandStack[-1]=="&" or operandStack[-1]=="|" or operandStack[-1]=="-" or operandStack[-1]=="!" or operandStack[-1]=="+":
            postfixStack.append(operandStack.pop())
        operandStack.append("-")
    if OPERAND == "=":
        while operandStack[-1]=="&" or operandStack[-1]=="|" or operandStack[-1]=="=" or operandStack[-1]=="-" or operandStack[-1]=="!" or operandStack[-1]=="+":
            postfixStack.append(operandStack.pop())
        operandStack.append("=")

def postFixConverter ( STRING ):
    stringStack = list("("+STRING+")")
    postfix = []
    operandStack = []

    for i in stringStack:
        if i!="(" and i!=")" and i!="!" and i!="&" and i!="|" and i!="=" and i!="-" and i!="+":
            postfix.append(i)
        else:
            priorityCheck( postfix, operandStack, i )

    while len(operandStack)!=0:
        temp = operandStack.pop()
        if temp!="(":
            postfix.append(temp)

    return postfix

def trueValue ( POSTFIX, truthArray ):
    constantArray = list(string.ascii_lowercase)
    for i in range(len(truthArray)):
        exec(str(constantArray[i].upper())+"="+str(truthArray[i]))
    stack = []
    PostfixList = list(POSTFIX)
    for i in PostfixList:
        if i=="!":
            a = eval(str(stack.pop()))
            stack.append(NOT(a))
        
        elif i=="+":
            b = eval(str(stack.pop()))
            a = eval(str(stack.pop()))
            stack.append(XOR(a,b))
        elif i=="&":
            b = eval(str(stack.pop()))
            a = eval(str(stack.pop()))
            stack.append(AND(a,b))
        elif i=="|":
            b = eval(str(stack.pop()))
            a = eval(str(stack.pop()))
            stack.append(OR(a,b))
        elif i=="-":
            b = eval(str(stack.pop()))
            a = eval(str(stack.pop()))
            stack.append(CONDITIONAL(a,b))
        elif i=="=":
            b = eval(str(stack.pop()))
            a = eval(str(stack.pop()))
            stack.append(BICONDITIONAL(a,b))
        else:
            stack.append(eval(str(i)))
    # print stack
    return stack[0]

def evaluator ( STATEMENT, TESTDATA ):
    postfix = postFixConverter(STATEMENT)
    truthTable = []

    for i in TESTDATA:
        truthTable.append(trueValue(postfix,list(i)))

    return truthTable

# Test Value generator
def testValueGenerator(size):
    testData = list(itertools.product([True,False],repeat=size))
    return testData

def preProcess(QESTIONSTATEMENT):
    validLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    max = 0;
    temp = copy.deepcopy(QESTIONSTATEMENT)
    maxConstant = set()

    for i in temp:
        newString = ''
        for char in i:
            if char in validLetters:
                newString += char
                maxConstant.add(char)
        if len(newString) > max:
            max = len(newString)

    preProcessData = []
    preProcessData.append(max)
    preProcessData.append(sorted(list(maxConstant)))
    return preProcessData

# ================================================ Question Solving =================================================
def findTautology(truthTable):
    print( "" )
    for i in range(len(truthTable)):
        if len(set(truthTable[i])) == 1 and list(set(truthTable[i]))[0] == True:
            print ( "Premise "+str(i+1)+" is a tautology" )

def findContradiction(truthTable):
    print( "" )
    for i in range(len(truthTable)):
        if len(set(truthTable[i])) == 1 and list(set(truthTable[i]))[0] == False:
            print ( "Premise "+str(i+1)+" is a contradiction" )

def findContingency(truthTable):
    print( "" )
    for i in range(len(truthTable)):
        if len(set(truthTable[i])) != 1:
            print ( "Premise "+str(i+1)+" is a contingency" )

def findEquivalence(truthTable):
    print( "" )
    for i in range(len(truthTable)):
        for j in range(len(truthTable)):
            if i == j:
                continue
            if( truthTable[i] == truthTable[j] ):
                print( "Premise"+ str(i+1) +" and "+"Premise"+ str(j+1) +" are equivalent")

def findEntailment(truthTable):
    print( "" )
    for i in range(len(truthTable)):
        for j in range(len(truthTable)):
            entailment = 1
            if i == j:
                continue
            for k,l in zip( truthTable[i], truthTable[j] ):
                if CONDITIONAL(k,l) == False:
                    entailment = 0
            if entailment == 1:
                print("Premise"+ str(j+1)+" is logically entalied by Premise"+str(i+1))


def findPremiseConsistency(truthTable):
    print("")
    consistent = 0
    for i in range(len(truthTable[0])):
        consistent = 1
        for j in range(len(truthTable)):
            if truthTable[j][i] == False:
                consistent = 0
        if consistent == 1:
            print("The Premises are consistent")
            break;



print("-------------------------------------Prepositional Logic Finder---------------------------------------------")
print("The following symbols lead to the following symantics:")
print("1) !        for        NOT")
print("1) &        for        AND")
print("1) |        for        OR")
print("1) -        for        CONDITIONAL")
print("1) =        for        BICONDITIONAL")
print("Paranthesis can also be used....")

n = input("\nNumber of Premise: ")
truthTable = []
questionStatement = []

for i in range(n):
    temp = raw_input("Premise-"+str(i+1)+": ")
    questionStatement.append(temp.upper())

preProcessData = preProcess(questionStatement)
maxConstant = preProcessData[0]

# Using the highest number of constants to generate testcase
testData = testValueGenerator( maxConstant )

for i in questionStatement:
    truthTable.append(evaluator( i, testData ))

# Using it again to show data
print("\n\n "),
print '      '.join(preProcessData[1]),
for i in range(n):
    print("      "+"P"+str(i+1)),
print("")
# print testData
for j in range(len(truthTable[0])):
    print('   '.join(map(str,list(testData[j])))),
         
    for i in range(n):
        print("  "+str(truthTable[i][j])),
    print( "" )
# ===================================== Question Solving =====================================================
findTautology(truthTable)
findContradiction(truthTable)
findContingency(truthTable)
findEquivalence(truthTable)
findEntailment(truthTable)
findPremiseConsistency(truthTable)

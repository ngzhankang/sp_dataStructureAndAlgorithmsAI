# import necessary classes and libraries
import os.path
import math
from binaryTree import binaryTree
from sortValue import sortValue
from sortLength import sortLength
from node import node
from sortedList import sortedList
from stack import stack
from treeLayout import display

stack = stack()

# print the selection menu
def selectionMenu():
    print('*' * 62)
    print('* ST1507 DSAA: Expression Evaluator & Sorter {:>17}'.format('*'))
    print('*' + '-' * 60 + '*')
    print('* {:>60}'.format('*'))
    print('*  ' + '- Done by: Ng Zhan Kang(1935727) & Triston Loh(1935488) {:>3}'.format('*'))
    print('*  ' + '- Class DIT/2B/11 {:>41}'.format('*'))
    print('*' * 62)
    print()
    print("Please select your choice ('1','2','3'):")
    print("  1. Evaluate expression")
    print("  2. Sort expressions")
    print("  3. Exit")

    choice = ''
    
    # loop to run the selection menu
    while choice != '3':
        choice = input('Enter Choice: ')
        if choice == '1':
            choice1()
        if choice == '2':
            choice2()
        if choice == '3':
            choice3()
        else:
            print("Invalid input! Please input 1, 2 or 3!")

# define how we validate our user equation first before we proceed on to deal with the equation
def validate(myStr):    
    open_list = ["[","{","("] 
    close_list = ["]","}",")"] 
    stack = []
    for i in myStr:
        if i in open_list:
            stack.append(i)
        elif i in close_list:
            pos = close_list.index(i)
            if ((len(stack) > 0) and (open_list[pos] == stack[len(stack) - 1])):
                stack.pop()
            else:
                return False
    if len(stack) == 0:
        return True
    else:
        return False

# build a parse tree
def buildParseTree(exp):
    # tokenize the expression
    tokens = []
    no = ""
    ast = ""
    for x in range(0, len(exp)):
        # skip spaces
        if exp[x] == " ":pass
        # concatenate digits or '.' to number
        elif exp[x].isdigit() or (exp[x] == "."):
            no += exp[x]
        # concatenate subtraction and subtraction or addition and addition to be addition
        elif (exp[x] == '-' and exp[x-1] == '-') or (exp[x] == '+' and exp[x-1] == '+'):
            del tokens[-1]
            ast = '+'
            tokens.append(ast)
            ast = ""
        # concatenate subtraction and addition to be subtraction
        elif (exp[x] == '-' and exp[x-1] == '+') or (exp[x] == '+' and exp[x-1] == '-'):
            del tokens[-1]
            ast = '-'
            tokens.append(ast)
            ast = ""
        # concatenate negative symbol to number
        elif exp[x] == '-' and exp[x-1] in ['+', '-', '*', '/', '**', '(']:
            no += exp[x]
        # concatenate positive symbol to number
        elif exp[x] == '+' and exp[x-1] in ['+', '-', '*', '/', '**', '(']:
            no += exp[x]
        # concatenate asterik to another asterik
        elif (exp[x] == "*" and exp[x-1] == "*"):
            del tokens[-1]
            ast = '**'
            tokens.append(ast)
            ast = ""
        # concatenate slash to another slash
        elif (exp[x] == "/" and exp[x-1] == "/"):
            del tokens[-1]
            ast = "//"
            tokens.append(ast)
            ast = ""   
        else:
            if no != "":
                tokens.append(no)
            tokens.append(exp[x])
            no = ""

    tree = binaryTree('?')
    stack.push(tree)
    currentTree = tree
    
    for t in tokens:
        # rule 1: If token is '(' add a new node as left child and descend into that node
        if t == '(':
            currentTree.insertLeft('?')
            stack.push(currentTree)
            currentTree = currentTree.getLeftTree()
        # rule 2: If token is operator, set key of current node to that operator and add a new node as right child and descend into that node
        elif t in ['+', '-', '*', '/', '**', '//', '%']:
            currentTree.setKey(t)
            currentTree.insertRight('?')
            stack.push(currentTree)
            currentTree = currentTree.getRightTree() 
        # rule 3: If token is number, set key of the current node to that number and return to parent
        elif t not in ['+', '-', '*', '/', '**', '//', '%', ')']:
            currentTree.setKey(t)
            parent = stack.pop()
            currentTree = parent
        # rule 4: If token is ')' go to parent of current node
        elif t == ')':
            currentTree = stack.pop()
        else:
            raise ValueError

    return tree

# evaluate the expression
def evaluate(tree):
    leftTree = tree.getLeftTree()
    rightTree = tree.getRightTree()
    op = tree.getKey()
    
    # loop to return the true value of each pair of terms of the expression
    if leftTree != None and rightTree != None:
        if op == '+':
            return float(evaluate(leftTree)) + float(evaluate(rightTree))
        elif op == '-':
            return float(evaluate(leftTree)) - float(evaluate(rightTree)) 
        elif op == '*':
            return float(evaluate(leftTree)) * float(evaluate(rightTree))
        elif op == '**':
            return float(evaluate(leftTree)) ** float(evaluate(rightTree))
        elif op == '/':
            return float(evaluate(leftTree)) / float(evaluate(rightTree))
        elif op == '//':
            return float(evaluate(leftTree)) // float(evaluate(rightTree))
        elif op == "%":
            return float(evaluate(leftTree)) % float(evaluate(rightTree))
    else:
        return tree.getKey()

# change "num" into a decimal < 1
def toLessThanOne(num): 
    while num > 1:
        num /= 10
    return num

# converts float number to binary
# we will round it to 3 places
def toBinary(num, places=3):
    integral, fractional = str(num).split(".")                 
    integral, fractional = int(integral), int(fractional) 
    if fractional == 0:
        res = bin(integral).lstrip("0b")
        return res
    else:
        res = bin(integral).lstrip("0b") + "."
        for x in range(places):
            integral, fractional = str((toLessThanOne(fractional)) * 2).split(".") 
            fractional = int(fractional)
            res += integral
    return res

# converts float number to octal
# we will round it to 8 places
def toOctal(num, places=8):
    integral, fractional = str(num).split(".")                 
    integral, fractional = int(integral), int(fractional)
    if fractional == 0:
        # removes the 0x in front of output
        res = oct(integral)[2::]
        return res
    else:
        res = oct(integral)[2::]+"."    
        for x in range(places): 
            integral, fractional = str((toLessThanOne(fractional)) * 8).split(".")            
            fractional = int(fractional)
            res += integral 
    return res

# display selection screen for base conversion
def displayBaseConversion():
    print("Do you want to convert the evaluated value? 'y' or 'n'")
    baseSelect = ''
    while baseSelect != 'n' or baseSelect != 'y':
        baseSelect = input(">>> ")
        if baseSelect == 'n':
            input("Press any key, to continue....")
            selectionMenu()
        if baseSelect == 'y':
            print()
            print("How do you want to convert the evaluated value?")
            print("  1. Convert to binary")
            print("  2. Convert to hexadecimal")
            print("  3. Convert to octal")
            print("  4. Exit")
            baseSelection = ''
            while baseSelection != '4':
                baseSelection = input(">>> ")
                if baseSelection == '1':
                    print(f'The value {evaluate(tree)} converted to binary is: \n{toBinary(evaluate(tree))} (3 d.p)')
                    print()
                    input("Press any key, to continue....")
                    selectionMenu()
                if baseSelection == '2':
                    hexed = float.hex(float(evaluate(tree)))
                    print(f"The value {evaluate(tree)} converted to hexadecimal is: \n{hexed.split('x')[-1]}") 
                    print()
                    input("Press any key, to continue....")
                    selectionMenu()
                if baseSelection == '3':
                    print(f"The value {evaluate(tree)} converted to octal is: \n{toOctal(evaluate(tree))} (8 d.p)")
                    print()
                    input("Press any key, to continue....")
                    selectionMenu()
                if baseSelection == '4':
                    print()
                    choice3()
                else:
                    print("Invalid input! Please input 1, 2, 3 or 4!")
        else:
            print("Invalid input! Please input 'n' or 'y'")

# sorting using merge sort method
def mergeSort(l):
    for i in l:
        if len(l) > 1:
            mid = int (len(l)/2) 
            leftHalf = l[:mid]
            rightHalf = l[mid:] 
            mergeSort(leftHalf)
            mergeSort(rightHalf)
            
            # declare the starting indexes as 0
            leftIndex, rightIndex, mergeIndex = 0, 0, 0
            
            # declare mergeList as l (list)
            mergeList = l
            
            # handle those items still left in both the left half and right half
            while leftIndex < len(leftHalf) and rightIndex < len(rightHalf):
                if leftHalf[leftIndex] < rightHalf[rightIndex]:
                    mergeList[mergeIndex] = leftHalf[leftIndex]
                    leftIndex+=1
                else:
                    mergeList[mergeIndex] = rightHalf[rightIndex]
                    rightIndex+=1
                mergeIndex+=1

            # handle those items still left in the left Half
            while leftIndex < len(leftHalf):
                mergeList[mergeIndex] = leftHalf[leftIndex]
                leftIndex+=1
                mergeIndex+=1
                
            # handle those items still left in the right Half
            while rightIndex < len(rightHalf):
                mergeList[mergeIndex] = rightHalf[rightIndex]
                rightIndex+=1
                mergeIndex+=1

# change the positions of key and value in the dictionary arranged in either ascending or descending order based on value
def order(x, y):
    if orderSelect == '1':
        if x[1] < y[1]: 
            return x, y
        else: 
            return y, x
    elif orderSelect == '2':
        if x[1] > y[1]:
            return x, y
        else:
            return y, x
        
# do a bubble sort to sort by value
def bubble(mydict):
    d_items = list(mydict.items())
    for j in range(len(d_items) - 1):
        for i in range(len(d_items) - 1):
            d_items[i], d_items[i+1] = order(d_items[i], d_items[i+1])
    return d_items

# sort by equation length
def sortsLength(lists):
    # this is the index to determine location in the big list
    index = 0 
    for x in lists:
        # if it is a single element list
        if len(x) == 1:
            index += 1
            continue
        else:
            eqn_list = []
            # if it is a multiple element lists, loop through the big list
            for n in x:
                eqn_list.append(sortLength(n[0]))

            mergeSort(eqn_list)
            temp_list = []

            for i in range(0, len(eqn_list), 1):
                temp_tuple = list(x[i])
                temp_tuple[0] = eqn_list[i]
                back_tuple = tuple(temp_tuple)
                temp_list.append(back_tuple)

            lists[index] = temp_list
            index += 1
    return lists

# encapsulate each item in the list with [] to allow for comparison with another list
def extractDigits(lst): 
    res = [] 
    for el in lst: 
        sub = el.split(', ') 
        res.append(sub) 
    return(res) 


##############################################################################
##############################################################################
# main functions
# function to carry out choice 1  
def choice1():
    exp = input("Please enter the expression you want to evaluate: \n")
    # validate validity of expression here
    validation = validate(exp)
    while exp == '' or validation == False:
        if exp == '':
            print("Expression is empty! Please input an expression!")
        else:
            print("Invalid Expression! Check parenthesis!")            
        exp = input("Please enter the expression you want to evaluate: \n")
    exp = exp.replace(" ", "")
    global tree
    tree = buildParseTree(exp)
    print()
    print("How do you want to print the parse tree?")
    print("  1. Pre-order")
    print("  2. Post-order")
    print("  3. In-order")
    print("  4. Exit")
    printSelect = ''
    while printSelect != '4':
        printSelect = input(">>> ")
        if printSelect == '1':
            print()
            print("Expression Tree: ")
            tree.printPreorder(0)
            print()
            print("Binary Tree Diagram:")
            display(tree)
            print()
            print(f'Expression evaluates to: \n{evaluate(tree)} \n')
            displayBaseConversion()

        if printSelect == '2':
            print()
            print("Expression Tree: ")
            tree.printPostorder(0)
            print()
            print("Binary Tree Diagram:")
            display(tree)
            print()
            print(f'Expression evaluates to: \n{evaluate(tree)} \n')
            displayBaseConversion()

        if printSelect == '3':
            print()
            print("Expression Tree: ")
            tree.printInorder(0)
            print()
            print("Binary Tree Diagram:")
            display(tree)
            print()
            print(f'Expression evaluates to: \n{evaluate(tree)} \n')  
            displayBaseConversion()

        if printSelect == '4':
            choice3()

        else:
            print("Invalid input! Please input 1, 2, 3 or 4!")

# function to carry out choice 2
def choice2():
    # create a compare list to append the corrected list
    unstructured_list = []
    eqn_list = []
    print()
    inputFile = input("Please enter input file: ")
    while True:
        if os.path.isfile(inputFile): 
            break
        else:
            print('Invalid file name! File not found!')
            inputFile = input("Please enter valid input file: ")        
    outputFile = input("please enter output file: ")
    print()
    print('Do you want to print the sorting of values in ascending or descending order?')
    print("  1. Ascending")
    print("  2. Descending")
    print("  3. Exit")
    global orderSelect
    orderSelect = ''
    while orderSelect != '3':
        orderSelect = input(">>> ")
        print()
        if orderSelect == '1':
            break
        if orderSelect == '2':
            break
        if orderSelect == '3':
            choice3()
        else:
            print("Invalid input! Please input 1, 2, 3!")
    print(">>>Evaluation and sorting started:")
    print()
    l = sortedList()

    # read expressions from input file and sort in list
    # we also remove any whitespace so that we can compare length of equations fairly
    f = open(inputFile, 'r')
    for expressions in f:
        # validate validity of expression here
        validation = validate(expressions)
        while validation == False:
            print("Invalid Expression In File Detected! Check parenthesis! Returning to menu...")
            print()
            selectionMenu()
        expressions = expressions.strip()
        expressions = expressions.replace(" ", "")
        tree = buildParseTree(expressions)
        # here we evaluate the expression and then sort by value
        eqn_list.append(expressions)
        l.insert(sortValue(evaluate(tree)))
        unstructured_list.append(sortValue(evaluate(tree)))
    f.close()

    # make a dictionary for the equation and values
    dictionary = dict(zip(eqn_list, unstructured_list))

    # bubble sort the dictionary
    sorted_tuples = bubble(dictionary)
    new_list = []

    # loop through the tuples in the list and encapsulate tuples with similar values together with []
    for n in sorted_tuples:
        if len(new_list) == 0: 
            new_list.append([n])
        else:
            if new_list[-1][-1][1] == n[1]:
                new_list[-1].append(n)
            else: 
                new_list.append([n])
    
    # sort the list that is sorted by value based on length of equation
    finalSorted = sortsLength(new_list)
    
    temp_valList = [[x[1] for x in l] for l in finalSorted]
    expList = [[x[0] for x in l] for l in finalSorted]
    valList = []
    valsList = []

    # remove duplicate values
    for i in temp_valList:
        for x in i:
            if x not in valList:
                valList.append(x)
    
    # get rid of quotes from values
    for g in valList:
        value = str(g).strip('"\'')
        valsList.append(value)

    # get the list back with each item encapsulated by []
    valList = extractDigits(valsList)   
    
    # zip valList and expList so that we can compare the 2 list
    # then we print based on list index
    for val, exp in zip(valList, expList):
        result = val[0]
        print(f'*** Expressions with value => {result}')
        for e in exp:
            print(f'{e} ==> {result}')
        print()
        
    # write sorted expressions into output file
    f = open(outputFile, 'w')
    for val, exp in zip(valList, expList):
        result = val[0]
        f.write(f'*** Expressions with value => {result}\n')
        for e in exp:
            f.write(f'{e} ==> {result}\n')
        f.write('\n')
    f.close()

    print(">>>Evaluation and sorting completed!")
    input("Press any key, to continue....")
    selectionMenu()

# function to carry out choice 3
def choice3():
    print("Bye, thanks for using ST1507 DSAA: Expression Evaluator & Sorter")
    exit()

selectionMenu()
import os
from enum import Enum

# Things to do
#   - Parse out negative numbers.
#   - Combine parentheses code with the rest of the code. Ie. Figure out how to
#     validate statements between parentheses pairs.
#   - Implement assignment. Should be done after the above two objectives.
#   - Figure out how to generate tests cases. How do you test a parser?
#   - Look into optimizing some of the algorithms. I do lots of searching that I maybe don't have to do.
# Need to build out tree. Easiest way to solve the edge cases I am seeing. Node is operator or statement

# Tree generation
#   Number & open parentheses valid first tokens
#   Number can transition to operator or close parentheses if open has been seen
#   Open parentheses can transition to number or open parentheses
#   Operator can transition to open parentheses or number
#   Operators cannot be leaves
#   Numbers must be leaves
#   Parentheses generate sub trees to be evaluated. The can be leaves or nodes (kinda? will think about this) 

# Nodes can consist of 3 values
# Number/Value <- Leaf
# Operator <- parent of two children]

class OperatorType(Enum):
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4

class Types(Enum):
    NUMBER = 1
    OPERATOR = 2
    OPEN_PARENTHESES = 3
    CLOSE_PARENTHESES = 4

def CharToOperatorType(val):
    if val == '+':
        return OperatorType.ADDITION
    if val == '-':
        return OperatorType.SUBTRACTION
    if val == '/':
        return OperatorType.DIVISION
    if val == '*':
        return OperatorType.MULTIPLICATION

def OperatorRank(operator):
    if operator == OperatorType.ADDITION:
        return 1
    elif operator == OperatorType.SUBTRACTION:
        return 1
    elif operator == OperatorType.MULTIPLICATION:
        return 2
    elif operator == OperatorType.DIVISION:
        return 2

def IsLeftAssociative(operator):
    if operator == OperatorType.ADDITION:
        return False
    elif operator == OperatorType.SUBTRACTION:
        return True
    elif operator == OperatorType.MULTIPLICATION:
        return False
    elif operator == OperatorType.DIVISION:
        return True

def GenerateOrderedTypeList(line):
    current_number = None
    retval = []
    for char in line:
        examined_type = None
        if char.isnumeric():
            examined_type = Types.NUMBER
        elif char == '(':
            examined_type = Types.OPEN_PARENTHESES
        elif char == ')':
            examined_type = Types.CLOSE_PARENTHESES
        elif char in ['+', '-', '*', '/']:
            examined_type = Types.OPERATOR
        else:
            raise ValueError("Invalid type: {}".format(char))

        if examined_type == Types.NUMBER:
            if current_number:
                current_number = current_number + char
            else:
                current_number = char
        else:
            if current_number:
                retval.append((Types.NUMBER, int(current_number)))
                current_number = None
            if examined_type == Types.OPERATOR:
                retval.append((Types.OPERATOR, CharToOperatorType(char)))
            elif examined_type == Types.OPEN_PARENTHESES:
                retval.append((Types.OPEN_PARENTHESES,))
            elif examined_type == Types.CLOSE_PARENTHESES:
                retval.append((Types.CLOSE_PARENTHESES,))
    return retval

def GenerateRPN(type_list):
    output_queue = []
    operator_stack = []
    for val in type_list:
        if val[0] == Types.NUMBER:
            output_queue.append(val)
        elif val[0] == Types.OPEN_PARENTHESES:
            operator_stack.append(val)
        elif val[0] == Types.CLOSE_PARENTHESES:
            while len(operator_stack) > 0:
                current_operator = operator_stack[-1]
                if current_operator[0] == Types.OPERATOR:
                    output_queue.append(current_operator)
                    operator_stack.pop()
                elif current_operator[0] == Types.OPEN_PARENTHESES:
                    operator_stack.pop()
                    break
        else:
            while len(operator_stack) > 0:
                current_operator = operator_stack[-1]
                print(current_operator)
                if current_operator[0] == Types.OPEN_PARENTHESES:
                    break
                if current_operator[0] == Types.OPERATOR:
                    if OperatorRank(current_operator[1]) > OperatorRank(val[1]):
                        output_queue.append(current_operator)
                        operator_stack.pop()
                    elif OperatorRank(current_operator[1]) == OperatorRank(val[1]) and IsLeftAssociative(val[1]):
                        output_queue.append(current_operator)
                        operator_stack.pop()
                    else:
                        break
            operator_stack.append(val)

    while len(operator_stack) > 0:
        output_queue.append(operator_stack.pop())
    return output_queue

def EvaluateRPN(rpn_queue):
    while len(rpn_queue) > 1:
        found_operator = False
        for i in range(0, len(rpn_queue)):
            if rpn_queue[i][0] == Types.OPERATOR:
                found_operator = True
                break
        assert found_operator, "Couldn't find operator"
        left_operand = rpn_queue[i - 2]
        right_operand = rpn_queue[i - 1]
        operator = rpn_queue[i]
        val = None
        if operator[1] == OperatorType.ADDITION:
            val = left_operand[1] + right_operand[1]
        elif operator[1] == OperatorType.SUBTRACTION:
            val = left_operand[1] - right_operand[1]
        elif operator[1] == OperatorType.MULTIPLICATION:
            val = left_operand[1] * right_operand[1]
        elif operator[1] == OperatorType.DIVISION:
            val = left_operand[1] / right_operand[1]
        else:
            assert False, "Oh no"
        rpn_queue[i - 2] = (Types.NUMBER, val)
        rpn_queue.pop(i - 1)
        rpn_queue.pop(i - 1)
    
    assert rpn_queue[0][0] == Types.NUMBER
    return rpn_queue[0][1]

def main():
    type_list = GenerateOrderedTypeList("(10*61/3+2)/(4-1*(9/100+(132*7)/8))")
    rpn = GenerateRPN(type_list)
    value = EvaluateRPN(rpn)
    print(value)
    pass

if __name__ == "__main__":
    main()
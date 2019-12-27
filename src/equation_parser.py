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
# Operator <- parent of two children
#  

class OperatorType(Enum):
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4

class NodeType(Enum):
    OPERATOR = 1
    SUBTREE = 2
    NUMBER = 3

class Node:
    def __init__(self):
        self.type_and_data = None
        self.left = None
        self.right = None

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

def GenerateTree(type_and_data_list):
    current_node = Node()
    for i in range(0, len(type_and_data_list)):
        type_and_data = type_and_data_list[i]
        print(type_and_data)
        if type_and_data[0] == Types.NUMBER:
            node = Node()
            node.type_and_data = (NodeType.NUMBER, type_and_data[1])
            if not current_node.left:
                current_node.left = node
            else:
                current_node.right = node
                copy_node = current_node
                current_node = Node()
                current_node.left = copy_node
        elif type_and_data[0] == Types.OPERATOR:
            current_node.type_and_data = (NodeType.OPERATOR, type_and_data[1])
        elif type_and_data[0] == Types.OPEN_PARENTHESES:
            if not current_node.left:
                continue
            else:
                node = GenerateTree(type_and_data_list[i + 1:])
                current_node.right = node
                copy_node = current_node
                current_node = Node()
                current_node.left = copy_node
        elif type_and_data[0] == Types.CLOSE_PARENTHESES:
            return current_node

    return current_node

def main():
    val = GenerateOrderedTypeList("(1+2)/(4*(9))")
    temp = GenerateTree(val)
    pass

if __name__ == "__main__":
    main()
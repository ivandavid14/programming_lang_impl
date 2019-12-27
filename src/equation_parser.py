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
    
    def IsEmpty(self):
        return self.type_and_data == None and self.left == None and self.right == None
    
    def IsFull(self):
        return self.type_and_data != None and self.left != None and self.right != None

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

# Need to write down an algorithm for this. Too difficult to just solve in my head. Need to write
# down grammar and then pseudo code to implement it. Too many cases.

# Strategy
# When we see '(' called GenerateTree on rest of range
#   If previous_node doesn't exist, set previous node equal to GenerateTreeImpl return value
#   Else set previous_node right node to GenerateTreeImpl return value
# 'previous_node' should always be a valid tree
# When we see a number, look at previous_node
#   If it doesn't exist, create a node with a number in it and make it a leaf node
#   If it does exist create new node which is right leaf of previous node
# When we see ')' return previous_node

def GenerateTreeImpl(type_and_data_list):
    previous_node = None
    for i in range(0, len(type_and_data_list)):
        type_and_data = type_and_data_list[i]
        if type_and_data[0] == Types.NUMBER:
            node = Node()
            node.type_and_data = (NodeType.NUMBER, type_and_data[1])
            if previous_node:
                previous_node.right = node
                new_node = Node()
                new_node.left = previous_node
                previous_node = new_node
            else:
                previous_node = Node()
                previous_node.left = node
        elif type_and_data[0] == Types.OPERATOR:
            node = Node()
            node.type_and_data = (NodeType.OPERATOR, type_and_data[1])
            node.left = previous_node
            previous_node = node
        elif type_and_data[0] == Types.OPEN_PARENTHESES:
            node = GenerateTree(type_and_data_list[i + 1:])
            if previous_node:
                previous_node.right = node
            else:
                previous_node = node
        # BECAUSE WE ARE RETURNING, WE NEED TO KNOW WHERE WE WERE PREVIOUSLY
        # SO WE DON'T REPEAT THE COMPUTATION
        elif type_and_data[0] == Types.CLOSE_PARENTHESES:
            return previous_node

    return previous_node

def _traverseTreeImpl(root, level_list, current_level):
    if current_level in level_list:
        level_list[current_level].append(root.type_and_data)
    else:
        level_list[current_level] = [root.type_and_data]
    if root.left:
        _traverseTreeImpl(root.left, level_list, current_level + 1)
    if root.right:
        _traverseTreeImpl(root.right, level_list, current_level + 1)

def TraverseTree(root):
    level_list = {}
    if root:
        _traverseTreeImpl(root, level_list, 0)
    return level_list

def RenderTree(level_list):
    for i in range(0, len(level_list)):
        print("Level: {}. List: {}".format(i, level_list[i]))

def main():
    val = GenerateOrderedTypeList("(1+2)/(4*(9))")
    temp = GenerateTreeImpl(val)
    level_list = TraverseTree(temp)
    RenderTree(level_list)
    pass

if __name__ == "__main__":
    main()
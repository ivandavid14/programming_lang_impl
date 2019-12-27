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

class OperatorType(Enum):
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4

class NodeType(Enum):
    OPERATOR = 1
    SUBTREE = 2
    NUMBER = 3

class NodeTypeAndData:
    def __init__(self, node_type, node_data = None):
        self.node_type = node_type
        self.node_data = node_data

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

def GenerateTree(line):
    open_parentheses_count = 0
    valid_types = {Types.NUMBER, Types.OPEN_PARENTHESES}
    current_type = None
    current_number = None

    current_node = None
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
        
        if examined_type in valid_types:
            if examined_type == Types.NUMBER:
                # add to number
                if not current_number:
                    current_number = char
                else:
                    current_number = current_number + char
                # state transition
                valid_types = {Types.OPERATOR, Types.Number}
                if open_parentheses_count != 0:
                    valid_types.add(Types.CLOSE_PARENTHESES)
            elif examined_type == Types.OPEN_PARENTHESES:
                open_parentheses_count += 1
                valid_types = {Types.NUMBER, Types.OPEN_PARENTHESES}
            elif examined_type == Types.CLOSE_PARENTHESES:
                open_parentheses_count -= 1
                valid_types = {Types.NUMBER, Types.OPERATOR, TYPES.CLOSE_PARENTHESES}
            elif examined_type == Types.OPERATOR:
                operator_type = None
                if char == '+':
                    operator_type = OperatorType.ADDITION
                elif char == '-':
                    operator_type = OperatorType.SUBTRACTION
                elif char == '*':
                    operator_type = OperatorType.MULTIPLICATION
                else:
                    operator_type = OperatorType.DIVISION
                    
                current_number = None
                valid_types = {Types.NUMBER, Types.OPEN_PARENTHESES}
        else:
            raise ValueError("Unexpected type :{}. Valid types: {}", examined_type, valid_types)

class ExpectedType(Enum):
    NUMBER = 1
    NUMBER_OR_OPERATOR = 2

class ParenthesesType(Enum):
    OPEN = 1
    CLOSE = 2

def GetParenthesesPairs(line):
    pairs = []
    open_count = 0
    close_count = 0
    for i in range(0, len(line)):
        if line[i] == '(':
            pairs.append((i, ParenthesesType.OPEN))
            open_count = open_count + 1
        elif line [i] == ')':
            pairs.append((i, ParenthesesType.CLOSE))
            close_count = close_count + 1
    if open_count != close_count:
        raise ValueError("open count {} != close count {}".format(open_count, close_count))

    if (open_count == 0):
        return []

    retval = []
    while len(pairs) > 0:
        found_match = False
        for i in range(0, len(pairs) - 1):
            if pairs[i][1] == ParenthesesType.OPEN and pairs[i + 1][1] == ParenthesesType.CLOSE:
                retval.append((pairs[i][0], pairs[i + 1][0]))
                del pairs[i + 1]
                del pairs[i]
                found_match = True
                break
        if not found_match:
            raise ValueError("Unbalanced Parentheses")

    return retval


def ParseStatement(line):
    expected_type = ExpectedType.NUMBER
    current_number = None
    number_list = []
    operator_list = []
    for i in range(0, len(line)):
        current_char = line[i]
        if expected_type == ExpectedType.NUMBER:
            if current_char.isnumeric():
                current_number = current_char
                expected_type = ExpectedType.NUMBER_OR_OPERATOR
            else:
                print("ERROR, char {} at pos {} not a number".format(current_char, i))
                exit()
        elif expected_type == ExpectedType.NUMBER_OR_OPERATOR:
            if current_char.isnumeric():
                current_number += current_char
            else:
                if current_char in ['+', '-', '/', '*']:
                    number_list.append(current_number)
                    current_number = None
                    expected_type = ExpectedType.NUMBER
                    operator_list.append(current_char)
                else:
                    print("ERROR, char {} at pos {} not a number".format(current_char, i))
                    exit()
    if (current_number):
        number_list.append(current_number)

    for i in range(0, len(number_list)):
        number_list[i] = int(number_list[i])

    # find all divisions
    while '/' in operator_list:
        index = operator_list.index("/")
        number_list[index] = number_list[index] / number_list[index + 1]
        del number_list[index + 1]
        del operator_list[index]

    # find all multiplications
    while '*' in operator_list:
        index = operator_list.index("*")
        number_list[index] = number_list[index] * number_list[index + 1]
        del number_list[index + 1]
        del operator_list[index]

    current_value = number_list[0]
    for i in range(0, len(operator_list)):
        if operator_list[i] == '+':
            current_value += number_list[i + 1]
        elif operator_list[i] == '-':
            current_value -= number_list[i + 1]
    return current_value

def ParseLineWithParentheses(line):
    stripped_line = ''.join(line.strip())
    if len(stripped_line) == 0:
        print("Line of length 0 not allowed")
        exit()
    pairs = GetParenthesesPairs(stripped_line)
    retval = 0
    for pair in pairs:
        retval += ParseStatement(stripped_line[pair[0] + 1 : pair[1]])
    return retval

def main():
    print(ParseLineWithParentheses("(1+2)*(4*6)"))
    pass

if __name__ == "__main__":
    main()
'''SPACE = "Space"
OPERAND = "Operand"
OPERATOR = "Operator"
ERROR = "Error"
OPEN_BRACKET = "Open bracket"
CLOSE_BRACKET = "Close bracket"
FUNCTION_LIST = ["sqrt", "sin"]
CONSTANT_LIST = ['e', 'n', 'p'] # e, pi, phi
LETTER = "Letter"

# You should not create an instance of this class.
class Function:
    def __init__(self, function_name):
        self.name = function_name
        self.num_of_arguments = 1
        self.param_list = []
    
    def action(self):
        pass

class Sqrt(Function):
    def __init__(self):
        Function.__init__(self, "sqrt")
        self.num_of_arguments = 1
    def action(self):
        if self.num_of_arguments != 1:
            raise ArithmeticError("Invalid amount of argument. Must be 1.")
        elif self.param_list[0] < 0:
            raise ArithmeticError("We currently not supporting i.")
        elif len(self.param_list) == 0:
            raise ArithmeticError("No parameter found.")
        else:
            return self.param_list[0] ** (1/2)



class Calculator:
    def __init__(self):
        self.operands = []
        self.operators = []
        self.functions = []

    def isWhat(self, input, flag = None):
        try:
            placeholder = int(input)
        except ValueError:
            if input in ['+', '-', '*', '/']:
                return OPERATOR
            elif input == '(':
                return OPEN_BRACKET
            elif input == ')':
                return CLOSE_BRACKET
            else:
                # Save the possible functions here.
                for iter in FUNCTION_LIST:
                    if input == iter[0] and flag == None:
                        self.functions.append(iter)
                # Add iterate through constant list here
                if len(self.functions) > 0:
                    return LETTER
        else:
            return OPERAND
    
    def getPrecedence(self, operator):
        res = 0
        if operator == '+' or operator == '-':
            res = 1
        elif operator == '*' or operator == '/':
            res = 2
        elif operator == '^':
            res = 3
        else:
            res = -1
        return res
    
    def compute(self, first, second, operator):
        res = 0
        if operator == '+':
            res = first + second
        elif operator == '-':
            res = first - second
        elif operator == '*':
            res = first * second
        elif operator == '/':
            res = first / second
        elif operator == '^':
            res = first ** second

        return res

    def process(self):
        first = self.operands.pop()
        operator = self.operators.pop()
        second = self.operands.pop()
        self.operands.append(self.compute(first, second, operator))

# This is the only function that should create an instance of Calculator.

def calculate(expression):
    
    c = Calculator()
    
    ex_index = 0

    while ex_index < len(expression):
        char = expression[ex_index]
        what_is_char = c.isWhat(char)
        if char == ' ':
            continue
        elif what_is_char == OPERAND:
            c.operands.append(int(char))
        elif what_is_char == OPERATOR:
            if len(c.operators) == 0:
                c.operators.append(char)
            elif c.getPrecedence(char) > c.getPrecedence(c.operators[len(c.operators) - 1]):
                c.operators.append(char)
            else:
                while c.getPrecedence(char) <= c.getPrecedence(c.operators[len(c.operators) - 1]):
                    c.process()
                    if len(c.operators) == 0:
                        break

        elif what_is_char == OPEN_BRACKET:
            c.operators.append(char)
        elif what_is_char == CLOSE_BRACKET:
            while c.operators[len(c.operators) - 1] != '(':
                c.process()
                if len(c.operators) == 0:
                    break
            c.operators.pop()
            # If those expression are in a function, then base on what function, it'll append the parameter.
            if c.operators[len(c.operators) - 1] in FUNCTION_LIST:
                if c.operators[len(c.operators) - 1] == "sqrt":
                    function = Sqrt()
                    function.param_list.append(c.operands[len(c.operands) - 1])
                
                c.operands.append(function.action())
                c.operators.pop()
        # Either function or constant. For now, only check for function.
        elif what_is_char == LETTER:
            ex_index += 1
            func_iter = 1
            while (c.isWhat(expression[ex_index], 0) == LETTER):
                for i in c.functions:
                    try:
                        # If one character in the function i is different from the current "function" inputted, then remove it.
                        if expression[ex_index] != i[func_iter]:
                            c.functions.remove(i)
                    # If the function i length is not same as the current "function", then remove it.
                    except IndexError:
                        c.functions.remove(i)
                ex_index += 1
                func_iter += 1
            # If no function found.
            if len(c.functions) == 0:
                raise ArithmeticError("Odd symbol detected: " + char)
            else:
                c.operators.append(c.functions[0])
                



        ex_index += 1
            

    
    while len(c.operators) != 0:
        c.process()

    return c.operands[0]'''

from math import *
import ast
def calculate(expression):
    safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 
                 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 
                 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 
                 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 
                 'tan', 'tanh']
    safe_dict = dict([(k, locals().get(k, None)) for k in safe_list])
    answer = "" 
    try:
        answer = eval(expression, {"__builtins__":None}, safe_dict)
        answer = str(answer)
    except ZeroDivisionError as zde:
        answer = "Infinity/Undefined"
    except Exception:
        answer = "Error"
    return answer
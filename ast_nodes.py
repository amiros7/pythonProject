class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class FunctionDefinition(ASTNode):
    def __init__(self, name, arguments, body):
        self.name = name
        self.arguments = arguments
        self.body = body

class LambdaExpression(ASTNode):
    def __init__(self, arguments, body):
        self.arguments = arguments
        self.body = body

class FunctionApplication(ASTNode):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOperation(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class TernaryOperation(ASTNode):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name
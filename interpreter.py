from ast_nodes import *


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.enclosing:
            return self.enclosing.get(name)
        raise RuntimeError(f"Undefined variable '{name}'")


class Function:
    def __init__(self, declaration, env):
        self.declaration = declaration
        self.env = env

    def call(self, interpreter, arguments):
        environment = Environment(self.env)
        for i, param in enumerate(self.declaration.arguments):
            environment.define(param, arguments[i])
        return interpreter.evaluate(self.declaration.body, environment)


class Interpreter:
    def __init__(self):
        self.global_env = Environment()

    def interpret(self, program):
        result = None
        for statement in program.statements:
            result = self.evaluate(statement, self.global_env)
        return result

    def evaluate(self, node, env):
        if isinstance(node, Program):
            return self.interpret(node)
        elif isinstance(node, FunctionDefinition):
            function = Function(node, env)
            env.define(node.name, function)
        elif isinstance(node, LambdaExpression):
            return Function(node, env)
        elif isinstance(node, FunctionApplication):
            function = self.evaluate(node.function, env)
            arguments = [self.evaluate(arg, env) for arg in node.arguments]
            if not isinstance(function, Function):
                raise RuntimeError(f"Can only call functions and classes.")
            return function.call(self, arguments)
        elif isinstance(node, BinaryOperation):
            left = self.evaluate(node.left, env)
            right = self.evaluate(node.right, env)
            return self.apply_operator(node.operator, left, right)
        elif isinstance(node, UnaryOperation):
            operand = self.evaluate(node.operand, env)
            return self.apply_unary_operator(node.operator, operand)
        elif isinstance(node, TernaryOperation):
            condition = self.evaluate(node.condition, env)
            if condition:
                return self.evaluate(node.true_branch, env)
            else:
                return self.evaluate(node.false_branch, env)
        elif isinstance(node, Literal):
            return node.value
        elif isinstance(node, Identifier):
            return env.get(node.name)
        raise RuntimeError(f"Unexpected node type: {type(node)}")

    def apply_operator(self, operator, left, right):
        if not (isinstance(left, (int, bool)) and isinstance(right, (int, bool))):
            raise TypeError(operator, type(left).__name__, type(right).__name__)

        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left // right
        elif operator == '%':
            return left % right
        elif operator == '==':
            return left == right
        elif operator == '!=':
            return left != right
        elif operator == '<':
            return left < right
        elif operator == '>':
            return left > right
        elif operator == '<=':
            return left <= right
        elif operator == '>=':
            return left >= right
        elif operator == '&&':
            return left and right
        elif operator == '||':
            return left or right
        raise RuntimeError(f"Unknown operator: {operator}")

    def apply_unary_operator(self, operator, operand):
        if not isinstance(operand, bool):
            raise TypeError(operator, type(operand).__name__)

        if operator == '!':
            return not operand
        raise RuntimeError(f"Unknown unary operator: {operator}")


class InterpreterError(Exception):
    pass


class TypeError(InterpreterError):
    def __init__(self, operation, *types):
        self.operation = operation
        self.types = types
        super().__init__(f"TypeError: Cannot perform '{operation}' on types {', '.join(str(t) for t in types)}")


class RuntimeError(InterpreterError):
    def __init__(self, message):
        super().__init__(f"RuntimeError: {message}")
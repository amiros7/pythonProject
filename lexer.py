from ast_nodes import *

class ParseError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message

    def __str__(self):
        if self.token.type == 'EOF':
            return f"[line {self.token.line}] Error at end: {self.message}"
        return f"[line {self.token.line}] Error at '{self.token.value}': {self.message}"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        if self.match('DEFUN'):
            return self.parse_function_definition()
        else:
            return self.parse_expression()

    def parse_function_definition(self):
        self.consume('LBRACE', "Expect '{' after 'Defun'.")
        self.consume('STRING', "Expect function name.")
        self.consume('COLON', "Expect ':' after function name.")
        name = self.consume('STRING', "Expect function name.").value
        self.consume('COMMA', "Expect ',' after function name.")
        self.consume('STRING', "Expect 'arguments'.")
        self.consume('COLON', "Expect ':' after 'arguments'.")
        self.consume('LPAREN', "Expect '(' before argument list.")
        arguments = self.parse_argument_list()
        self.consume('RPAREN', "Expect ')' after argument list.")
        self.consume('RBRACE', "Expect '}' after function definition.")
        body = self.parse_expression()
        return FunctionDefinition(name, arguments, body)

    def parse_argument_list(self):
        arguments = []
        if not self.check('RPAREN'):
            arguments.append(self.consume('IDENTIFIER', "Expect argument name.").value)
            while self.match('COMMA'):
                arguments.append(self.consume('IDENTIFIER', "Expect argument name.").value)
        return arguments

    def parse_expression(self):
        return self.parse_ternary()

    def parse_ternary(self):
        expr = self.parse_or()
        if self.match('QUESTION'):
            true_branch = self.parse_expression()
            self.consume('COLON', "Expect ':' in ternary expression.")
            false_branch = self.parse_expression()
            expr = TernaryOperation(expr, true_branch, false_branch)
        return expr

    def parse_or(self):
        expr = self.parse_and()
        while self.match('LOGICAL') and self.previous().value == '||':
            right = self.parse_and()
            expr = BinaryOperation(expr, '||', right)
        return expr

    def parse_and(self):
        expr = self.parse_equality()
        while self.match('LOGICAL') and self.previous().value == '&&':
            right = self.parse_equality()
            expr = BinaryOperation(expr, '&&', right)
        return expr

    def parse_equality(self):
        expr = self.parse_comparison()
        while self.match('OPERATOR') and self.previous().value in ['==', '!=']:
            operator = self.previous().value
            right = self.parse_comparison()
            expr = BinaryOperation(expr, operator, right)
        return expr

    def parse_comparison(self):
        expr = self.parse_term()
        while self.match('OPERATOR') and self.previous().value in ['<', '>', '<=', '>=']:
            operator = self.previous().value
            right = self.parse_term()
            expr = BinaryOperation(expr, operator, right)
        return expr

    def parse_term(self):
        expr = self.parse_factor()
        while self.match('OPERATOR') and self.previous().value in ['+', '-']:
            operator = self.previous().value
            right = self.parse_factor()
            expr = BinaryOperation(expr, operator, right)
        return expr

    def parse_factor(self):
        expr = self.parse_unary()
        while self.match('OPERATOR') and self.previous().value in ['*', '/', '%']:
            operator = self.previous().value
            right = self.parse_unary()
            expr = BinaryOperation(expr, operator, right)
        return expr

    def parse_unary(self):
        if self.match('LOGICAL') and self.previous().value == '!':
            operator = self.previous().value
            right = self.parse_unary()
            return UnaryOperation(operator, right)
        return self.parse_primary()

    def parse_primary(self):
        if self.match('INTEGER'):
            return Literal(int(self.previous().value))
        if self.match('BOOLEAN'):
            return Literal(self.previous().value == 'True')
        if self.match('IDENTIFIER'):
            name = self.previous().value
            if self.match('LPAREN'):
                arguments = self.parse_arguments()
                self.consume('RPAREN', "Expect ')' after arguments.")
                return FunctionApplication(Identifier(name), arguments)
            return Identifier(name)
        if self.match('LPAREN'):
            expr = self.parse_expression()
            self.consume('RPAREN', "Expect ')' after expression.")
            return expr
        if self.match('LAMBD'):
            arguments = [self.consume('IDENTIFIER', "Expect parameter name.").value]
            self.consume('DOT', "Expect '.' after parameter name.")
            body = self.parse_expression()
            return LambdaExpression(arguments, body)
        raise self.error(self.peek(), "Expect expression.")

    def parse_arguments(self):
        arguments = []
        if not self.check('RPAREN'):
            arguments.append(self.parse_expression())
            while self.match('COMMA'):
                arguments.append(self.parse_expression())
        return arguments

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == 'EOF'

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token, message):
        return ParseError(token, message)
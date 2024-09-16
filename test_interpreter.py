import unittest
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def evaluate(self, source):
        lexer = Lexer()
        tokens = list(lexer.tokenize(source))
        parser = Parser(tokens)
        program = parser.parse()
        return self.interpreter.interpret(program)

    def test_arithmetic(self):
        self.assertEqual(self.evaluate("(3 + 4) * (2 - 1)"), 7)
        self.assertEqual(self.evaluate("10 / 3"), 3)
        self.assertEqual(self.evaluate("10 % 3"), 1)

    def test_boolean_operations(self):
        self.assertEqual(self.evaluate("True && False"), False)
        self.assertEqual(self.evaluate("True || False"), True)
        self.assertEqual(self.evaluate("!True"), False)
        self.assertEqual(self.evaluate("(True && False) || (True && True)"), True)

    def test_comparisons(self):
        self.assertTrue(self.evaluate("5 > 3"))
        self.assertFalse(self.evaluate("5 < 3"))
        self.assertTrue(self.evaluate("5 >= 5"))
        self.assertTrue(self.evaluate("3 <= 5"))
        self.assertTrue(self.evaluate("5 == 5"))
        self.assertTrue(self.evaluate("5 != 3"))

    def test_function_definition_and_call(self):
        source = """
        Defun {'name': 'add', 'arguments': (x, y)}
        x + y
        add(3, 4)
        """
        self.assertEqual(self.evaluate(source), 7)

    def test_recursive_function(self):
        source = """
        Defun {'name': 'factorial', 'arguments': (n,)}
        (n == 0) || (n == 1) ? 1 : n * factorial(n - 1)
        factorial(5)
        """
        self.assertEqual(self.evaluate(source), 120)

    def test_lambda_expression(self):
        source = """
        (Lambd x. x * x)(5)
        """
        self.assertEqual(self.evaluate(source), 25)

    def test_higher_order_function(self):
        source = """
        Defun {'name': 'apply', 'arguments': (f, x)}
        f(x)
        apply(Lambd x. x * x, 5)
        """
        self.assertEqual(self.evaluate(source), 25)

    def test_closure(self):
        source = """
        Defun {'name': 'make_adder', 'arguments': (n,)}
        Lambd x. x + n

        Defun {'name': 'add5', 'arguments': ()}
        make_adder(5)

        add5()(10)
        """
        self.assertEqual(self.evaluate(source), 15)


if __name__ == '__main__':
    unittest.main()
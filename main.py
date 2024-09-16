from lexer import Lexer
from parser import Parser, ParseError
from interpreter import Interpreter, InterpreterError

def run_file(filename):
    with open(filename, 'r') as file:
        source = file.read()
    run(source)

def run(source):
    lexer = Lexer()
    tokens = list(lexer.tokenize(source))
    parser = Parser(tokens)
    try:
        program = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(program)
        if result is not None:
            print(result)
    except ParseError as error:
        print(error)
    except InterpreterError as error:
        print(error)

def repl():
    interpreter = Interpreter()
    while True:
        try:
            line = input("λ> ")
            if line.lower() in ['exit', 'quit']:
                break
            run(line)
        except KeyboardInterrupt:
            print("\nUse 'exit' or 'quit' to exit the REPL.")
        except Exception as error:
            print(f"An unexpected error occurred: {error}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        print("Lambda Interpreter REPL")
        print("Type 'exit' or 'quit' to exit")
        repl()
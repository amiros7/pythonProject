from functools import reduce

# 1. Fibonacci sequence generator using a single lambda expression
fib = lambda n: [0] if n == 1 else [0, 1] if n == 2 else (lambda f: f(f, n))((lambda f, n: lambda x: f(f, n-1) + [x[-1] + x[-2]] if len(x) < n else x)([0, 1]))

# 2. Shortest string concatenation program using lambda
concat_strings = lambda strings: (lambda f: f(f, strings, ""))((lambda f, lst, acc: acc if not lst else f(f, lst[1:], acc + " " + lst[0] if acc else lst[0])))

# 3. Cumulative sum of squares of even numbers using nested lambda expressions
cumulative_sum_squares = lambda lists: (lambda f: f(f, lists, []))((lambda f, lst, acc: acc if not lst else f(f, lst[1:], acc + [(lambda x: sum(map(lambda y: y**2, filter(lambda z: z % 2 == 0, x))))(lst[0])])))

# 4. Higher-order function for cumulative operations
def cumulative_op(op):
    return lambda seq: (lambda f: f(f, seq, None))((lambda f, s, acc: acc if not s else f(f, s[1:], op(acc, s[0]) if acc is not None else s[0])))

factorial = cumulative_op(lambda x, y: x * y)
exponentiation = lambda base: cumulative_op(lambda x, y: x ** y)([base] + [2] * (base - 1))

# 5. One-line program using filter, map, and reduce
one_line_program = lambda nums: reduce(lambda x, y: x + y, map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))

# 6. Palindrome counter
palindrome_counter = lambda lists: list(map(lambda sublist: reduce(lambda count, s: count + (s == s[::-1]), sublist, 0), lists))

# 7. Lazy evaluation explanation
def generate_values():
    print('Generating values...')
    yield 1
    yield 2
    yield 3

def square(x):
    print(f'Squaring {x}')
    return x * x

print('Eager evaluation:')
values = list(generate_values())
squared_values = [square(x) for x in values]
print(squared_values)

print('\nLazy evaluation:')
squared_values = [square(x) for x in generate_values()]
print(squared_values)

# 8. Prime number filter
prime_filter = lambda nums: sorted(filter(lambda n: n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1)), nums), reverse=True)

# Test the functions
if __name__ == "__main__":
    print("1. Fibonacci:", fib(10))
    print("2. Concat strings:", concat_strings(["Hello", "world", "from", "lambda"]))
    print("3. Cumulative sum of squares:", cumulative_sum_squares([[1, 2, 3, 4], [5, 6, 7, 8]]))
    print("4. Factorial of 5:", factorial([1, 2, 3, 4, 5]))
    print("   Exponentiation 2^3:", exponentiation(2)([1, 2, 3]))
    print("5. One-line program result:", one_line_program([1, 2, 3, 4, 5, 6]))
    print("6. Palindrome counter:", palindrome_counter([["racecar", "hello", "deified"], ["python", "lambda"]]))
    print("8. Prime numbers:", prime_filter([10, 7, 4, 3, 2, 13, 15, 23]))
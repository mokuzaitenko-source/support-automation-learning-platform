"""
ACA UNIFIED APPLICATION - ALL-IN-ONE PLATFORM
==============================================

Complete integrated application combining:
✓ GUI & CLI interfaces
✓ Code execution with sandbox
✓ Copilot tools (run, read, explain)
✓ Code analysis & helpers (lint, analyze, suggest)
✓ Lab access (Lab1, Lab2, Lab3)
✓ Deep learning templates
✓ External tools (VS Code, Jupyter)
✓ Safety controls & manifest logging
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, scrolledtext, ttk
from typing import Any, Dict, List

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

# Force UTF-8 output for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Project paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LAB1_DIR = os.path.join(BASE_DIR, "lab1")
LAB2_DIR = os.path.join(BASE_DIR, "lab2")
LAB3_DIR = os.path.join(BASE_DIR, "lab3")
README_PATH = os.path.join(BASE_DIR, "README.md")
ROADMAP_PATH = os.path.join(BASE_DIR, "DeepLearning_Roadmap.ipynb")
SANDBOX_DIR = os.path.join(os.path.expanduser("~"), "aca_data")
os.makedirs(SANDBOX_DIR, exist_ok=True)

# Policy settings
POLICY = {
    "aca_version": "4.2",
    "sandbox": {
        "sandbox_dir": SANDBOX_DIR,
        "code_exec": {
            "confirm_required": True,
            "timeout_seconds": 8,
            "restricted_globals": True
        }
    }
}

# Allowed builtins for sandbox
ALLOWED_BUILTINS = {
    "print": print, "len": len, "range": range,
    "min": min, "max": max, "sum": sum, "abs": abs,
    "int": int, "str": str, "float": float, "bool": bool,
    "list": list, "dict": dict, "tuple": tuple, "set": set
}

# ============================================================================
# CODE TEMPLATES
# ============================================================================

CODE_TEMPLATES = {
    "Hello World": "print('Hello, World!')",
    "Loop": "for i in range(5):\n    print(i)",
    "Function": "def add(a, b):\n    return a + b\n\nprint(add(5, 3))",
}

# Beginner-Friendly Examples
BEGINNER_EXAMPLES = {
    "1. My First Program": "# This is your first Python program!\nprint('Hello! I am learning Python!')\nprint('Python is awesome!')",
    "2. Simple Math": "# Python can do math for you\nx = 5\ny = 3\nprint(f'{x} + {y} = {x + y}')\nprint(f'{x} x {y} = {x * y}')",
    "3. Ask Your Name": "# This program asks for your name\n# Uncomment the line below to make it interactive\n# name = input('What is your name? ')\nname = 'Student'  # For now, we use this\nprint(f'Nice to meet you, {name}!')",
    "4. Count to 10": "# Let's count from 1 to 10\nfor number in range(1, 11):\n    print(f'Counting: {number}')",
    "5. Make a List": "# Lists store multiple items\nfruits = ['apple', 'banana', 'orange']\nprint('My favorite fruits:')\nfor fruit in fruits:\n    print(f'  - {fruit}')",
    "6. If Statement": "# Programs can make decisions\nage = 15\nif age >= 18:\n    print('You are an adult')\nelse:\n    print('You are still young')",
    "7. Simple Function": "# Functions are reusable code blocks\ndef greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('Alice'))\nprint(greet('Bob'))",
    "8. For Loop Practice": "# Practice using loops\ncolors = ['red', 'blue', 'green', 'yellow']\nfor color in colors:\n    print(f'I like the color {color}')",
}

# Full Python Course with Detailed Explanations
PYTHON_COURSE = {
    "Lesson 1: Welcome to Python": """'''
LESSON 1: WELCOME TO PYTHON
============================

WHAT IS PYTHON?
Python is a programming language that lets you tell a computer what to do.
It's one of the easiest programming languages to learn, which is why
millions of people use it - from beginners to professionals at Google!

WHY LEARN PYTHON?
- Easy to read and write (looks almost like English!)
- Powerful (can build websites, AI, games, robots, and more)
- Widely used in jobs (data science, web development, automation)
- Free and has a huge community to help you

YOUR FIRST PROGRAM:
The 'print()' function displays text on the screen.
'''

# This is a comment - Python ignores it (it's just for humans to read)
# Comments help explain what your code does

# Let's write our first line of code!
print('Hello, World!')  # This displays "Hello, World!" on the screen

# You can print multiple things:
print('My name is Python')
print('I was created in 1991')
print('I am fun to learn!')

# TASK: Change the text above to print your own messages!
print('\\n--- You completed Lesson 1! Move to Lesson 2! ---')
""",

    "Lesson 2: Variables - Storing Information": """'''
LESSON 2: VARIABLES - STORING INFORMATION
==========================================

WHAT ARE VARIABLES?
Variables are like labeled boxes that store information.
Instead of writing the same value over and over, we can store it
in a variable and use it whenever we need it.

RULES FOR VARIABLE NAMES:
- Use letters, numbers, and underscores (_)
- Must start with a letter or underscore
- Cannot use spaces (use underscores instead)
- Case-sensitive (Name and name are different)
'''

# Creating variables is called "assignment"
# Format: variable_name = value

name = 'Alice'          # Text is called a "string" (use quotes)
age = 25                # Numbers without decimals are "integers"
height = 5.7            # Numbers with decimals are "floats"
is_student = True       # True/False values are "booleans"

# Using variables
print('Name:', name)
print('Age:', age)
print('Height:', height, 'feet')
print('Is student:', is_student)

# Variables can change (that's why they're called "variable"!)
age = 26  # Happy birthday!
print('New age:', age)

# You can do math with variables
x = 10
y = 5
print('x + y =', x + y)        # Addition: 15
print('x - y =', x - y)        # Subtraction: 5
print('x * y =', x * y)        # Multiplication: 50
print('x / y =', x / y)        # Division: 2.0
print('x ** 2 =', x ** 2)      # Power: 100

# TASK: Create your own variables and print them!
print('\\n--- Lesson 2 complete! Try Lesson 3! ---')
""",

    "Lesson 3: Data Types Explained": """'''
LESSON 3: DATA TYPES - DIFFERENT KINDS OF DATA
==============================================

PYTHON HAS SEVERAL DATA TYPES:
1. String (str)    - Text in quotes: 'hello' or "hello"
2. Integer (int)   - Whole numbers: 42, -10, 0
3. Float (float)   - Decimal numbers: 3.14, -0.5
4. Boolean (bool)  - True or False
5. None (NoneType) - Represents "nothing" or "no value"
'''

# Strings (text)
message = 'Hello, Python!'
quote = "I can use single or double quotes"
multiline = '''I can even
span multiple
lines!'''

print('String:', message)
print('Type:', type(message))  # type() tells us what data type it is

# Integers (whole numbers)
count = 42
negative = -10
zero = 0

print('\\nInteger:', count)
print('Type:', type(count))

# Floats (decimals)
pi = 3.14159
temperature = -2.5

print('\\nFloat:', pi)
print('Type:', type(temperature))

# Booleans (True or False)
is_raining = False
is_sunny = True

print('\\nBoolean:', is_sunny)
print('Type:', type(is_sunny))

# Converting between types (called "casting")
num_string = '42'              # This is text, not a number
num_int = int(num_string)      # Convert text to integer
num_float = float(num_string)  # Convert text to float

print('\\n--- Type Conversions ---')
print('Original:', num_string, '(type:', type(num_string), ')')
print('As integer:', num_int, '(type:', type(num_int), ')')
print('As float:', num_float, '(type:', type(num_float), ')')

# String operations
first_name = 'John'
last_name = 'Doe'
full_name = first_name + ' ' + last_name  # Joining strings is "concatenation"
print('\\nFull name:', full_name)

# TASK: Try creating variables of each type!
print('\\n--- Lesson 3 complete! On to Lesson 4! ---')
""",

    "Lesson 4: User Input & String Formatting": """'''
LESSON 4: USER INPUT & STRING FORMATTING
========================================

GETTING INPUT FROM USERS:
The input() function lets users type information.
Everything from input() is a string, even if they type numbers!

STRING FORMATTING:
Python has several ways to insert variables into strings:
1. f-strings (modern, recommended) - f'Hello {name}'
2. format() method - 'Hello {}'.format(name)
3. % operator (old style) - 'Hello %s' % name
'''

# For demonstration, we'll use predefined values
# (Remove the # to make it interactive!)

# name = input('What is your name? ')
# age = input('How old are you? ')

name = 'Alice'  # Simulated input
age = '25'      # Simulated input

print('\\n--- Different ways to format strings ---')

# Method 1: f-strings (best!)
print(f'Hello, {name}! You are {age} years old.')

# Method 2: format()
print('Hello, {}! You are {} years old.'.format(name, age))

# Method 3: + concatenation
print('Hello, ' + name + '! You are ' + age + ' years old.')

# Converting input to numbers
age_number = int(age)  # Convert string to integer
next_year = age_number + 1

print(f'\\nNext year, you will be {next_year}!')

# String methods
print('\\n--- String Methods ---')
text = 'hello python world'
print('Original:', text)
print('Uppercase:', text.upper())
print('Titlecase:', text.title())
print('Replace:', text.replace('python', 'coding'))
print('Split into words:', text.split())

# INTERACTIVE CHALLENGE:
# Uncomment these lines to make it interactive:
# print('\\n--- Interactive Challenge ---')
# fav_color = input('What is your favorite color? ')
# fav_number = input('What is your favorite number? ')
# print(f'Cool! {fav_color} is a great color!')
# print(f'And {fav_number} is an interesting number!')

print('\\n--- Lesson 4 complete! Try Lesson 5! ---')
""",

    "Lesson 5: Making Decisions (If/Else)": """'''
LESSON 5: MAKING DECISIONS WITH IF/ELSE
========================================

CONDITIONAL STATEMENTS:
Programs need to make decisions! The if statement lets your code
do different things based on whether something is True or False.

COMPARISON OPERATORS:
==  Equal to (note: double = for comparison!)
!=  Not equal to
>   Greater than
<   Less than
>=  Greater than or equal to
<=  Less than or equal to

LOGICAL OPERATORS:
and  Both conditions must be True
or   At least one condition must be True
not  Reverses True/False
'''

# Simple if statement
age = 18
print('Age:', age)

if age >= 18:
    print('You can vote!')  # This runs if condition is True
    
# If-else: do one thing or another
temperature = 75
print('\\nTemperature:', temperature, 'degrees')

if temperature > 80:
    print('It''s hot! Stay hydrated!')
else:
    print('It''s nice weather!')

# If-elif-else: multiple conditions
score = 85
print('\\nYour score:', score)

if score >= 90:
    print('Grade: A - Excellent!')
elif score >= 80:
    print('Grade: B - Great job!')
elif score >= 70:
    print('Grade: C - Good!')
elif score >= 60:
    print('Grade: D - Need improvement')
else:
    print('Grade: F - Study harder!')

# Multiple conditions with and/or
age = 20
has_license = True

print('\\n--- Checking driving eligibility ---')
if age >= 16 and has_license:
    print('You can drive!')
elif age >= 16 and not has_license:
    print('You need to get a license first')
else:
    print('You are too young to drive')

# Nested if statements
is_weekend = True
is_raining = False

print('\\n--- Weekend plans ---')
if is_weekend:
    if is_raining:
        print('Stay inside and watch movies')
    else:
        print('Go outside and play!')
else:
    print('Time for school/work')

# Ternary operator (short if-else)
number = 10
result = 'Even' if number % 2 == 0 else 'Odd'
print(f'\\n{number} is {result}')

# PRACTICE CHALLENGE:
print('\\n--- Practice ---')
your_age = 16  # Try changing this number!
print(f'Your age: {your_age}')

if your_age >= 21:
    print('You can drink alcohol (in USA)')
elif your_age >= 18:
    print('You are an adult!')
elif your_age >= 16:
    print('You can drive (with permit)')
elif your_age >= 13:
    print('You are a teenager!')
else:
    print('You are a child!')

print('\\n--- Lesson 5 complete! Try Lesson 6! ---')
""",

    "Lesson 6: Loops - Repeating Actions": """'''
LESSON 6: LOOPS - REPEATING ACTIONS
====================================

WHY USE LOOPS?
Instead of writing the same code over and over, loops let you
repeat actions automatically. Python has two types of loops:

1. FOR LOOPS: When you know how many times to repeat
2. WHILE LOOPS: Keep going until a condition becomes False

THE RANGE() FUNCTION:
range(5)       -> 0, 1, 2, 3, 4
range(1, 6)    -> 1, 2, 3, 4, 5
range(0, 10, 2) -> 0, 2, 4, 6, 8 (step by 2)
'''

# FOR LOOP: Count from 1 to 5
print('--- Counting with for loop ---')
for i in range(1, 6):
    print(f'Count: {i}')

# FOR LOOP: Loop through a list
print('\\n--- Looping through colors ---')
colors = ['red', 'green', 'blue', 'yellow']
for color in colors:
    print(f'I like {color}')

# ENUMERATE: Get both index and value
print('\\n--- Using enumerate (index + value) ---')
fruits = ['apple', 'banana', 'cherry']
for index, fruit in enumerate(fruits):
    print(f'{index + 1}. {fruit}')

# WHILE LOOP: Keep going while condition is True
print('\\n--- Countdown with while loop ---')
countdown = 5
while countdown > 0:
    print(f'{countdown}...')
    countdown = countdown - 1  # Same as: countdown -= 1
print('Blast off! 🚀')

# BREAK: Exit the loop early
print('\\n--- Using break ---')
for number in range(1, 11):
    if number == 5:
        print('Found 5! Stopping loop.')
        break
    print(number)

# CONTINUE: Skip to next iteration
print('\\n--- Using continue (skip even numbers) ---')
for number in range(1, 11):
    if number % 2 == 0:  # If even
        continue  # Skip the rest and go to next number
    print(number)  # Only odd numbers will print

# NESTED LOOPS: Loop inside a loop
print('\\n--- Multiplication table ---')
for i in range(1, 4):
    for j in range(1, 4):
        print(f'{i} x {j} = {i * j}', end='  ')
    print()  # New line after each row

# PRACTICAL EXAMPLE: Sum of numbers
print('\\n--- Calculate sum ---')
total = 0
for number in range(1, 6):
    total += number  # Same as: total = total + number
    print(f'Adding {number}, total is now {total}')
print(f'Final sum: {total}')

# CHALLENGE: Print a pattern
print('\\n--- Star pattern ---')
for i in range(1, 6):
    print('*' * i)

print('\\n--- Lesson 6 complete! Try Lesson 7! ---')
""",

    "Lesson 7: Lists - Storing Multiple Items": """'''
LESSON 7: LISTS - STORING MULTIPLE ITEMS
=========================================

WHAT ARE LISTS?
Lists are like containers that can hold multiple items.
Think of a shopping list - it can have many items in order.

LIST FEATURES:
- Ordered: Items stay in the order you add them
- Changeable: You can add, remove, or modify items
- Allow duplicates: Can have the same item multiple times
- Mixed types: Can hold different data types together
'''

# Creating lists
print('--- Creating Lists ---')
fruits = ['apple', 'banana', 'cherry']
numbers = [1, 2, 3, 4, 5]
mixed = ['hello', 42, 3.14, True]  # Different types!
empty = []  # Empty list

print('Fruits:', fruits)
print('Numbers:', numbers)
print('Mixed:', mixed)

# Accessing items (indexing starts at 0!)
print('\\n--- Accessing Items ---')
print('First fruit:', fruits[0])   # apple
print('Second fruit:', fruits[1])  # banana
print('Last fruit:', fruits[-1])   # cherry (negative index from end)

# Slicing: Get multiple items
print('\\n--- Slicing ---')
print('First two fruits:', fruits[0:2])  # apple, banana
print('From second onward:', fruits[1:])  # banana, cherry
print('Last two:', fruits[-2:])  # banana, cherry

# Modifying lists
print('\\n--- Modifying Lists ---')
fruits[1] = 'blueberry'  # Change banana to blueberry
print('After change:', fruits)

# Adding items
fruits.append('orange')  # Add to end
print('After append:', fruits)

fruits.insert(1, 'mango')  # Insert at position 1
print('After insert:', fruits)

# Removing items
fruits.remove('apple')  # Remove specific item
print('After remove:', fruits)

popped = fruits.pop()  # Remove and return last item
print('Popped item:', popped)
print('After pop:', fruits)

# List methods
print('\\n--- List Methods ---')
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print('Original:', numbers)
print('Length:', len(numbers))
print('Max:', max(numbers))
print('Min:', min(numbers))
print('Sum:', sum(numbers))
print('Count of 1s:', numbers.count(1))

numbers.sort()  # Sort in place
print('Sorted:', numbers)

numbers.reverse()  # Reverse in place
print('Reversed:', numbers)

# List comprehension (advanced way to create lists)
print('\\n--- List Comprehension ---')
squares = [x**2 for x in range(1, 6)]
print('Squares:', squares)

evens = [x for x in range(1, 11) if x % 2 == 0]
print('Even numbers:', evens)

# Combining lists
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = list1 + list2
print('\\nCombined:', combined)

# Checking membership
print('\\n--- Checking Items ---')
fruits = ['apple', 'banana', 'cherry']
print('Is apple in list?', 'apple' in fruits)
print('Is grape in list?', 'grape' in fruits)

# PRACTICE
print('\\n--- Practice ---')
shopping_list = []
shopping_list.append('milk')
shopping_list.append('bread')
shopping_list.append('eggs')
print('Shopping list:', shopping_list)

for index, item in enumerate(shopping_list, 1):
    print(f'{index}. {item}')

print('\\n--- Lesson 7 complete! Try Lesson 8! ---')
""",

    "Lesson 8: Dictionaries - Key-Value Pairs": """'''
LESSON 8: DICTIONARIES - KEY-VALUE PAIRS
=========================================

WHAT ARE DICTIONARIES?
Dictionaries store data in key-value pairs, like a real dictionary
where you look up a word (key) to find its meaning (value).

WHEN TO USE DICTIONARIES?
- When you need to look up values by name
- Storing related data together (like a person's information)
- JSON data from websites uses this format

FORMAT: {key: value, key: value}
'''

# Creating dictionaries
print('--- Creating Dictionaries ---')
person = {
    'name': 'Alice',
    'age': 25,
    'city': 'New York',
    'is_student': True
}
print('Person:', person)

# Accessing values
print('\\n--- Accessing Values ---')
print('Name:', person['name'])
print('Age:', person['age'])

# Safer way using get() (won't crash if key doesn't exist)
print('City:', person.get('city'))
print('Job:', person.get('job', 'Not specified'))  # Default value

# Adding/modifying values
print('\\n--- Adding/Modifying ---')
person['job'] = 'Engineer'  # Add new key
person['age'] = 26  # Modify existing key
print('Updated:', person)

# Removing items
print('\\n--- Removing Items ---')
removed = person.pop('is_student')
print('Removed:', removed)
print('After removal:', person)

# Dictionary methods
print('\\n--- Dictionary Methods ---')
print('All keys:', list(person.keys()))
print('All values:', list(person.values()))
print('All items:', list(person.items()))

# Looping through dictionary
print('\\n--- Looping Through Dictionary ---')
for key in person:
    print(f'{key}: {person[key]}')

# Better way: loop through items
print()
for key, value in person.items():
    print(f'{key} -> {value}')

# Nested dictionaries
print('\\n--- Nested Dictionaries ---')
people = {
    'person1': {'name': 'Alice', 'age': 25},
    'person2': {'name': 'Bob', 'age': 30},
    'person3': {'name': 'Charlie', 'age': 35}
}

for person_id, info in people.items():
    print(f"{person_id}: {info['name']}, age {info['age']}")

# Dictionary comprehension
print('\\n--- Dictionary Comprehension ---')
squares = {x: x**2 for x in range(1, 6)}
print('Squares:', squares)

# Practical example: Word counter
print('\\n--- Word Counter Example ---')
text = 'hello world hello python python python'
words = text.split()

word_count = {}
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

print('Word count:', word_count)

# Better way using get()
word_count2 = {}
for word in words:
    word_count2[word] = word_count2.get(word, 0) + 1
print('Word count (method 2):', word_count2)

# PRACTICE
print('\\n--- Practice: Student Grades ---')
grades = {
    'Alice': 95,
    'Bob': 87,
    'Charlie': 92,
    'Diana': 88
}

for student, grade in grades.items():
    if grade >= 90:
        status = 'Excellent!'
    elif grade >= 80:
        status = 'Good!'
    else:
        status = 'Keep trying!'
    print(f'{student}: {grade} - {status}')

print('\\n--- Lesson 8 complete! Try Lesson 9! ---')
""",

    "Lesson 9: Functions - Reusable Code": """'''
LESSON 9: FUNCTIONS - REUSABLE CODE
====================================

WHAT ARE FUNCTIONS?
Functions are reusable blocks of code that perform a specific task.
Instead of writing the same code multiple times, write it once
as a function and call it whenever you need it!

WHY USE FUNCTIONS?
- Avoid repeating code (DRY: Don't Repeat Yourself)
- Make code easier to read and maintain
- Break complex problems into smaller pieces
- Can reuse the function in different programs

FUNCTION STRUCTURE:
def function_name(parameters):
    \"\"\"Docstring explains what function does\"\"\"
    # code goes here
    return result
'''

# Simple function with no parameters
print('--- Simple Function ---')

def greet():
    \"\"\"Print a greeting message\"\"\"
    print('Hello! Welcome to Python!')

greet()  # Call the function
greet()  # Can call it multiple times!

# Function with parameters
print('\\n--- Function with Parameters ---')

def greet_person(name):
    \"\"\"Greet a specific person\"\"\"
    return f'Hello, {name}! Nice to meet you!'

message1 = greet_person('Alice')
message2 = greet_person('Bob')
print(message1)
print(message2)

# Function with multiple parameters
print('\\n--- Multiple Parameters ---')

def add_numbers(a, b):
    \"\"\"Add two numbers and return the result\"\"\"
    result = a + b
    return result

sum1 = add_numbers(5, 3)
sum2 = add_numbers(10, 20)
print(f'5 + 3 = {sum1}')
print(f'10 + 20 = {sum2}')

# Default parameters
print('\\n--- Default Parameters ---')

def greet_with_title(name, title='Mr.'):
    \"\"\"Greet with optional title\"\"\"
    return f'Hello, {title} {name}!'

print(greet_with_title('Smith'))  # Uses default title
print(greet_with_title('Johnson', 'Dr.'))  # Custom title

# Multiple return values
print('\\n--- Multiple Return Values ---')

def get_stats(numbers):
    \"\"\"Calculate min, max, and average of numbers\"\"\"
    minimum = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    return minimum, maximum, average

nums = [1, 2, 3, 4, 5]
min_val, max_val, avg_val = get_stats(nums)
print(f'Numbers: {nums}')
print(f'Min: {min_val}, Max: {max_val}, Avg: {avg_val}')

# *args: Accept any number of arguments
print('\\n--- *args (Variable Arguments) ---')

def sum_all(*numbers):
    \"\"\"Sum any number of arguments\"\"\"
    total = 0
    for num in numbers:
        total += num
    return total

print('Sum of 1,2,3:', sum_all(1, 2, 3))
print('Sum of 1,2,3,4,5:', sum_all(1, 2, 3, 4, 5))

# **kwargs: Accept keyword arguments
print('\\n--- **kwargs (Keyword Arguments) ---')

def print_info(**info):
    \"\"\"Print all keyword arguments\"\"\"
    for key, value in info.items():
        print(f'{key}: {value}')

print_info(name='Alice', age=25, city='NYC')

# Lambda functions (short anonymous functions)
print('\\n--- Lambda Functions ---')

square = lambda x: x ** 2
add = lambda x, y: x + y

print(f'Square of 5: {square(5)}')
print(f'3 + 4: {add(3, 4)}')

# Practical example: Temperature converter
print('\\n--- Practical Example: Temperature Converter ---')

def celsius_to_fahrenheit(celsius):
    \"\"\"Convert Celsius to Fahrenheit\"\"\"
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

def fahrenheit_to_celsius(fahrenheit):
    \"\"\"Convert Fahrenheit to Celsius\"\"\"
    celsius = (fahrenheit - 32) * 5/9
    return celsius

temp_c = 25
temp_f = celsius_to_fahrenheit(temp_c)
print(f'{temp_c}°C = {temp_f}°F')

temp_f2 = 77
temp_c2 = fahrenheit_to_celsius(temp_f2)
print(f'{temp_f2}°F = {temp_c2:.1f}°C')

# PRACTICE: Create a calculator
print('\\n--- Practice: Simple Calculator ---')

def calculator(num1, num2, operation):
    \"\"\"Perform basic math operations\"\"\"
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 != 0:
            return num1 / num2
        else:
            return 'Error: Division by zero!'
    else:
        return 'Error: Invalid operation!'

print('10 + 5 =', calculator(10, 5, '+'))
print('10 - 5 =', calculator(10, 5, '-'))
print('10 * 5 =', calculator(10, 5, '*'))
print('10 / 5 =', calculator(10, 5, '/'))

print('\\n--- Lesson 9 complete! Try Lesson 10! ---')
""",

    "Lesson 10: File Handling": """'''
LESSON 10: FILE HANDLING - READ & WRITE FILES
==============================================

WHY FILE HANDLING?
Programs need to save data permanently and load it later.
Files let you store data that survives after the program closes.

FILE MODES:
'r'  - Read (default)
'w'  - Write (creates new file or overwrites existing)
'a'  - Append (add to end of existing file)
'r+' - Read and write

BEST PRACTICE: Use 'with' statement
It automatically closes the file when done!
'''

# Writing to a file
print('--- Writing to a File ---')

with open('example.txt', 'w') as file:
    file.write('Hello, World!\\n')
    file.write('This is line 2\\n')
    file.write('This is line 3\\n')

print('✓ File written successfully!')

# Reading entire file
print('\\n--- Reading Entire File ---')

with open('example.txt', 'r') as file:
    content = file.read()
    print(content)

# Reading line by line
print('--- Reading Line by Line ---')

with open('example.txt', 'r') as file:
    for line_num, line in enumerate(file, 1):
        print(f'Line {line_num}: {line.strip()}')

# Reading into a list
print('\\n--- Reading into List ---')

with open('example.txt', 'r') as file:
    lines = file.readlines()
    print('All lines:', lines)

# Appending to a file
print('\\n--- Appending to File ---')

with open('example.txt', 'a') as file:
    file.write('This is an appended line\\n')
    file.write('Another appended line\\n')

print('✓ Lines appended!')

# Read updated file
with open('example.txt', 'r') as file:
    print('\\nUpdated file contents:')
    print(file.read())

# Writing a list to file
print('--- Writing List to File ---')

fruits = ['apple', 'banana', 'cherry', 'date']

with open('fruits.txt', 'w') as file:
    for fruit in fruits:
        file.write(f'{fruit}\\n')

print('✓ Fruit list written!')

# Reading list from file
with open('fruits.txt', 'r') as file:
    loaded_fruits = [line.strip() for line in file]
    print('Loaded fruits:', loaded_fruits)

# Working with CSV (Comma-Separated Values)
print('\\n--- Working with CSV ---')

# Writing CSV
with open('students.csv', 'w') as file:
    file.write('Name,Age,Grade\\n')
    file.write('Alice,20,A\\n')
    file.write('Bob,22,B\\n')
    file.write('Charlie,21,A\\n')

print('✓ CSV file created!')

# Reading and parsing CSV
with open('students.csv', 'r') as file:
    headers = file.readline().strip().split(',')
    print('\\nHeaders:', headers)
    print('\\nStudents:')
    for line in file:
        data = line.strip().split(',')
        print(f'Name: {data[0]}, Age: {data[1]}, Grade: {data[2]}')

# File exists check
import os

print('\\n--- Checking File Existence ---')
if os.path.exists('example.txt'):
    print('✓ example.txt exists!')
else:
    print('✗ example.txt does not exist')

# Error handling with files
print('\\n--- Error Handling ---')

try:
    with open('nonexistent.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print('Error: File not found!')
except Exception as e:
    print(f'An error occurred: {e}')

# PRACTICE: Log file
print('\\n--- Practice: Simple Log File ---')

import datetime

log_entries = [
    'Application started',
    'User logged in',
    'Data processed successfully',
    'User logged out'
]

with open('app.log', 'w') as log:
    for entry in log_entries:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.write(f'[{timestamp}] {entry}\\n')

print('✓ Log file created!')

with open('app.log', 'r') as log:
    print('\\nLog contents:')
    print(log.read())

print('--- Lesson 10 complete! Try Lesson 11! ---')
""",

    "Lesson 11: Error Handling": """'''
LESSON 11: ERROR HANDLING - DEALING WITH ERRORS
================================================

WHY ERROR HANDLING?
Errors (exceptions) happen! Instead of crashing, we can handle them
gracefully and keep the program running.

COMMON EXCEPTIONS:
- ZeroDivisionError: Dividing by zero
- ValueError: Wrong value type
- TypeError: Wrong data type
- FileNotFoundError: File doesn't exist
- KeyError: Dictionary key doesn't exist
- IndexError: List index out of range

STRUCTURE:
try:
    # Code that might cause an error
except ErrorType:
    # What to do if that error occurs
else:
    # Runs if NO error occurred
finally:
    # Always runs, error or not
'''

# Basic try-except
print('--- Basic Error Handling ---')

try:
    result = 10 / 0
except ZeroDivisionError:
    print('Error: Cannot divide by zero!')
    result = None

print(f'Result: {result}')

# Multiple except blocks
print('\\n--- Multiple Exception Types ---')

def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return 'Error: Division by zero!'
    except TypeError:
        return 'Error: Invalid data type!'

print('10 / 2 =', safe_divide(10, 2))
print('10 / 0 =', safe_divide(10, 0))
print("10 / 'a' =", safe_divide(10, 'a'))

# Catching all exceptions
print('\\n--- Catching Any Exception ---')

try:
    number = int('abc')  # This will cause ValueError
except Exception as e:
    print(f'An error occurred: {e}')
    print(f'Error type: {type(e).__name__}')

# else and finally
print('\\n--- else and finally ---')

try:
    number = int('42')
    print(f'Converted: {number}')
except ValueError:
    print('Conversion failed!')
else:
    print('✓ Conversion successful (else block)')
finally:
    print('✓ Cleanup code (finally block - always runs)')

# Raising exceptions
print('\\n--- Raising Exceptions ---')

def check_age(age):
    if age < 0:
        raise ValueError('Age cannot be negative!')
    elif age > 150:
        raise ValueError('Age seems unrealistic!')
    else:
        return f'Age {age} is valid'

try:
    print(check_age(25))
    print(check_age(-5))
except ValueError as e:
    print(f'Validation error: {e}')

# Custom exceptions
print('\\n--- Custom Exceptions ---')

class CustomError(Exception):
    \"\"\"Custom exception for our app\"\"\"
    pass

def process_data(data):
    if not data:
        raise CustomError('Data cannot be empty!')
    return f'Processing: {data}'

try:
    result = process_data('')
except CustomError as e:
    print(f'Custom error caught: {e}')

# Practical example: Safe input
print('\\n--- Practical: Safe Number Input ---')

def get_number(prompt, default=0):
    \"\"\"Get a number from user input with error handling\"\"\"
    try:
        # For demo, we'll use a value
        # Replace this with: value = input(prompt)
        value = '42'  # Simulated input
        return int(value)
    except ValueError:
        print(f'Invalid input! Using default: {default}')
        return default

number = get_number('Enter a number: ', default=0)
print(f'You entered: {number}')

# Error handling with files
print('\\n--- File Error Handling ---')

def read_file_safely(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f'Error: {filename} not found'
    except PermissionError:
        return f'Error: No permission to read {filename}'
    except Exception as e:
        return f'Unexpected error: {e}'

content = read_file_safely('nonexistent.txt')
print(content)

# PRACTICE: Calculator with error handling
print('\\n--- Practice: Safe Calculator ---')

def safe_calculator(num1, num2, operation):
    \"\"\"Calculator with comprehensive error handling\"\"\"
    try:
        num1 = float(num1)
        num2 = float(num2)
        
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            if num2 == 0:
                raise ZeroDivisionError('Cannot divide by zero')
            return num1 / num2
        else:
            raise ValueError(f'Invalid operation: {operation}')
    except ValueError as e:
        return f'Value error: {e}'
    except ZeroDivisionError as e:
        return f'Math error: {e}'
    except Exception as e:
        return f'Unexpected error: {e}'

print('10 + 5 =', safe_calculator('10', '5', '+'))
print('10 / 0 =', safe_calculator('10', '0', '/'))
print("'abc' + 5 =", safe_calculator('abc', '5', '+'))
print('10 % 5 =', safe_calculator('10', '5', '%'))

print('\\n--- Lesson 11 complete! Try Lesson 12! ---')
""",

    "Lesson 12: Object-Oriented Programming": """'''
LESSON 12: OBJECT-ORIENTED PROGRAMMING (OOP)
=============================================

WHAT IS OOP?
OOP is a programming paradigm that organizes code around "objects"
that contain both data (attributes) and functions (methods).

KEY CONCEPTS:
1. Class: Blueprint for creating objects
2. Object: Instance of a class
3. Attributes: Variables belonging to an object
4. Methods: Functions belonging to an object

THINK OF IT LIKE:
Class = Cookie Cutter (blueprint)
Object = Actual Cookie (instance)

WHY OOP?
- Organize complex code
- Reuse code easily
- Model real-world things
- Make code more maintainable
'''

# Creating a simple class
print('--- Simple Class ---')

class Dog:
    \"\"\"A simple dog class\"\"\"
    
    def __init__(self, name, age):
        \"\"\"Initialize dog with name and age\"\"\"
        self.name = name  # Attribute
        self.age = age    # Attribute
    
    def bark(self):
        \"\"\"Method to make dog bark\"\"\"
        return f'{self.name} says Woof!'
    
    def get_info(self):
        \"\"\"Method to get dog info\"\"\"
        return f'{self.name} is {self.age} years old'

# Creating objects (instances)
dog1 = Dog('Rex', 5)
dog2 = Dog('Buddy', 3)

print(dog1.bark())
print(dog2.bark())
print(dog1.get_info())
print(dog2.get_info())

# Class with more features
print('\\n--- Bank Account Class ---')

class BankAccount:
    \"\"\"Bank account with deposits and withdrawals\"\"\"
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []
    
    def deposit(self, amount):
        \"\"\"Add money to account\"\"\"
        if amount > 0:
            self.balance += amount
            self.transactions.append(f'+${amount}')
            return f'Deposited ${amount}. New balance: ${self.balance}'
        return 'Invalid deposit amount'
    
    def withdraw(self, amount):
        \"\"\"Remove money from account\"\"\"
        if amount > self.balance:
            return 'Insufficient funds!'
        elif amount > 0:
            self.balance -= amount
            self.transactions.append(f'-${amount}')
            return f'Withdrew ${amount}. New balance: ${self.balance}'
        return 'Invalid withdrawal amount'
    
    def get_balance(self):
        return f'{self.owner} has ${self.balance}'
    
    def get_transactions(self):
        return f'Transactions: {self.transactions}'

# Using the bank account
account = BankAccount('Alice', 1000)
print(account.get_balance())
print(account.deposit(500))
print(account.withdraw(200))
print(account.withdraw(2000))
print(account.get_balance())
print(account.get_transactions())

# Inheritance (creating subclasses)
print('\\n--- Inheritance ---')

class Animal:
    \"\"\"Base class for animals\"\"\"
    
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return 'Some sound'
    
    def info(self):
        return f'I am {self.name}'

class Cat(Animal):
    \"\"\"Cat inherits from Animal\"\"\"
    
    def speak(self):
        return f'{self.name} says Meow!'

class Bird(Animal):
    \"\"\"Bird inherits from Animal\"\"\"
    
    def speak(self):
        return f'{self.name} says Tweet!'
    
    def fly(self):
        return f'{self.name} is flying!'

cat = Cat('Whiskers')
bird = Bird('Tweety')

print(cat.info())
print(cat.speak())
print(bird.info())
print(bird.speak())
print(bird.fly())

# Magic methods (special methods)
print('\\n--- Magic Methods ---')

class Point:
    \"\"\"2D point with magic methods\"\"\"
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        \"\"\"String representation\"\"\"
        return f'Point({self.x}, {self.y})'
    
    def __add__(self, other):
        \"\"\"Add two points\"\"\"
        return Point(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        \"\"\"Check equality\"\"\"
        return self.x == other.x and self.y == other.y

p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2  # Uses __add__

print(f'p1: {p1}')  # Uses __str__
print(f'p2: {p2}')
print(f'p1 + p2 = {p3}')
print(f'p1 == p2: {p1 == p2}')  # Uses __eq__

# Properties
print('\\n--- Properties ---')

class Temperature:
    \"\"\"Temperature with Celsius/Fahrenheit conversion\"\"\"
    
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError('Temperature below absolute zero!')
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

temp = Temperature(25)
print(f'{temp.celsius}°C = {temp.fahrenheit}°F')
temp.fahrenheit = 98.6
print(f'{temp.celsius:.1f}°C = {temp.fahrenheit}°F')

# PRACTICE: Student class
print('\\n--- Practice: Student Class ---')

class Student:
    \"\"\"Student with grades\"\"\"
    
    def __init__(self, name):
        self.name = name
        self.grades = []
    
    def add_grade(self, grade):
        if 0 <= grade <= 100:
            self.grades.append(grade)
            return f'Added grade: {grade}'
        return 'Invalid grade (must be 0-100)'
    
    def get_average(self):
        if self.grades:
            return sum(self.grades) / len(self.grades)
        return 0
    
    def get_letter_grade(self):
        avg = self.get_average()
        if avg >= 90: return 'A'
        elif avg >= 80: return 'B'
        elif avg >= 70: return 'C'
        elif avg >= 60: return 'D'
        else: return 'F'
    
    def __str__(self):
        avg = self.get_average()
        letter = self.get_letter_grade()
        return f'{self.name}: Avg={avg:.1f}, Grade={letter}'

student = Student('Alice')
student.add_grade(95)
student.add_grade(87)
student.add_grade(92)
print(student)

print('\\n--- Lesson 12 complete! Try Lesson 13! ---')
""",

    "Lesson 13: Modules & Packages": """'''
LESSON 13: MODULES & PACKAGES
==============================

WHAT ARE MODULES?
A module is a file containing Python code (functions, classes, variables).
Instead of writing everything in one file, you can split code into
multiple files (modules) and import them when needed.

WHAT ARE PACKAGES?
A package is a collection of modules organized in directories.

WHY USE MODULES?
- Organize code into logical units
- Reuse code across projects
- Use code written by others (libraries)
- Keep files manageable in size

IMPORT METHODS:
1. import module
2. from module import function
3. from module import *
4. import module as alias
'''

# Importing built-in modules
print('--- Built-in Modules ---')

import math
import random
import datetime
import os

# Using math module
print('\\nMath Module:')
print(f'Pi: {math.pi}')
print(f'Square root of 16: {math.sqrt(16)}')
print(f'5 factorial: {math.factorial(5)}')
print(f'Ceiling of 4.2: {math.ceil(4.2)}')
print(f'Floor of 4.8: {math.floor(4.8)}')

# Using random module
print('\\nRandom Module:')
print(f'Random float [0,1): {random.random()}')
print(f'Random int [1,10]: {random.randint(1, 10)}')
colors = ['red', 'blue', 'green', 'yellow']
print(f'Random choice: {random.choice(colors)}')

numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print(f'Shuffled: {numbers}')

# Using datetime module
print('\\nDatetime Module:')
now = datetime.datetime.now()
print(f'Current time: {now}')
print(f'Formatted: {now.strftime(\"%Y-%m-%d %H:%M:%S\")}')

birthday = datetime.datetime(2000, 1, 1)
age = now.year - birthday.year
print(f'Years since 2000: {age}')

# Using os module
print('\\nOS Module:')
print(f'Current directory: {os.getcwd()}')
print(f'User home: {os.path.expanduser(\"~\")}')
print(f'Path separator: {os.sep}')

# Different import methods
print('\\n--- Import Methods ---')

# Method 1: import module
import math as m
print(f'Using alias: {m.sqrt(25)}')

# Method 2: from module import specific items
from random import randint, choice
print(f'Random int: {randint(1, 100)}')
print(f'Random choice: {choice([\"a\", \"b\", \"c\"])}')

# Method 3: from module import * (not recommended!)
# from math import *  # Imports everything

# Creating your own module
print('\\n--- Creating Your Own Module ---')
print('''
To create a module:

1. Create a file called 'mymodule.py':
   # mymodule.py
   def greet(name):
       return f\"Hello, {name}!\"
   
   def add(a, b):
       return a + b
   
   PI = 3.14159

2. Import and use it:
   import mymodule
   print(mymodule.greet(\"Alice\"))
   print(mymodule.add(5, 3))
   print(mymodule.PI)

3. Or import specific items:
   from mymodule import greet, PI
   print(greet(\"Bob\"))
   print(PI)
''')

# Useful standard library modules
print('--- Useful Standard Library Modules ---')

# json: Work with JSON data
import json
data = {'name': 'Alice', 'age': 25, 'city': 'NYC'}
json_string = json.dumps(data, indent=2)
print('\\nJSON module:')
print(json_string)

# sys: System-specific parameters
import sys
print('\\nSys module:')
print(f'Python version: {sys.version.split()[0]}')
print(f'Platform: {sys.platform}')

# time: Time-related functions
import time
print('\\nTime module:')
print(f'Current timestamp: {time.time()}')
print('Sleeping for 1 second...')
time.sleep(1)
print('Done!')

# collections: Specialized container types
from collections import Counter, defaultdict
print('\\nCollections module:')
words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
word_count = Counter(words)
print(f'Word count: {word_count}')
print(f'Most common: {word_count.most_common(2)}')

# Creating a package structure
print('\\n--- Package Structure ---')
print('''
Package structure example:

mypackage/
├── __init__.py
├── module1.py
├── module2.py
└── subpackage/
    ├── __init__.py
    └── module3.py

Usage:
from mypackage import module1
from mypackage.subpackage import module3
import mypackage.module2 as m2
''')

# Installing external packages with pip
print('\\n--- Installing Packages with PIP ---')
print('''
PIP is Python's package installer.

Common commands:
  pip install package_name    # Install a package
  pip install package==1.2.3  # Install specific version
  pip install -r requirements.txt  # Install from file
  pip list                    # List installed packages
  pip show package_name       # Show package info
  pip uninstall package_name  # Remove package
  pip freeze > requirements.txt  # Save all packages

Popular packages to try:
  pip install requests        # HTTP library
  pip install pandas          # Data analysis
  pip install numpy           # Numerical computing
  pip install matplotlib      # Plotting
  pip install beautifulsoup4  # Web scraping
  pip install flask           # Web framework
''')

# PRACTICE: Using multiple modules
print('--- Practice: File Info Script ---')

import os
import datetime

def get_file_info(filename):
    \"\"\"Get information about a file\"\"\"
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        modified = os.path.getmtime(filename)
        mod_date = datetime.datetime.fromtimestamp(modified)
        return f'''
File: {filename}
Size: {size} bytes
Modified: {mod_date.strftime(\"%Y-%m-%d %H:%M:%S\")}
'''
    else:
        return f'File {filename} not found'

# Create a test file
with open('test_file.txt', 'w') as f:
    f.write('Hello, World!')

print(get_file_info('test_file.txt'))

print('--- Lesson 13 complete! Try Lesson 14! ---')
""",

    "Lesson 14: Final Project - Task Manager": """'''
LESSON 14: FINAL PROJECT - TASK MANAGER
========================================

Let's build a complete task manager application that combines
everything you've learned!

FEATURES:
- Add tasks
- View tasks
- Mark tasks as complete
- Delete tasks
- Save/load tasks from file
- Search tasks

This demonstrates:
- Functions
- Lists & dictionaries
- File handling
- Error handling
- Loops
- User input
'''

import json
import datetime

class TaskManager:
    \"\"\"Task Manager Application\"\"\"
    
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
    
    def add_task(self, title, description='', priority='medium'):
        \"\"\"Add a new task\"\"\"
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'priority': priority,
            'completed': False,
            'created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        self.tasks.append(task)
        self.save_tasks()
        return f'✓ Task added: {title}'
    
    def view_tasks(self, show_completed=True):
        \"\"\"View all tasks\"\"\"
        if not self.tasks:
            return 'No tasks found!'
        
        output = []
        output.append('\\n' + '='*60)
        output.append('TASK LIST')
        output.append('='*60)
        
        for task in self.tasks:
            if not show_completed and task['completed']:
                continue
            
            status = '✓' if task['completed'] else '○'
            priority_icon = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(task['priority'], '⚪')
            
            output.append(f\"\\n[{task['id']}] {status} {priority_icon} {task['title']}\")
            if task['description']:
                output.append(f\"    {task['description']}\")
            output.append(f\"    Created: {task['created']}\")
        
        output.append('\\n' + '='*60)
        return '\\n'.join(output)
    
    def complete_task(self, task_id):
        \"\"\"Mark task as complete\"\"\"
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                return f\"✓ Completed: {task['title']}\"
        return f'Task {task_id} not found!'
    
    def delete_task(self, task_id):
        \"\"\"Delete a task\"\"\"
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                title = task['title']
                self.tasks.pop(i)
                self.save_tasks()
                return f'✓ Deleted: {title}'
        return f'Task {task_id} not found!'
    
    def search_tasks(self, keyword):
        \"\"\"Search tasks by keyword\"\"\"
        keyword = keyword.lower()
        results = []
        
        for task in self.tasks:
            if (keyword in task['title'].lower() or 
                keyword in task['description'].lower()):
                results.append(task)
        
        if not results:
            return f'No tasks found matching \"{keyword}\"'
        
        output = [f'\\nFound {len(results)} task(s):']
        for task in results:
            status = '✓' if task['completed'] else '○'
            output.append(f\"[{task['id']}] {status} {task['title']}\")
        
        return '\\n'.join(output)
    
    def get_stats(self):
        \"\"\"Get task statistics\"\"\"
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['completed'])
        pending = total - completed
        
        high = sum(1 for t in self.tasks if t['priority'] == 'high')
        medium = sum(1 for t in self.tasks if t['priority'] == 'medium')
        low = sum(1 for t in self.tasks if t['priority'] == 'low')
        
        return f'''
STATISTICS:
Total tasks: {total}
Completed: {completed}
Pending: {pending}
High priority: {high}
Medium priority: {medium}
Low priority: {low}
'''
    
    def save_tasks(self):
        \"\"\"Save tasks to file\"\"\"
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            print(f'Error saving tasks: {e}')
    
    def load_tasks(self):
        \"\"\"Load tasks from file\"\"\"
        try:
            with open(self.filename, 'r') as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []
        except Exception as e:
            print(f'Error loading tasks: {e}')
            self.tasks = []

# Demo the task manager
print('='*60)
print('TASK MANAGER APPLICATION')
print('='*60)

# Create task manager
tm = TaskManager()

# Add some demo tasks
print('\\n--- Adding Tasks ---')
print(tm.add_task('Learn Python', 'Complete Python course', 'high'))
print(tm.add_task('Build project', 'Create a web app', 'medium'))
print(tm.add_task('Read documentation', priority='low'))

# View all tasks
print(tm.view_tasks())

# Complete a task
print('\\n--- Completing Task ---')
print(tm.complete_task(1))

# View updated tasks
print(tm.view_tasks())

# Search tasks
print('\\n--- Searching Tasks ---')
print(tm.search_tasks('python'))

# Get statistics
print(tm.get_stats())

# Delete a task
print('\\n--- Deleting Task ---')
print(tm.delete_task(3))

# Final view
print(tm.view_tasks())

print('''
\\n--- CONGRATULATIONS! ---
You've completed the Python course!

You've learned:
✓ Variables & data types
✓ Control flow (if/else)
✓ Loops (for/while)
✓ Functions
✓ Lists & dictionaries
✓ File handling
✓ Error handling
✓ Object-oriented programming
✓ Modules & packages
✓ Building complete applications

NEXT STEPS:
1. Build your own projects
2. Explore libraries (pandas, requests, flask)
3. Learn web development with Django/Flask
4. Try data science with pandas/numpy
5. Explore machine learning with scikit-learn

Keep coding and have fun! 🚀
''')
"""
}

# Comprehensive Python Examples
PYTHON_EXAMPLES = {
    # Fundamentals & Best Practices
    "Syntax vs PEP8": "# Python Syntax is flexible, PEP8 is the style guide\n\n# BAD: Not PEP8 compliant\ndef badFunction(x,y):\n    return x+y\n\n# GOOD: PEP8 compliant\ndef good_function(x, y):\n    \"\"\"Add two numbers together.\"\"\"\n    return x + y\n\n# PEP8 Rules:\n# - 4 spaces for indentation\n# - snake_case for functions/variables\n# - PascalCase for classes\n# - 2 blank lines between top-level definitions\n# - Max line length: 79 characters\n\nprint(good_function(5, 3))",
    "VSCode Project Setup": "# Setting up a Python project in VSCode\n\n# 1. Create project structure:\n# my_project/\n#   ├── src/\n#   │   └── main.py\n#   ├── tests/\n#   │   └── test_main.py\n#   ├── requirements.txt\n#   ├── README.md\n#   └── .gitignore\n\n# 2. Create virtual environment:\n# python -m venv venv\n\n# 3. Activate it:\n# Windows: .\\venv\\Scripts\\activate\n# Mac/Linux: source venv/bin/activate\n\n# 4. Install dependencies:\n# pip install -r requirements.txt\n\nprint('Project structure ready!')\nprint('VSCode extensions to install:')\nprint('  - Python (Microsoft)')\nprint('  - Pylance')\nprint('  - autopep8 or Black formatter')",
    "Variables & Types": "# Python is dynamically typed\n\n# Basic types\nname = 'Alice'          # str\nage = 30                # int\nheight = 5.7            # float\nis_student = True       # bool\n\n# Type checking\nprint(f'name is {type(name).__name__}')\nprint(f'age is {type(age).__name__}')\n\n# Type hints (Python 3.5+)\ndef greet(name: str, age: int) -> str:\n    return f'Hello {name}, you are {age} years old'\n\nprint(greet('Bob', 25))\n\n# Type conversion\nnum_str = '42'\nnum_int = int(num_str)\nprint(f'Converted: {num_int} is {type(num_int).__name__}')",
    "Loops Mastery": "# For loops\nfor i in range(5):\n    print(f'Count: {i}')\n\n# While loops\ncount = 0\nwhile count < 3:\n    print(f'While: {count}')\n    count += 1\n\n# Loop with break\nfor i in range(10):\n    if i == 5:\n        break\n    print(i)\n\n# Loop with continue\nfor i in range(5):\n    if i == 2:\n        continue\n    print(i)\n\n# Enumerate\nfruits = ['apple', 'banana', 'cherry']\nfor idx, fruit in enumerate(fruits):\n    print(f'{idx}: {fruit}')\n\n# Nested loops\nfor i in range(3):\n    for j in range(3):\n        print(f'({i},{j})', end=' ')\n    print()",
    "REST APIs & JSON": "import json\n\n# Working with JSON\ndata = {\n    'name': 'Alice',\n    'age': 30,\n    'skills': ['Python', 'JavaScript', 'SQL']\n}\n\n# Convert to JSON string\njson_string = json.dumps(data, indent=2)\nprint('JSON String:')\nprint(json_string)\n\n# Parse JSON string\nparsed = json.loads(json_string)\nprint(f\"\\nName: {parsed['name']}\")\nprint(f\"Skills: {', '.join(parsed['skills'])}\")\n\n# Note: For actual REST API calls, use:\n# import requests\n# response = requests.get('https://api.example.com/data')\n# data = response.json()\nprint('\\nInstall requests: pip install requests')",
    "File Reading & Writing": "# Writing to a file\nwith open('sample.txt', 'w') as f:\n    f.write('Hello, World!\\n')\n    f.write('Python file operations\\n')\n    f.write('Line 3')\n\nprint('✓ File written')\n\n# Reading entire file\nwith open('sample.txt', 'r') as f:\n    content = f.read()\n    print('\\nFile contents:')\n    print(content)\n\n# Reading line by line\nwith open('sample.txt', 'r') as f:\n    print('\\nLine by line:')\n    for line_num, line in enumerate(f, 1):\n        print(f'{line_num}: {line.strip()}')\n\n# Append to file\nwith open('sample.txt', 'a') as f:\n    f.write('\\nAppended line')\n\nprint('\\n✓ File operations complete')",
    "User Input": "# Getting user input\nprint('User Input Examples:\\n')\n\n# Basic input (commented out for auto-run)\n# name = input('Enter your name: ')\n# print(f'Hello, {name}!')\n\n# Input with type conversion\n# age = int(input('Enter your age: '))\n# print(f'In 10 years, you will be {age + 10}')\n\n# Validation loop\n# while True:\n#     choice = input('Enter yes or no: ').lower()\n#     if choice in ['yes', 'no']:\n#         break\n#     print('Invalid input, try again')\n\n# Simulated input for demo\nname = 'Alice'\nage = 25\nprint(f'Simulated: Hello, {name}!')\nprint(f'Simulated: In 10 years, you will be {age + 10}')\nprint('\\nNote: Uncomment lines for interactive input')",
    "Writing Functions": "# Basic function\ndef greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('Alice'))\n\n# Default parameters\ndef greet_with_title(name, title='Mr.'):\n    return f'Hello, {title} {name}!'\n\nprint(greet_with_title('Smith'))\nprint(greet_with_title('Johnson', 'Dr.'))\n\n# Multiple return values\ndef get_stats(numbers):\n    return min(numbers), max(numbers), sum(numbers)\n\nnums = [1, 2, 3, 4, 5]\nmin_val, max_val, total = get_stats(nums)\nprint(f'Min: {min_val}, Max: {max_val}, Sum: {total}')\n\n# *args and **kwargs\ndef flexible_func(*args, **kwargs):\n    print(f'Args: {args}')\n    print(f'Kwargs: {kwargs}')\n\nflexible_func(1, 2, 3, name='Alice', age=30)",
    "Modules & PIP": "# Built-in modules\nimport os\nimport sys\nfrom datetime import datetime\n\nprint('Current directory:', os.getcwd())\nprint('Python version:', sys.version.split()[0])\nprint('Current time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))\n\n# Creating your own module:\n# 1. Create file 'mymodule.py' with functions\n# 2. Import it: import mymodule\n# 3. Use it: mymodule.my_function()\n\nprint('\\nPIP Commands:')\nprint('  pip install package_name')\nprint('  pip install -r requirements.txt')\nprint('  pip list')\nprint('  pip show package_name')\nprint('  pip uninstall package_name')\nprint('  pip freeze > requirements.txt')\n\nprint('\\nPopular packages to install:')\nprint('  pip install requests pandas numpy matplotlib')",
    "Ollama Setup": "# Setting up Ollama for AI functionality\n\nprint('Ollama Setup Steps:')\nprint('='*50)\nprint('\\n1. Download Ollama:')\nprint('   Visit: https://ollama.ai')\nprint('   Download for your OS (Windows/Mac/Linux)')\nprint()\nprint('2. Install Ollama')\nprint('   Run the installer')\nprint()\nprint('3. Pull a model:')\nprint('   ollama pull llama2')\nprint('   ollama pull codellama')\nprint('   ollama pull mistral')\nprint()\nprint('4. Test it:')\nprint('   ollama run llama2')\nprint()\nprint('5. Install Python package:')\nprint('   pip install ollama')\nprint()\nprint('6. Check available models:')\nprint('   ollama list')\nprint('='*50)",
    "Ollama AI Scripts": "# Using Ollama with Python\n\nprint('Install first: pip install ollama\\n')\n\n# Example code (requires ollama package):\ncode_example = '''\nimport ollama\n\n# Simple chat\nresponse = ollama.chat(\n    model='llama2',\n    messages=[\n        {'role': 'user', 'content': 'Why is the sky blue?'}\n    ]\n)\nprint(response['message']['content'])\n\n# Streaming response\nfor chunk in ollama.chat(\n    model='llama2',\n    messages=[{'role': 'user', 'content': 'Tell me a joke'}],\n    stream=True\n):\n    print(chunk['message']['content'], end='', flush=True)\n\n# Code generation with CodeLlama\nresponse = ollama.chat(\n    model='codellama',\n    messages=[\n        {'role': 'user', 'content': 'Write a Python function to calculate fibonacci'}\n    ]\n)\nprint(response['message']['content'])\n'''\n\nprint('Example Ollama Python Code:')\nprint('='*50)\nprint(code_example)\nprint('='*50)",
}

# Course Labs & Projects
COURSE_LABS = {
    "LAB - Guessing Game": "from random import randint\n\nnumber = randint(1,10)\n\nwhile True:\n    guess = input('Your Guess: ')\n    guess = int(guess)\n\n    if guess > number:\n        print(f'{guess} is too high')\n    elif guess < number:\n        print(f'{guess} is too low')\n    else:\n        print(f'{guess} is right')\n        break",
    "LAB - Repayment Calculator": "owed = float(input('Starting Loan: '))\npayment = float(input('Monthly Payment: '))\ninterest = float(input('Yearly Interest Rate: '))\n\ninterest_monthly = (interest / 12) / 100\nmonth = 0\n\nwhile owed >= 0:\n    print(f'Month {month}: ${owed:.2f}')\n    owed = owed - payment\n    owed = owed + (owed * interest_monthly)\n    month += 1\n\nprint(f'\\nMonths to Pay Off = {month}')",
    "LAB - Joke Web App": "import requests\n\nurl = 'https://official-joke-api.appspot.com/random_joke'\n\nresponse = requests.get(url).json()\n\nprint(response['setup'])\nprint(response['punchline'])\n\nwith open('joke.html', 'w') as file:\n    file.write('<h1>Joke Web App</h1>')\n    file.write(f\"<p>{response['setup']}</p>\")\n    file.write('<hr>')\n    file.write(f\"<p>{response['punchline']}</p>\")\n\nprint('\\n✓ Joke saved to joke.html')",
    "LAB - Journal App": "import datetime\n\nwhile True:\n    title = input('Title: ')\n    note = input('Note: ')\n    time = datetime.datetime.now()\n    \n    with open('data.csv', 'a') as file:\n        file.write(f'{title}|{time}|{note}\\n')\n\n    with open('data.csv', 'r') as file:\n        records = file.readlines()\n    \n    records.sort(reverse=True)\n\n    with open('journal.htm', 'w') as file:\n        file.write('<h1>Journal App</h1>')\n\n    for line in records:\n        note_parts = line.split('|')\n        with open('journal.htm', 'a') as file:\n            file.write(f'<h2>{note_parts[0]}</h2>')\n            file.write(f'<strong>{note_parts[1]}</strong>')\n            file.write(f'<p>{note_parts[2]}</p>')\n    \n    print('\\n✓ Journal updated!')\n    break  # Remove this to continue adding entries",
    "LAB - Up/Down Dashboard": "import os\n\nhost = ['cnn.com', 'google.com', 'github.com']\n\ncommand = 'ping -c 1 '  # Use 'ping -n 1 ' for Windows\n\npage = '''<meta http-equiv=\"refresh\" content=\"5\">\n<h1>Up/Down Dashboard</h1>\n'''\n\nfor site in host:\n    response = os.popen(f'{command} {site}').read()\n    status = '🟢 UP' if 'bytes from' in response else '🔴 DOWN'\n    page += f'<h2>{site} - {status}</h2>'\n    page += f'<pre>{response[:200]}</pre><hr>'\n\nwith open('dashboard.htm', 'w') as file:\n    file.write(page)\n\nprint('✓ Dashboard saved to dashboard.htm')",
    "LAB - Basic Ollama": "# Install: pip install ollama\nprint('Basic Ollama Script\\n')\n\ncode = '''\nfrom ollama import chat\nfrom ollama import ChatResponse\n\nresponse: ChatResponse = chat(\n    model='granite3:1b',\n    messages=[{\n        'role': 'user',\n        'content': 'Why is the sky blue?',\n    }]\n)\n\nprint(response.message.content)\n'''\n\nprint(code)\nprint('\\nNote: Requires Ollama installed and running')\nprint('Download from: https://ollama.com')",
    "LAB - Dynamic Ollama": "# Interactive AI Chat\nprint('Dynamic Ollama Script\\n')\n\ncode = '''\nfrom ollama import chat\nfrom ollama import ChatResponse\nimport os\n\ndef ai(query):\n    injection = 'Answer in under 20 words'\n    query = f'{injection} -- {query}'\n    response: ChatResponse = chat(\n        model='granite3:1b',\n        messages=[{'role': 'user', 'content': query}]\n    )\n    return response.message.content\n\nwhile True:\n    query = input('Query: ')\n    if query.lower() == 'quit':\n        break\n    response = ai(query)\n    os.system('clear')  # 'cls' on Windows\n    print(f'Q: {query}')\n    print(f'A: {response}\\n')\n'''\n\nprint(code)\nprint('\\nInstall: pip install ollama')",
    "LAB - Personalized AI": "# AI with Geographic Context\nprint('Personalized AI Script\\n')\n\ncode = '''\nfrom ollama import chat\nimport requests\n\ndef geo():\n    url = 'http://ip-api.com/json/'\n    return requests.get(url).json()\n\ndef ai(query, location):\n    prompt = f\"\"\"I am in {location['city']}, {location['country']}.\n    Question: {query}\n    Answer in under 20 words.\"\"\"\n    \n    response = chat(\n        model='granite3:1b',\n        messages=[{'role': 'user', 'content': prompt}]\n    )\n    return response.message.content\n\nlocation = geo()\nwhile True:\n    query = input('Query: ')\n    if query == 'quit': break\n    print(ai(query, location))\n'''\n\nprint(code)\nprint('\\nInstall: pip install ollama requests')",
    "LAB - AI Memory": "# AI with Conversation Memory\nprint('AI Memory Script\\n')\n\ncode = '''\nfrom ollama import chat\nimport os\n\ndef ai(query, memory):\n    prompt = f\"\"\"Previous conversation:\n{memory}\n\nNew question: {query}\nAnswer in under 20 words.\"\"\"\n    \n    response = chat(\n        model='granite3:1b',\n        messages=[{'role': 'user', 'content': prompt}]\n    )\n    return response.message.content\n\n# Initialize memory\nwith open('memory.txt', 'w') as f:\n    f.write('Conversation log\\n\\n')\n\nwhile True:\n    query = input('Query: ')\n    if query == 'quit': break\n    \n    with open('memory.txt', 'r') as f:\n        memory = f.read()\n    \n    response = ai(query, memory)\n    print(response)\n    \n    with open('memory.txt', 'a') as f:\n        f.write(f'Q: {query}\\nA: {response}\\n\\n')\n'''\n\nprint(code)\nprint('\\nInstall: pip install ollama')",
    "LAB - AI Autoblog": "# AI Autoblog Generator\nprint('AI Autoblog Script\\n')\n\ncode = '''\nfrom ollama import chat\nfrom bs4 import BeautifulSoup\nimport requests\n\ndef scrape(url):\n    page = requests.get(url).text\n    soup = BeautifulSoup(page, \"html.parser\")\n    paragraphs = soup.find_all(\"p\")\n    return ' '.join([p.text for p in paragraphs])\n\ndef generate_post(text):\n    response = chat(\n        model='granite3:1b',\n        messages=[{\n            'role': 'user',\n            'content': f'Write 200 word blog post: {text[:500]}'\n        }]\n    )\n    return response.message.content\n\ndef generate_title(text):\n    response = chat(\n        model='granite3:1b',\n        messages=[{\n            'role': 'user',\n            'content': f'Create 10 word title: {text[:200]}'\n        }]\n    )\n    return response.message.content\n\nurl = input('URL: ')\ntext = scrape(url)\ntitle = generate_title(text)\npost = generate_post(text)\n\nwith open('autoblog.htm', 'a') as f:\n    f.write(f'<h1>{title}</h1><p>{post}</p>')\n\nprint(f'Title: {title}')\nprint(f'Post: {post}')\n'''\n\nprint(code)\nprint('\\nInstall: pip install ollama beautifulsoup4 requests')",
}

# Data Types & Structures
PYTHON_EXAMPLES_CONT = {
    "Strings": "s = 'Hello, Python!'\nprint(s.upper())\nprint(s.lower())\nprint(s.split(','))\nprint(s.replace('Python', 'World'))\nprint(f'Length: {len(s)}')\nprint(s[0:5])  # Slicing",
    "Lists": "nums = [1, 2, 3, 4, 5]\nnums.append(6)\nnums.extend([7, 8])\nprint(nums)\nprint(nums[2:5])\nprint(sorted(nums, reverse=True))\nprint([x*2 for x in nums])  # List comprehension",
    "Tuples": "coords = (10, 20, 30)\nx, y, z = coords  # Unpacking\nprint(f'x={x}, y={y}, z={z}')\nprint(coords[1])\nprint(len(coords))\n# Tuples are immutable",
    "Dictionaries": "person = {'name': 'Alice', 'age': 30, 'city': 'NYC'}\nprint(person['name'])\nprint(person.get('age'))\nperson['job'] = 'Engineer'\nfor key, val in person.items():\n    print(f'{key}: {val}')",
    "Sets": "s1 = {1, 2, 3, 4, 5}\ns2 = {4, 5, 6, 7, 8}\nprint('Union:', s1 | s2)\nprint('Intersection:', s1 & s2)\nprint('Difference:', s1 - s2)\ns1.add(6)\nprint('Updated:', s1)",
    
    # Control Flow
    "If-Elif-Else": "x = 10\nif x > 15:\n    print('Large')\nelif x > 5:\n    print('Medium')\nelse:\n    print('Small')\n\n# Ternary\nresult = 'Even' if x % 2 == 0 else 'Odd'\nprint(result)",
    "For Loops": "# Range\nfor i in range(5):\n    print(i)\n\n# List iteration\nfruits = ['apple', 'banana', 'cherry']\nfor fruit in fruits:\n    print(fruit)\n\n# Enumerate\nfor idx, fruit in enumerate(fruits):\n    print(f'{idx}: {fruit}')",
    "While Loops": "count = 0\nwhile count < 5:\n    print(f'Count: {count}')\n    count += 1\n\n# With break\ni = 0\nwhile True:\n    if i >= 3:\n        break\n    print(i)\n    i += 1",
    "Comprehensions": "# List comprehension\nsquares = [x**2 for x in range(10)]\nprint(squares)\n\n# Dict comprehension\nsq_dict = {x: x**2 for x in range(5)}\nprint(sq_dict)\n\n# Set comprehension\nevens = {x for x in range(10) if x % 2 == 0}\nprint(evens)",
    
    # Functions
    "Functions": "def greet(name, greeting='Hello'):\n    return f'{greeting}, {name}!'\n\nprint(greet('Alice'))\nprint(greet('Bob', 'Hi'))\n\n# *args and **kwargs\ndef func(*args, **kwargs):\n    print('Args:', args)\n    print('Kwargs:', kwargs)\n\nfunc(1, 2, 3, x=10, y=20)",
    "Lambda": "# Lambda functions\nadd = lambda x, y: x + y\nprint(add(5, 3))\n\n# With map, filter\nnums = [1, 2, 3, 4, 5]\nsquared = list(map(lambda x: x**2, nums))\nevens = list(filter(lambda x: x % 2 == 0, nums))\nprint('Squared:', squared)\nprint('Evens:', evens)",
    "Decorators": "def uppercase_decorator(func):\n    def wrapper(*args, **kwargs):\n        result = func(*args, **kwargs)\n        return result.upper()\n    return wrapper\n\n@uppercase_decorator\ndef greet(name):\n    return f'hello, {name}'\n\nprint(greet('alice'))",
    "Generators": "def countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\n\nfor i in countdown(5):\n    print(i)\n\n# Generator expression\nsquares = (x**2 for x in range(5))\nprint(list(squares))",
    
    # OOP
    "Classes": "class Dog:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    \n    def bark(self):\n        return f'{self.name} says Woof!'\n    \n    def __str__(self):\n        return f'Dog({self.name}, {self.age})'\n\ndog = Dog('Rex', 5)\nprint(dog)\nprint(dog.bark())",
    "Inheritance": "class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        return 'Some sound'\n\nclass Cat(Animal):\n    def speak(self):\n        return f'{self.name} says Meow!'\n\ncat = Cat('Whiskers')\nprint(cat.speak())\nprint(isinstance(cat, Animal))",
    "Magic Methods": "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    \n    def __add__(self, other):\n        return Point(self.x + other.x, self.y + other.y)\n    \n    def __str__(self):\n        return f'Point({self.x}, {self.y})'\n\np1 = Point(1, 2)\np2 = Point(3, 4)\np3 = p1 + p2\nprint(p3)",
    "Properties": "class Circle:\n    def __init__(self, radius):\n        self._radius = radius\n    \n    @property\n    def radius(self):\n        return self._radius\n    \n    @radius.setter\n    def radius(self, value):\n        if value < 0:\n            raise ValueError('Radius cannot be negative')\n        self._radius = value\n    \n    @property\n    def area(self):\n        return 3.14159 * self._radius ** 2\n\nc = Circle(5)\nprint(f'Area: {c.area:.2f}')\nc.radius = 10\nprint(f'New area: {c.area:.2f}')",
    
    # Error Handling
    "Try-Except": "try:\n    x = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero')\nexcept Exception as e:\n    print(f'Error: {e}')\nelse:\n    print('No errors')\nfinally:\n    print('Cleanup code')",
    "Custom Exceptions": "class CustomError(Exception):\n    pass\n\ndef validate_age(age):\n    if age < 0:\n        raise CustomError('Age cannot be negative')\n    return age\n\ntry:\n    validate_age(-5)\nexcept CustomError as e:\n    print(f'Validation error: {e}')",
    
    # File I/O
    "File Reading": "# Write file\nwith open('test.txt', 'w') as f:\n    f.write('Hello, World!\\n')\n    f.write('Python is awesome!')\n\n# Read file\nwith open('test.txt', 'r') as f:\n    content = f.read()\n    print(content)\n\n# Read lines\nwith open('test.txt', 'r') as f:\n    for line in f:\n        print(line.strip())",
    "JSON": "import json\n\ndata = {'name': 'Alice', 'age': 30, 'hobbies': ['reading', 'coding']}\n\n# To JSON string\njson_str = json.dumps(data, indent=2)\nprint(json_str)\n\n# From JSON string\nparsed = json.loads(json_str)\nprint(parsed['name'])",
    
    # Standard Library
    "OS Module": "import os\n\nprint('Current dir:', os.getcwd())\nprint('Home dir:', os.path.expanduser('~'))\nprint('Path exists:', os.path.exists('.'))\nprint('Is file:', os.path.isfile('UnifiedApp.py'))\nprint('Is dir:', os.path.isdir('.'))",
    "Datetime": "from datetime import datetime, timedelta\n\nnow = datetime.now()\nprint('Now:', now)\nprint('Formatted:', now.strftime('%Y-%m-%d %H:%M:%S'))\n\ntomorrow = now + timedelta(days=1)\nprint('Tomorrow:', tomorrow.strftime('%Y-%m-%d'))",
    "Collections": "from collections import Counter, defaultdict, namedtuple\n\n# Counter\nwords = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']\ncounter = Counter(words)\nprint(counter)\nprint(counter.most_common(2))\n\n# defaultdict\ndd = defaultdict(int)\ndd['a'] += 1\nprint(dd)\n\n# namedtuple\nPoint = namedtuple('Point', ['x', 'y'])\np = Point(10, 20)\nprint(f'Point: x={p.x}, y={p.y}')",
    "Itertools": "from itertools import count, cycle, chain, combinations\n\n# Count\nfor i in count(10, 2):\n    if i > 20:\n        break\n    print(i)\n\n# Chain\nlist1 = [1, 2, 3]\nlist2 = [4, 5, 6]\nprint(list(chain(list1, list2)))\n\n# Combinations\nprint(list(combinations([1, 2, 3], 2)))",
    "Random": "import random\n\nprint('Random int:', random.randint(1, 10))\nprint('Random float:', random.random())\nprint('Random choice:', random.choice(['a', 'b', 'c']))\n\nitems = [1, 2, 3, 4, 5]\nrandom.shuffle(items)\nprint('Shuffled:', items)\nprint('Sample:', random.sample(items, 3))",
    "Math": "import math\n\nprint('Pi:', math.pi)\nprint('E:', math.e)\nprint('sqrt(16):', math.sqrt(16))\nprint('sin(π/2):', math.sin(math.pi/2))\nprint('log(10):', math.log(10))\nprint('ceil(4.3):', math.ceil(4.3))\nprint('floor(4.7):', math.floor(4.7))",
    
    # Advanced
    "Context Managers": "class FileManager:\n    def __init__(self, filename):\n        self.filename = filename\n    \n    def __enter__(self):\n        self.file = open(self.filename, 'w')\n        return self.file\n    \n    def __exit__(self, exc_type, exc_val, exc_tb):\n        self.file.close()\n\nwith FileManager('test.txt') as f:\n    f.write('Context manager!')\n\nprint('File closed automatically')",
    "Enumerate & Zip": "# Enumerate\nfruits = ['apple', 'banana', 'cherry']\nfor idx, fruit in enumerate(fruits, start=1):\n    print(f'{idx}. {fruit}')\n\n# Zip\nnames = ['Alice', 'Bob', 'Charlie']\nages = [25, 30, 35]\nfor name, age in zip(names, ages):\n    print(f'{name} is {age} years old')",
    "Map & Filter": "# Map\nnums = [1, 2, 3, 4, 5]\nsquared = list(map(lambda x: x**2, nums))\nprint('Squared:', squared)\n\n# Filter\nevens = list(filter(lambda x: x % 2 == 0, nums))\nprint('Evens:', evens)\n\n# Reduce\nfrom functools import reduce\nproduct = reduce(lambda x, y: x * y, nums)\nprint('Product:', product)",
    "Sorting": "# Sort list\nnums = [3, 1, 4, 1, 5, 9, 2, 6]\nprint('Sorted:', sorted(nums))\nprint('Reverse:', sorted(nums, reverse=True))\n\n# Sort with key\nwords = ['banana', 'pie', 'Washington', 'book']\nprint('By length:', sorted(words, key=len))\nprint('Case insensitive:', sorted(words, key=str.lower))\n\n# Sort dict\ndata = {'c': 3, 'a': 1, 'b': 2}\nprint('Sorted dict:', dict(sorted(data.items())))",
}

# Merge Python examples
PYTHON_EXAMPLES.update(PYTHON_EXAMPLES_CONT)

# Roadmap Examples by Phase
ROADMAP_EXAMPLES = {
    # Phase 1: Mathematical Foundations
    "Phase 1 - Linear Algebra": "import numpy as np\nv1 = np.array([1, 2, 3])\nv2 = np.array([4, 5, 6])\nprint('Dot product:', np.dot(v1, v2))\nprint('Vector norm:', np.linalg.norm(v1))\nprint('Normalized:', v1 / np.linalg.norm(v1))",
    "Phase 1 - Derivatives": "def numerical_derivative(f, x, h=1e-5):\n    return (f(x + h) - f(x - h)) / (2 * h)\n\ndef f(x):\n    return x**2\n\nx = 2.0\nprint(f'f({x}) = {f(x)}')\nprint(f\"f'({x}) = {numerical_derivative(f, x)}\")\nprint(f'Analytical: 2x = {2*x}')",
    "Phase 1 - Chain Rule": "# Backpropagation foundation\ndef outer(u):\n    return u**3\n\ndef inner(x):\n    return 2*x + 1\n\nx = 2.0\nu = inner(x)\ndf_du = 3 * u**2\ndu_dx = 2\ndf_dx = df_du * du_dx\nprint(f'Chain rule: df/dx = {df_dx}')",
    "Phase 1 - Matrix Operations": "import numpy as np\nA = np.array([[1, 2], [3, 4]])\nB = np.array([[5, 6], [7, 8]])\nprint('Matrix multiply:\\n', A @ B)\nprint('Transpose:\\n', A.T)\nprint('Determinant:', np.linalg.det(A))\nprint('Inverse:\\n', np.linalg.inv(A))",
    
    # Phase 2: PyTorch Proficiency
    "Phase 2 - Tensors": "import torch\n\n# Create tensors\nx = torch.tensor([1.0, 2.0, 3.0])\ny = torch.tensor([4.0, 5.0, 6.0])\n\nprint('Tensors:', x, y)\nprint('Addition:', x + y)\nprint('Dot product:', torch.dot(x, y))\nprint('Shape:', x.shape)",
    "Phase 2 - Autograd": "import torch\n\n# Requires gradient tracking\nx = torch.tensor([2.0], requires_grad=True)\ny = x ** 2\n\nprint('y = x^2, x =', x.item())\ny.backward()\nprint('dy/dx =', x.grad.item())\nprint('Expected: 2x = 2*2 = 4')",
    "Phase 2 - Linear Layer": "import torch\nimport torch.nn as nn\n\n# Simple linear layer\nlayer = nn.Linear(3, 2)\nx = torch.randn(1, 3)\noutput = layer(x)\n\nprint('Input shape:', x.shape)\nprint('Output shape:', output.shape)\nprint('Weights shape:', layer.weight.shape)\nprint('Bias shape:', layer.bias.shape)",
    "Phase 2 - Training Loop": "import torch\nimport torch.nn as nn\n\nmodel = nn.Linear(1, 1)\noptimizer = torch.optim.SGD(model.parameters(), lr=0.01)\nloss_fn = nn.MSELoss()\n\nfor epoch in range(5):\n    x = torch.randn(10, 1)\n    y = 2 * x + 1\n    \n    pred = model(x)\n    loss = loss_fn(pred, y)\n    \n    optimizer.zero_grad()\n    loss.backward()\n    optimizer.step()\n    \n    print(f'Epoch {epoch+1}: Loss = {loss.item():.4f}')",
    
    # Phase 3: From Scratch
    "Phase 3 - Value Class": "class Value:\n    def __init__(self, data):\n        self.data = data\n        self.grad = 0.0\n        self._backward = lambda: None\n    \n    def __add__(self, other):\n        out = Value(self.data + other.data)\n        def _backward():\n            self.grad += out.grad\n            other.grad += out.grad\n        out._backward = _backward\n        return out\n    \n    def backward(self):\n        self.grad = 1.0\n        self._backward()\n\na = Value(2.0)\nb = Value(3.0)\nc = a + b\nc.backward()\nprint(f'c = {c.data}, da/dc = {a.grad}, db/dc = {b.grad}')",
    "Phase 3 - Neuron": "import random\n\nclass Neuron:\n    def __init__(self, nin):\n        self.w = [random.uniform(-1, 1) for _ in range(nin)]\n        self.b = random.uniform(-1, 1)\n    \n    def __call__(self, x):\n        act = sum(wi*xi for wi, xi in zip(self.w, x)) + self.b\n        return max(0, act)  # ReLU\n\nneuron = Neuron(3)\nx = [1.0, 2.0, 3.0]\noutput = neuron(x)\nprint(f'Input: {x}')\nprint(f'Output: {output:.4f}')\nprint(f'Weights: {[f\"{w:.4f}\" for w in neuron.w]}')",
    "Phase 3 - MLP Layer": "import random\nimport math\n\ndef relu(x):\n    return max(0, x)\n\nclass Layer:\n    def __init__(self, nin, nout):\n        self.weights = [[random.gauss(0, 1/math.sqrt(nin)) \n                        for _ in range(nin)] for _ in range(nout)]\n        self.biases = [0.0] * nout\n    \n    def forward(self, x):\n        out = []\n        for w, b in zip(self.weights, self.biases):\n            out.append(relu(sum(wi*xi for wi, xi in zip(w, x)) + b))\n        return out\n\nlayer = Layer(3, 2)\noutput = layer.forward([1, 2, 3])\nprint(f'Output: {output}')",
    
    # Phase 4: Vision Mastery
    "Phase 4 - Conv2d": "import torch\nimport torch.nn as nn\n\nconv = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)\nx = torch.randn(1, 1, 28, 28)  # Batch, channels, height, width\n\noutput = conv(x)\nprint(f'Input shape: {x.shape}')\nprint(f'Output shape: {output.shape}')\nprint(f'Filter params: {conv.weight.shape}')",
    "Phase 4 - Simple CNN": "import torch\nimport torch.nn as nn\n\nclass SimpleCNN(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)\n        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)\n        self.pool = nn.MaxPool2d(2, 2)\n        self.fc = nn.Linear(64 * 7 * 7, 10)\n    \n    def forward(self, x):\n        x = self.pool(torch.relu(self.conv1(x)))\n        x = self.pool(torch.relu(self.conv2(x)))\n        x = x.view(-1, 64 * 7 * 7)\n        return self.fc(x)\n\nmodel = SimpleCNN()\nx = torch.randn(4, 1, 28, 28)\noutput = model(x)\nprint(f'Output shape: {output.shape}')",
    "Phase 4 - Data Augmentation": "import torch\nimport torchvision.transforms as T\n\n# Common augmentations\ntransform = T.Compose([\n    T.RandomHorizontalFlip(p=0.5),\n    T.RandomRotation(10),\n    T.ColorJitter(brightness=0.2, contrast=0.2),\n    T.Normalize(mean=[0.485], std=[0.229])\n])\n\nprint('Augmentation pipeline:')\nfor t in transform.transforms:\n    print(f'  - {t.__class__.__name__}')",
    
    # Phase 5: NLP & LLMs
    "Phase 5 - Tokenization": "# Simple character-level tokenizer\ntext = 'Hello, World!'\n\n# Build vocabulary\nchars = sorted(set(text))\nvocab_size = len(chars)\nchar_to_idx = {ch: i for i, ch in enumerate(chars)}\nidx_to_char = {i: ch for i, ch in enumerate(chars)}\n\n# Encode\nencoded = [char_to_idx[ch] for ch in text]\n\n# Decode\ndecoded = ''.join([idx_to_char[i] for i in encoded])\n\nprint(f'Original: {text}')\nprint(f'Encoded: {encoded}')\nprint(f'Decoded: {decoded}')\nprint(f'Vocab size: {vocab_size}')",
    "Phase 5 - Embeddings": "import torch\nimport torch.nn as nn\n\nvocab_size = 1000\nembedding_dim = 128\n\nembedding = nn.Embedding(vocab_size, embedding_dim)\ntokens = torch.tensor([1, 5, 10, 20])\n\nembedded = embedding(tokens)\nprint(f'Token IDs: {tokens}')\nprint(f'Embedding shape: {embedded.shape}')\nprint(f'Each token → {embedding_dim}D vector')",
    "Phase 5 - Attention": "import torch\nimport torch.nn.functional as F\n\n# Simplified attention\nQ = torch.randn(4, 8)  # Query\nK = torch.randn(4, 8)  # Key  \nV = torch.randn(4, 8)  # Value\n\n# Attention scores\nscores = Q @ K.T / (8 ** 0.5)\nweights = F.softmax(scores, dim=-1)\noutput = weights @ V\n\nprint('Attention mechanism:')\nprint(f'  Q, K, V shape: {Q.shape}')\nprint(f'  Attention weights: {weights.shape}')\nprint(f'  Output: {output.shape}')",
    "Phase 5 - Transformer Block": "import torch\nimport torch.nn as nn\n\nclass TransformerBlock(nn.Module):\n    def __init__(self, d_model, nhead):\n        super().__init__()\n        self.attention = nn.MultiheadAttention(d_model, nhead)\n        self.norm1 = nn.LayerNorm(d_model)\n        self.norm2 = nn.LayerNorm(d_model)\n        self.ffn = nn.Sequential(\n            nn.Linear(d_model, 4 * d_model),\n            nn.ReLU(),\n            nn.Linear(4 * d_model, d_model)\n        )\n    \n    def forward(self, x):\n        attn_out, _ = self.attention(x, x, x)\n        x = self.norm1(x + attn_out)\n        x = self.norm2(x + self.ffn(x))\n        return x\n\nblock = TransformerBlock(d_model=512, nhead=8)\nx = torch.randn(10, 32, 512)  # seq_len, batch, d_model\noutput = block(x)\nprint(f'Output shape: {output.shape}')",
    
    # Phase 6: Specialization
    "Phase 6 - VAE Encoder": "import torch\nimport torch.nn as nn\n\nclass VAEEncoder(nn.Module):\n    def __init__(self, input_dim, latent_dim):\n        super().__init__()\n        self.fc = nn.Linear(input_dim, 256)\n        self.mu = nn.Linear(256, latent_dim)\n        self.logvar = nn.Linear(256, latent_dim)\n    \n    def forward(self, x):\n        h = torch.relu(self.fc(x))\n        return self.mu(h), self.logvar(h)\n\nencoder = VAEEncoder(784, 20)\nx = torch.randn(32, 784)\nmu, logvar = encoder(x)\nprint(f'Latent mean: {mu.shape}')\nprint(f'Latent logvar: {logvar.shape}')",
    "Phase 6 - GAN Generator": "import torch\nimport torch.nn as nn\n\nclass Generator(nn.Module):\n    def __init__(self, latent_dim, output_dim):\n        super().__init__()\n        self.model = nn.Sequential(\n            nn.Linear(latent_dim, 128),\n            nn.ReLU(),\n            nn.Linear(128, 256),\n            nn.ReLU(),\n            nn.Linear(256, output_dim),\n            nn.Tanh()\n        )\n    \n    def forward(self, z):\n        return self.model(z)\n\ngen = Generator(100, 784)\nz = torch.randn(16, 100)\nfake_images = gen(z)\nprint(f'Generated images: {fake_images.shape}')",
    "Phase 6 - RL Q-Network": "import torch\nimport torch.nn as nn\n\nclass QNetwork(nn.Module):\n    def __init__(self, state_dim, action_dim):\n        super().__init__()\n        self.net = nn.Sequential(\n            nn.Linear(state_dim, 128),\n            nn.ReLU(),\n            nn.Linear(128, 128),\n            nn.ReLU(),\n            nn.Linear(128, action_dim)\n        )\n    \n    def forward(self, state):\n        return self.net(state)\n\nq_net = QNetwork(state_dim=4, action_dim=2)\nstate = torch.randn(1, 4)\nq_values = q_net(state)\nprint(f'Q-values: {q_values}')\nprint(f'Best action: {torch.argmax(q_values).item()}')",
}

# ============================================================================
# CORE RUNTIME FUNCTIONS
# ============================================================================

def safe_exec(code: str, context: str = "", *, auto_confirm: bool | None = None) -> str:
    """Execute code with safety controls and confirmation."""
    cx_cfg = POLICY["sandbox"]["code_exec"]
    confirm_required = cx_cfg["confirm_required"]
    restricted_globals = cx_cfg["restricted_globals"]
    max_timeout = cx_cfg["timeout_seconds"]
    
    # Handle confirmation
    if auto_confirm is None:
        auto_confirm = not confirm_required
    
    if not auto_confirm:
        response = input(f"Execute code? (y/n): {context[:50]}... ")
        if response.lower() != 'y':
            return "❌ Execution denied by user"
    
    try:
        start = time.time()
        globals_dict = {"__builtins__": ALLOWED_BUILTINS if restricted_globals else __builtins__}
        exec(code, globals_dict, {})
        elapsed = time.time() - start
        
        if elapsed > max_timeout:
            return f"⚠ Execution completed but took {elapsed:.2f}s (limit: {max_timeout}s)"
        
        return f"✓ Execution successful ({elapsed:.3f}s)"
    except Exception as exc:
        return f"❌ Error: {type(exc).__name__}: {str(exc)}"


def save_manifest(mode: str, input_text: str) -> str:
    """Save execution manifest for audit trail."""
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "input_hash": hashlib.sha256(input_text.encode()).hexdigest()[:16],
        "status": "ok"
    }
    manifest_path = os.path.join(SANDBOX_DIR, "last_run.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return manifest_path

# ============================================================================
# COPILOT TOOLS
# ============================================================================

def run_code(code: str, *, auto_confirm: bool | None = None) -> str:
    """Execute Python code snippet with safety controls."""
    result = safe_exec(code, f"copilot run: {code[:30]}", auto_confirm=auto_confirm)
    save_manifest("copilot_run", code)
    return result


def read_file(path: str, lines: int = 20) -> str:
    """Read first N lines of a file."""
    if not os.path.exists(path):
        return f"❌ File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = "".join(f.readlines()[:lines])
        save_manifest("copilot_read", path)
        return content
    except Exception as exc:
        return f"❌ Error reading file: {exc}"


def explain_code(code: str) -> str:
    """Provide simple code explanation."""
    lines = code.strip().split("\n")
    explanation = [f"📝 Code Analysis: {len(lines)} line(s)"]
    
    # Detect code elements
    if "def " in code:
        funcs = re.findall(r"def\s+(\w+)", code)
        explanation.append(f"  Functions: {', '.join(funcs)}")
    if "class " in code:
        classes = re.findall(r"class\s+(\w+)", code)
        explanation.append(f"  Classes: {', '.join(classes)}")
    if "import " in code or "from " in code:
        explanation.append("  Imports: Yes")
    
    # Show first few lines
    explanation.append("\nFirst lines:")
    for i, line in enumerate(lines[:5], 1):
        explanation.append(f"  {i}. {line.strip()}")
    
    save_manifest("copilot_explain", code[:50])
    return "\n".join(explanation)

# ============================================================================
# CODE HELPER TOOLS
# ============================================================================

def lint_code(code: str) -> str:
    """Check for common errors and style issues."""
    issues: List[str] = []
    lines = code.split("\n")
    
    for i, line in enumerate(lines, 1):
        if len(line) > 100:
            issues.append(f"Line {i}: Too long ({len(line)} chars)")
        if re.search(r"except\s*:", line):
            issues.append(f"Line {i}: Bare except clause")
        if "TODO" in line or "FIXME" in line:
            issues.append(f"Line {i}: {line.strip()}")
    
    if not issues:
        return "✓ No issues found! Code looks clean."
    
    save_manifest("codehelper_lint", code[:50])
    return "\n".join(issues[:10])


def analyze_code(code: str) -> str:
    """Analyze code structure."""
    analysis = {
        "lines": len(code.split("\n")),
        "functions": len(re.findall(r"def\s+\w+", code)),
        "classes": len(re.findall(r"class\s+\w+", code)),
        "imports": len(re.findall(r"^import |^from ", code, re.MULTILINE)),
        "comments": len(re.findall(r"#", code)),
    }
    
    result = ["📊 Code Analysis:"]
    for key, val in analysis.items():
        result.append(f"  {key.capitalize()}: {val}")
    
    save_manifest("codehelper_analyze", code[:50])
    return "\n".join(result)


def suggest_improvements(code: str) -> str:
    """Suggest code improvements."""
    suggestions: List[str] = []
    
    if "def " in code and "->" not in code:
        suggestions.append("• Add type hints to functions")
    if "def " in code and '"""' not in code:
        suggestions.append("• Add docstrings to functions")
    if re.search(r"\b[0-9]{2,}\b", code):
        suggestions.append("• Replace magic numbers with constants")
    if re.search(r"\b[x|y|z|a|b|c]\s*=", code):
        suggestions.append("• Use descriptive variable names")
    
    if not suggestions:
        suggestions.append("✓ Code looks well-structured!")
    
    save_manifest("codehelper_suggest", code[:50])
    return "\n".join(suggestions[:8])

# ============================================================================
# GUI APPLICATION
# ============================================================================

class UnifiedAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ACA Unified Application v4.2")
        self.root.geometry("1200x800")
        
        # Create main layout
        self.create_menu()
        self.create_main_layout()
        
    def create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Lab 1", command=lambda: self.open_path(LAB1_DIR))
        file_menu.add_command(label="Open Lab 2", command=lambda: self.open_path(LAB2_DIR))
        file_menu.add_command(label="Open Lab 3", command=lambda: self.open_path(LAB3_DIR))
        file_menu.add_separator()
        file_menu.add_command(label="📚 Deep Learning Roadmap", command=lambda: self.open_path(ROADMAP_PATH))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Labs", menu=file_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Open VS Code", command=self.open_vscode)
        tools_menu.add_command(label="Launch Jupyter Lab", command=self.launch_jupyter)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_main_layout(self):
        """Create main application layout."""
        # Left panel - Output
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel - Controls
        right_frame = tk.Frame(self.root, width=400, bg="#f0f0f0")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Output console (now on left)
        tk.Label(left_frame, text="Output Console", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.output_text = scrolledtext.ScrolledText(left_frame, height=25, width=80, 
                                                      bg="#1e1e1e", fg="#00ff00",
                                                      font=("Consolas", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Code Editor (now on right)
        tk.Label(right_frame, text="Code Editor", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=5)
        
        self.code_text = scrolledtext.ScrolledText(right_frame, height=30, width=60,
                                                    font=("Consolas", 11),
                                                    wrap=tk.NONE)
        self.code_text.pack(padx=5, pady=5)
        
        # Add helpful placeholder text
        placeholder = "# Welcome! Write your Python code here...\n# Or choose a template from the dropdown below!\n# Press Ctrl+Enter to run your code\n"
        self.code_text.insert("1.0", placeholder)
        
        # Keyboard shortcuts for code editor
        self.code_text.bind('<Control-Return>', lambda e: self.execute_code())
        self.code_text.bind('<Control-l>', lambda e: self.clear_output())
        self.code_text.bind('<Tab>', self.insert_tab)
        
        # Template selector
        tk.Label(right_frame, text="Templates:", bg="#f0f0f0").pack(pady=2)
        template_frame = tk.Frame(right_frame, bg="#f0f0f0")
        template_frame.pack(pady=5)
        
        # Template category selector
        self.template_category = tk.StringVar(value="Python Course")
        category_dropdown = ttk.Combobox(template_frame, textvariable=self.template_category,
                                        values=["Python Course", "Beginner", "Basic", "Python Library", "Course Labs", "DL Roadmap"], width=18)
        category_dropdown.pack(side=tk.LEFT, padx=2)
        category_dropdown.bind("<<ComboboxSelected>>", self.update_template_list)
        
        self.template_var = tk.StringVar(value="Hello World")
        self.template_dropdown = ttk.Combobox(template_frame, textvariable=self.template_var, 
                                         values=list(CODE_TEMPLATES.keys()), width=25)
        self.template_dropdown.pack(side=tk.LEFT, padx=2)
        tk.Button(template_frame, text="Load", command=self.load_template).pack(side=tk.LEFT, padx=2)
        
        # Action buttons
        tk.Label(right_frame, text="Actions:", bg="#f0f0f0").pack(pady=5)
        
        btn_frame = tk.Frame(right_frame, bg="#f0f0f0")
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="▶ Execute Code", command=self.execute_code, 
                 bg="#4CAF50", fg="white", width=15).pack(pady=2)
        tk.Button(btn_frame, text="🔍 Lint Code", command=self.lint_code, width=15).pack(pady=2)
        tk.Button(btn_frame, text="📊 Analyze Code", command=self.analyze_code, width=15).pack(pady=2)
        tk.Button(btn_frame, text="💡 Suggestions", command=self.suggest_improvements, width=15).pack(pady=2)
        tk.Button(btn_frame, text="📝 Explain Code", command=self.explain_code, width=15).pack(pady=2)
        tk.Button(btn_frame, text="🗑 Clear Output", command=self.clear_output, width=15).pack(pady=2)
        tk.Button(btn_frame, text="📚 DL Roadmap", command=self.open_roadmap, 
                 bg="#2196F3", fg="white", width=15).pack(pady=2)
        
        # Welcome message for beginners
        self.log_output("🎓 ACA UNIFIED APPLICATION - Learn Python & AI!")
        self.log_output("═" * 60)
        self.log_output("")
        self.log_output("� FULL PYTHON COURSE NOW AVAILABLE!")
        self.log_output("  Select 'Python Course' from dropdown to start learning")
        self.log_output("  14 comprehensive lessons from basics to advanced")
        self.log_output("")
        self.log_output("👋 GETTING STARTED (Easy as 1-2-3!):")
        self.log_output("  1️⃣  Choose 'Python Course' or 'Beginner' from dropdown")
        self.log_output("  2️⃣  Pick a lesson like 'Lesson 1: Welcome to Python'")
        self.log_output("  3️⃣  Click 'Load' then click '▶ Execute Code'")
        self.log_output("")
        self.log_output("⌨️  KEYBOARD SHORTCUTS:")
        self.log_output("  • Ctrl+Enter = Run your code")
        self.log_output("  • Ctrl+L = Clear output")
        self.log_output("  • Tab = Indent (4 spaces)")
        self.log_output("")
        self.log_output("💡 LEARNING PATHS:")
        self.log_output("  📘 Python Course → Complete step-by-step Python course")
        self.log_output("  🔰 Beginner → Quick examples for absolute beginners")
        self.log_output("  📚 Python Library → Comprehensive Python reference")
        self.log_output("  🎯 Course Labs → Hands-on projects")
        self.log_output("  🤖 DL Roadmap → Deep Learning & AI examples")
        self.log_output("")
        self.log_output(f"📁 Sandbox Directory: {SANDBOX_DIR}")
        self.log_output("═" * 60 + "\n")
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready | Lines: 0 | Chars: 0", 
                                   bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                   bg="#e0e0e0", font=("Arial", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Update status on keypress
        self.code_text.bind('<KeyRelease>', self.update_status)
    
    def log_output(self, text: str):
        """Write to output console."""
        self.output_text.insert(tk.END, f"{text}\n")
        self.output_text.see(tk.END)
        self.output_text.update()
    
    def clear_output(self):
        """Clear output console."""
        self.output_text.delete("1.0", tk.END)
        self.log_output("Output cleared.\n")
    
    def insert_tab(self, event):
        """Insert 4 spaces instead of tab."""
        self.code_text.insert(tk.INSERT, "    ")
        return 'break'
    
    def update_status(self, event=None):
        """Update status bar with line and character count."""
        content = self.code_text.get("1.0", tk.END)
        lines = content.count('\n')
        chars = len(content) - 1  # Exclude final newline
        self.status_bar.config(text=f"Ready | Lines: {lines} | Chars: {chars}")
    
    def update_template_list(self, event=None):
        """Update template dropdown based on selected category."""
        category = self.template_category.get()
        if category == "Python Course":
            templates = list(PYTHON_COURSE.keys())
        elif category == "Beginner":
            templates = list(BEGINNER_EXAMPLES.keys())
        elif category == "Python Library":
            templates = list(PYTHON_EXAMPLES.keys())
        elif category == "Course Labs":
            templates = list(COURSE_LABS.keys())
        elif category == "DL Roadmap":
            templates = list(ROADMAP_EXAMPLES.keys())
        else:
            templates = list(CODE_TEMPLATES.keys())
        
        self.template_dropdown['values'] = templates
        if templates:
            self.template_var.set(templates[0])
            # Auto-load the first template when category changes
            self.load_template()
    
    def load_template(self):
        """Load selected template into code editor."""
        template_name = self.template_var.get()
        category = self.template_category.get()
        
        # Clear editor first
        self.code_text.delete("1.0", tk.END)
        
        # Load based on category
        if category == "Python Course":
            if template_name in PYTHON_COURSE:
                self.code_text.insert("1.0", PYTHON_COURSE[template_name])
                self.log_output(f"📚 Loaded: {template_name}\n")
                self.log_output(f"💡 Read the lesson comments, then run the code to see it in action!\n")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
        elif category == "Beginner":
            if template_name in BEGINNER_EXAMPLES:
                self.code_text.insert("1.0", BEGINNER_EXAMPLES[template_name])
                self.log_output(f"✅ Loaded: {template_name}\n")
                self.log_output(f"💡 Tip: Click '▶ Execute Code' or press Ctrl+Enter to run!\n")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
        elif category == "DL Roadmap":
            if template_name in ROADMAP_EXAMPLES:
                self.code_text.insert("1.0", ROADMAP_EXAMPLES[template_name])
                self.log_output(f"✓ Loaded Roadmap: {template_name}\n")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
        elif category == "Python Library":
            if template_name in PYTHON_EXAMPLES:
                self.code_text.insert("1.0", PYTHON_EXAMPLES[template_name])
                self.log_output(f"✓ Loaded Python: {template_name}\n")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
        elif category == "Course Labs":
            if template_name in COURSE_LABS:
                self.code_text.insert("1.0", COURSE_LABS[template_name])
                self.log_output(f"✓ Loaded Lab: {template_name}\n")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
        else:  # Basic category
            if template_name in CODE_TEMPLATES:
                self.code_text.insert("1.0", CODE_TEMPLATES[template_name])
                self.log_output(f"✓ Loaded: {template_name}\n")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
    
    def execute_code(self):
        """Execute code from editor."""
        code = self.code_text.get("1.0", tk.END).strip()
        if not code:
            self.log_output("❌ No code to execute\n")
            return
        
        self.log_output(f"\n▶ Running your code...\n")
        self.log_output("─" * 50 + "\n")
        result = run_code(code, auto_confirm=True)
        self.log_output(result)
        
        # Encouraging feedback for beginners
        if "Error" not in result and "Traceback" not in result:
            self.log_output("\n🎉 Great job! Your code ran successfully!\n")
        else:
            self.log_output("\n💭 Don't worry - errors are part of learning! Try again.\n")
    
    def lint_code(self):
        """Lint code from editor."""
        code = self.code_text.get("1.0", tk.END).strip()
        if not code:
            self.log_output("❌ No code to lint")
            return
        
        self.log_output(f"\n🔍 Linting code...")
        result = lint_code(code)
        self.log_output(result)
    
    def analyze_code(self):
        """Analyze code from editor."""
        code = self.code_text.get("1.0", tk.END).strip()
        if not code:
            self.log_output("❌ No code to analyze")
            return
        
        self.log_output(f"\n📊 Analyzing code...")
        result = analyze_code(code)
        self.log_output(result)
    
    def suggest_improvements(self):
        """Suggest improvements for code."""
        code = self.code_text.get("1.0", tk.END).strip()
        if not code:
            self.log_output("❌ No code to analyze")
            return
        
        self.log_output(f"\n💡 Suggesting improvements...")
        result = suggest_improvements(code)
        self.log_output(result)
    
    def explain_code(self):
        """Explain code from editor."""
        code = self.code_text.get("1.0", tk.END).strip()
        if not code:
            self.log_output("❌ No code to explain")
            return
        
        self.log_output(f"\n📝 Explaining code...")
        result = explain_code(code)
        self.log_output(result)
    
    def open_path(self, path: str):
        """Open file or folder."""
        if not os.path.exists(path):
            self.log_output(f"❌ Path not found: {path}")
            return
        try:
            os.startfile(path)
            self.log_output(f"✓ Opened: {os.path.basename(path)}")
        except Exception as e:
            self.log_output(f"❌ Error: {e}")
    
    def open_vscode(self):
        """Launch VS Code."""
        try:
            self.log_output("▶ Launching VS Code...")
            os.system(f'code "{BASE_DIR}"')
        except Exception as e:
            self.log_output(f"❌ VS Code error: {e}")
    
    def launch_jupyter(self):
        """Launch Jupyter Lab."""
        try:
            self.log_output("▶ Starting Jupyter Lab...")
            subprocess.Popen([sys.executable, "-m", "jupyter", "lab"], shell=False)
        except Exception as e:
            self.log_output(f"❌ Jupyter error: {e}")
    
    def open_roadmap(self):
        """Open the Deep Learning Roadmap notebook."""
        if os.path.exists(ROADMAP_PATH):
            self.log_output("📚 Opening Deep Learning Roadmap notebook...")
            self.log_output("   The notebook has all 6 phases with interactive content")
            self.log_output("   You can also run examples directly in this app!")
            self.log_output("   → Change template category to 'DL Roadmap'")
            self.log_output("   → Choose from all phases (1-6) in the dropdown")
            self.open_path(ROADMAP_PATH)
        else:
            self.log_output("❌ Roadmap not found!")
            messagebox.showinfo("Info", "Deep Learning Roadmap notebook not found!")
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo("About", 
            "ACA Unified Application v4.2\n\n"
            "Complete integrated platform for code execution,\n"
            "analysis, and deep learning labs.\n\n"
            "Features: GUI, CLI, Copilot, Code Helpers, Safety Controls\n"
            "Includes Deep Learning Roadmap (6-phase curriculum)")

# ============================================================================
# CLI INTERFACE
# ============================================================================

def run_cli(args):
    """Run in CLI mode."""
    if args.open:
        target_map = {
            "lab1": LAB1_DIR,
            "lab2": LAB2_DIR,
            "lab3": LAB3_DIR,
            "readme": README_PATH,
            "roadmap": ROADMAP_PATH,
        }
        path = target_map.get(args.open)
        if path and os.path.exists(path):
            os.startfile(path)
            print(f"✓ Opened: {path}")
        else:
            print(f"❌ Invalid target: {args.open}")
    
    if args.run:
        print(run_code(args.run, auto_confirm=True))
    
    if args.read:
        print(read_file(args.read))
    
    if args.explain:
        print(explain_code(args.explain))
    
    if args.lint:
        print(lint_code(args.lint))
    
    if args.analyze:
        print(analyze_code(args.analyze))
    
    if args.suggest:
        print(suggest_improvements(args.suggest))

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main(argv: list[str] | None = None):
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="UnifiedApp",
        description="ACA Unified Application - Complete integrated platform"
    )
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode (no GUI)")
    parser.add_argument("--open", choices=["lab1", "lab2", "lab3", "readme", "roadmap"], help="Open folder/file")
    parser.add_argument("--run", help="Run code snippet")
    parser.add_argument("--read", help="Read file")
    parser.add_argument("--explain", help="Explain code")
    parser.add_argument("--lint", help="Lint code")
    parser.add_argument("--analyze", help="Analyze code")
    parser.add_argument("--suggest", help="Get suggestions")
    
    args = parser.parse_args(argv)
    
    if args.cli or any([args.open, args.run, args.read, args.explain, args.lint, args.analyze, args.suggest]):
        # CLI mode
        run_cli(args)
    else:
        # GUI mode
        root = tk.Tk()
        app = UnifiedAppGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()

from flask import Flask, render_template, request, jsonify, session
from flask_wtf.csrf import CSRFProtect
import sys
from io import StringIO
import contextlib
import traceback
import secrets
from progress import mark_complete, get_completed, get_progress, is_complete, get_all_progress

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Generate secure secret key
csrf = CSRFProtect(app)

# Comprehensive Learning Paths - Integrated from UnifiedApp_Modern.py
LEARNING_PATHS = {
    'fundamentals': {
        'id': 'fundamentals',
        'title': 'Python Fundamentals',
        'icon': '🐍',
        'description': 'Master the core concepts of Python programming',
        'duration': '2 hours',
        'lessons': [
            {
                'id': 'hello_world',
                'title': 'Hello World & Print Statements',
                'description': 'Your first steps in Python - learn to display output',
                'code': '''# Welcome to Python!
# Print is how we display information

print("Hello, World!")
print("My name is Python")
print("I love learning programming!")

# Try printing your name below:
''',
                'hints': [
                    'Use quotes (single or double) around text',
                    'Each print() creates a new line',
                    'You can print numbers without quotes'
                ]
            },
            {
                'id': 'variables',
                'title': 'Variables & Data Types',
                'description': 'Store and manipulate data with variables',
                'code': '''# Variables store information
name = "Alice"
age = 25
height = 5.6
is_student = True

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height} feet")
print(f"Student: {is_student}")

# Create your own variables below:
''',
                'hints': [
                    'Variable names should be descriptive',
                    'Use = to assign values',
                    'f-strings help format output nicely'
                ]
            },
            {
                'id': 'operators',
                'title': 'Math Operations & Operators',
                'description': 'Perform calculations and comparisons',
                'code': '''# Basic math operations
x = 10
y = 3

print(f"Addition: {x + y}")
print(f"Subtraction: {x - y}")
print(f"Multiplication: {x * y}")
print(f"Division: {x / y}")
print(f"Integer Division: {x // y}")
print(f"Remainder: {x % y}")
print(f"Power: {x ** y}")

# Try your own calculations:
''',
                'hints': [
                    '+ - * / are basic operators',
                    '// gives whole number division',
                    '% gives the remainder',
                    '** is for exponents'
                ]
            },
            {
                'id': 'strings',
                'title': 'Working with Strings',
                'description': 'Master text manipulation and string methods',
                'code': '''# Strings are text data
message = "Python is awesome!"

print(message.upper())
print(message.lower())
print(message.replace("awesome", "amazing"))
print(len(message))
print(message.split())

# String concatenation
first = "Hello"
last = "World"
print(first + " " + last)

# Try string operations:
''',
                'hints': [
                    '.upper() makes all uppercase',
                    '.lower() makes all lowercase',
                    'len() gets the length',
                    '.split() breaks into words'
                ]
            },
            {
                'id': 'lists',
                'title': 'Lists & Collections',
                'description': 'Store multiple items in ordered collections',
                'code': '''# Lists hold multiple items
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]

print(fruits[0])  # First item
print(fruits[-1])  # Last item
fruits.append("grape")
print(fruits)

# List operations
print(len(numbers))
print(sum(numbers))
print(max(numbers))

# Create your own list:
''',
                'hints': [
                    'Lists use square brackets []',
                    'Indexing starts at 0',
                    'Negative indices count from the end',
                    '.append() adds items'
                ]
            }
        ]
    },
    'control_flow': {
        'id': 'control_flow',
        'title': 'Control Flow',
        'icon': '🔀',
        'description': 'Make decisions and create loops',
        'duration': '1.5 hours',
        'lessons': [
            {
                'id': 'if_statements',
                'title': 'If Statements & Conditions',
                'description': 'Make your code make decisions',
                'code': '''# If statements control program flow
age = 18

if age >= 18:
    print("You are an adult")
elif age >= 13:
    print("You are a teenager")
else:
    print("You are a child")

# Multiple conditions
temperature = 75
if temperature > 80:
    print("It's hot!")
elif temperature > 60:
    print("It's nice!")
else:
    print("It's cold!")

# Try your own conditions:
''',
                'hints': [
                    'if checks a condition',
                    'elif is "else if"',
                    'else catches everything else',
                    'Use == for equality, != for not equal'
                ]
            },
            {
                'id': 'for_loops',
                'title': 'For Loops',
                'description': 'Repeat code for each item in a sequence',
                'code': '''# For loops iterate over sequences
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I like {fruit}")

# Loop with range
for i in range(5):
    print(f"Number: {i}")

# Loop with range and step
for i in range(0, 10, 2):
    print(f"Even: {i}")

# Try your own loop:
''',
                'hints': [
                    'for loops go through each item',
                    'range(n) goes from 0 to n-1',
                    'range(start, stop, step) allows customization',
                    'Indentation matters!'
                ]
            },
            {
                'id': 'while_loops',
                'title': 'While Loops',
                'description': 'Repeat code while a condition is true',
                'code': '''# While loops continue until condition is false
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# Countdown example
number = 10
while number > 0:
    print(number)
    number -= 1
print("Blast off!")

# Try your own while loop:
''',
                'hints': [
                    'while checks condition each time',
                    'Don\'t forget to update the variable!',
                    '+= adds to a variable',
                    '-= subtracts from a variable'
                ]
            }
        ]
    },
    'functions': {
        'id': 'functions',
        'title': 'Functions',
        'icon': '⚙️',
        'description': 'Create reusable blocks of code',
        'duration': '1 hour',
        'lessons': [
            {
                'id': 'functions_basics',
                'title': 'Defining & Using Functions',
                'description': 'Create reusable code with functions',
                'code': '''# Functions organize and reuse code
def greet(name):
    """Greet someone by name"""
    return f"Hello, {name}!"

def add_numbers(a, b):
    """Add two numbers together"""
    return a + b

def calculate_area(length, width):
    """Calculate rectangle area"""
    area = length * width
    return area

# Using functions
print(greet("Alice"))
print(add_numbers(5, 3))
print(calculate_area(10, 5))

# Create your own function:
''',
                'hints': [
                    'def defines a function',
                    'Parameters go in parentheses',
                    'return sends back a value',
                    'Call functions with their name()'
                ]
            }
        ]
    },
    'advanced': {
        'id': 'advanced',
        'title': 'Advanced Topics',
        'icon': '🚀',
        'description': 'Level up with advanced Python concepts',
        'duration': '2.5 hours',
        'lessons': [
            {
                'id': 'dictionaries',
                'title': 'Dictionaries & Key-Value Pairs',
                'description': 'Store data with meaningful keys',
                'code': '''# Dictionaries use key-value pairs
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "hobbies": ["reading", "coding"]
}

print(person["name"])
print(person["age"])

# Adding new items
person["job"] = "Developer"
print(person)

# Looping through dictionary
for key, value in person.items():
    print(f"{key}: {value}")

# Try your own dictionary:
''',
                'hints': [
                    'Dictionaries use curly braces {}',
                    'Keys can be strings or numbers',
                    'Access values with dict[key]',
                    '.items() gives key-value pairs'
                ]
            },
            {
                'id': 'file_handling',
                'title': 'Reading & Writing Files',
                'description': 'Work with external files',
                'code': '''# Writing to a file
with open("example.txt", "w") as file:
    file.write("Hello from Python!\\n")
    file.write("This is line 2\\n")
    file.write("This is line 3\\n")

# Reading from a file
with open("example.txt", "r") as file:
    content = file.read()
    print(content)

# Reading line by line
with open("example.txt", "r") as file:
    for line in file:
        print(f"Line: {line.strip()}")

# Try file operations:
''',
                'hints': [
                    '"w" means write mode',
                    '"r" means read mode',
                    'with ensures file closes properly',
                    '.strip() removes whitespace'
                ]
            },
            {
                'id': 'classes_oop',
                'title': 'Classes & Object-Oriented Programming',
                'description': 'Create custom objects with classes',
                'code': '''# Classes define blueprints for objects
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.age = 0
    
    def bark(self):
        return f"{self.name} says Woof!"
    
    def birthday(self):
        self.age += 1
        return f"{self.name} is now {self.age} years old!"

# Creating objects
my_dog = Dog("Buddy", "Golden Retriever")
print(my_dog.bark())
print(my_dog.birthday())
print(my_dog.birthday())

# Try creating your own class:
''',
                'hints': [
                    '__init__ is the constructor',
                    'self refers to the instance',
                    'Methods are functions inside classes',
                    'Create objects with ClassName()'
                ]
            }
        ]
    }
}

@app.route('/')
def index():
    """Main landing page with all learning paths"""
    # Add progress data for each path
    paths_with_progress = {}
    for path_id, path in LEARNING_PATHS.items():
        paths_with_progress[path_id] = path.copy()
        paths_with_progress[path_id]['progress'] = get_progress(path_id, len(path['lessons']))
    return render_template('unified_index.html', learning_paths=paths_with_progress)

@app.route('/path/<path_id>')
def learning_path(path_id):
    """Display all lessons in a learning path"""
    path = LEARNING_PATHS.get(path_id)
    if path:
        completed = get_completed(path_id)
        progress = get_progress(path_id, len(path['lessons']))
        return render_template('learning_path.html', path=path, completed=completed, progress=progress)
    return "Path not found", 404

@app.route('/lesson/<path_id>/<lesson_id>')
def lesson_view(path_id, lesson_id):
    """Interactive lesson workspace"""
    path = LEARNING_PATHS.get(path_id)
    if path:
        lesson = next((l for l in path['lessons'] if l['id'] == lesson_id), None)
        if lesson:
            is_completed = is_complete(path_id, lesson_id)
            return render_template('lesson_view.html', path=path, lesson=lesson, is_completed=is_completed)
    return "Lesson not found", 404

@app.route('/execute', methods=['POST'])
@csrf.exempt  # Exempt this endpoint from CSRF for API testing
def execute_code():
    """Execute Python code safely and return output"""
    try:
        code = request.json.get('code', '')
        
        # Validate code length
        if len(code) > 10000:
            return jsonify({'success': False, 'output': 'Error: Code too long (max 10000 characters)'})
        
        # Create a string buffer to capture output
        output_buffer = StringIO()
        
        # Create restricted globals with safe builtins
        safe_globals = {
            '__builtins__': {
                'print': print,
                'range': range,
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'abs': abs,
                'max': max,
                'min': min,
                'sum': sum,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
            }
        }
        
        # Redirect stdout to capture print statements
        with contextlib.redirect_stdout(output_buffer):
            # Execute the code with restricted globals
            exec(code, safe_globals, {})
        
        output = output_buffer.getvalue()
        return jsonify({'success': True, 'output': output or 'Code executed successfully'})
    
    except Exception as e:
        error_output = traceback.format_exc()
        return jsonify({'success': False, 'output': error_output})
    
    finally:
        if 'output_buffer' in locals():
            output_buffer.close()

@app.route('/playground')
def playground():
    """Free-form code playground"""
    return render_template('playground.html')

@app.route('/mark-complete/<path_id>/<lesson_id>', methods=['POST'])
@csrf.exempt
def mark_lesson_complete(path_id, lesson_id):
    """Mark a lesson as complete and return updated progress"""
    try:
        mark_complete(path_id, lesson_id)
        path = LEARNING_PATHS.get(path_id)
        if path:
            progress = get_progress(path_id, len(path['lessons']))
            return jsonify({'success': True, 'progress': progress})
        return jsonify({'success': False, 'message': 'Path not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/diagnostic')
def diagnostic():
    """Client-side diagnostic page"""
    return render_template('diagnostic.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

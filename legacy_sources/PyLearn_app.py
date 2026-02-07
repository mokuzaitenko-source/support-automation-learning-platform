from flask import Flask, render_template, request, jsonify
import sys
from io import StringIO
import contextlib
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'python-learning-platform-2026'

# ================================================
# COMPREHENSIVE LESSON CONTENT
# ================================================

LEARNING_PATHS = {
    "fundamentals": {
        "name": "🎯 Python Fundamentals",
        "description": "Master the basics - perfect for beginners",
        "icon": "🎯",
        "lessons": [
            {
                "id": "hello_world",
                "title": "Hello World & Print",
                "description": "Your first Python program",
                "code": '''# Lesson 1: Hello World & Print Function
# ==========================================
# The print() function displays output to the console

# Simple print
print("Hello, World!")

# Print multiple items
print("Learning", "Python", "is", "fun!")

# Print with f-strings (formatted strings)
name = "Learner"
age = 25
print(f"Hello {name}! You are {age} years old.")

# Practice: Print your own introduction!
''',
                "hints": ["Use quotes for text", "f-strings make formatting easy", "Practice makes perfect!"]
            },
            {
                "id": "variables",
                "title": "Variables & Data Types",
                "description": "Store and work with data",
                "code": '''# Lesson 2: Variables & Data Types
# ==========================================

# Numbers
age = 25
height = 5.9
temperature = -10

# Strings (text)
name = "Python Learner"
message = 'Learning is fun!'

# Booleans (True/False)
is_learning = True
is_expert = False

# Check data types
print(f"age is {type(age)}")
print(f"name is {type(name)}")
print(f"is_learning is {type(is_learning)}")

# Variables can change
score = 0
print(f"Starting score: {score}")
score = 100
print(f"New score: {score}")

# Practice: Create variables for your favorite things!
''',
                "hints": ["Variables store data", "Use meaningful names", "Types: int, float, str, bool"]
            },
            {
                "id": "operators",
                "title": "Math & Operators",
                "description": "Perform calculations",
                "code": '''# Lesson 3: Math & Operators
# ==========================================

# Basic arithmetic
print("Addition:", 5 + 3)
print("Subtraction:", 10 - 4)
print("Multiplication:", 6 * 7)
print("Division:", 15 / 3)
print("Floor Division:", 17 // 5)  # Whole number
print("Modulo (remainder):", 17 % 5)
print("Power:", 2 ** 3)  # 2 cubed

# Comparison operators
x = 10
y = 5
print(f"{x} > {y}:", x > y)
print(f"{x} == {y}:", x == y)
print(f"{x} != {y}:", x != y)

# Practice: Calculate your age in days!
age_years = 25
days = age_years * 365
print(f"{age_years} years = {days} days")
''',
                "hints": ["Math in Python is intuitive", "Use ** for powers", "Try different operations"]
            },
            {
                "id": "strings",
                "title": "Working with Strings",
                "description": "Master text manipulation",
                "code": '''# Lesson 4: Working with Strings
# ==========================================

# String basics
message = "Python is Amazing!"

# String methods
print("Original:", message)
print("Uppercase:", message.upper())
print("Lowercase:", message.lower())
print("Title Case:", message.title())

# String operations
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print("Full name:", full_name)

# String formatting
age = 25
intro = f"My name is {full_name} and I'm {age} years old."
print(intro)

# String slicing
word = "Python"
print("First letter:", word[0])
print("Last letter:", word[-1])
print("First 3 letters:", word[0:3])

# Practice: Create a story with your variables!
''',
                "hints": ["Strings are immutable", "Use f-strings for formatting", "Slice with [start:end]"]
            },
            {
                "id": "lists",
                "title": "Lists & Collections",
                "description": "Store multiple values",
                "code": '''# Lesson 5: Lists & Collections
# ==========================================

# Create a list
fruits = ["apple", "banana", "orange", "grape"]
print("Fruits:", fruits)

# Access items
print("First fruit:", fruits[0])
print("Last fruit:", fruits[-1])

# Modify lists
fruits.append("mango")  # Add to end
print("After append:", fruits)

fruits.insert(1, "kiwi")  # Insert at position
print("After insert:", fruits)

fruits.remove("banana")  # Remove item
print("After remove:", fruits)

# List operations
numbers = [1, 2, 3, 4, 5]
print("Sum:", sum(numbers))
print("Length:", len(numbers))
print("Max:", max(numbers))

# Practice: Create a list of your hobbies!
hobbies = ["coding", "reading", "gaming"]
print(f"I have {len(hobbies)} hobbies: {', '.join(hobbies)}")
''',
                "hints": ["Lists are mutable", "Index starts at 0", "Use -1 for last item"]
            }
        ]
    },
    "control_flow": {
        "name": "🔀 Control Flow",
        "description": "Make decisions and repeat actions",
        "icon": "🔀",
        "lessons": [
            {
                "id": "if_statements",
                "title": "If Statements",
                "description": "Make decisions in code",
                "code": '''# Lesson 6: If Statements
# ==========================================

# Basic if statement
age = 18
if age >= 18:
    print("You are an adult!")

# If-else
temperature = 75
if temperature > 80:
    print("It's hot!")
else:
    print("It's comfortable!")

# If-elif-else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
print(f"Score: {score}, Grade: {grade}")

# Multiple conditions
is_weekend = True
is_sunny = True
if is_weekend and is_sunny:
    print("Perfect day for a picnic!")

# Practice: Create a simple quiz!
answer = "python"
guess = input("What language are we learning? ").lower()
if guess == answer:
    print("Correct! 🎉")
else:
    print("Try again!")
''',
                "hints": ["Indentation matters!", "Use elif for multiple conditions", "and/or for combining conditions"]
            },
            {
                "id": "for_loops",
                "title": "For Loops",
                "description": "Repeat actions efficiently",
                "code": '''# Lesson 7: For Loops
# ==========================================

# Loop through a list
fruits = ["apple", "banana", "orange"]
print("Fruit list:")
for fruit in fruits:
    print(f"  - {fruit}")

# Loop with range
print("\\nNumbers 1 to 5:")
for i in range(1, 6):
    print(i, end=" ")

# Loop with index
colors = ["red", "green", "blue"]
print("\\n\\nColored list:")
for index, color in enumerate(colors, 1):
    print(f"{index}. {color}")

# Nested loops (pattern)
print("\\nTriangle pattern:")
for i in range(1, 6):
    print("*" * i)

# List comprehension (advanced)
squares = [x**2 for x in range(1, 6)]
print(f"\\nSquares: {squares}")

# Practice: Print your name 5 times!
name = "Learner"
for i in range(5):
    print(f"{i+1}. Hello {name}!")
''',
                "hints": ["for x in list: iterates items", "range(n) creates numbers", "enumerate() gives index+value"]
            },
            {
                "id": "while_loops",
                "title": "While Loops",
                "description": "Loop until condition is false",
                "code": '''# Lesson 8: While Loops
# ==========================================

# Basic while loop
count = 1
print("Counting to 5:")
while count <= 5:
    print(count, end=" ")
    count += 1

# While with break
print("\\n\\nGuessing game:")
secret_number = 7
attempts = 0
while True:
    attempts += 1
    if attempts > 3:  # Limit attempts for demo
        print("\\nToo many tries!")
        break
    guess = int(input(f"Attempt {attempts} - Guess (1-10): "))
    if guess == secret_number:
        print(f"Correct! You got it in {attempts} tries!")
        break
    elif guess < secret_number:
        print("Too low!")
    else:
        print("Too high!")

# While with continue
print("\\nEven numbers only:")
num = 0
while num < 10:
    num += 1
    if num % 2 != 0:  # Skip odd numbers
        continue
    print(num, end=" ")

# Practice: Countdown!
countdown = 5
while countdown > 0:
    print(f"\\n{countdown}...")
    countdown -= 1
print("Blast off! 🚀")
''',
                "hints": ["while condition: keeps looping", "break exits loop", "continue skips to next iteration"]
            }
        ]
    },
    "functions": {
        "name": "🔧 Functions & Modules",
        "description": "Organize and reuse code",
        "icon": "🔧",
        "lessons": [
            {
                "id": "functions_basics",
                "title": "Function Basics",
                "description": "Create reusable code blocks",
                "code": '''# Lesson 9: Function Basics
# ==========================================

# Simple function
def greet():
    print("Hello, World!")

greet()  # Call the function

# Function with parameters
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")
greet_person("Bob")

# Function with return value
def add_numbers(a, b):
    result = a + b
    return result

sum_result = add_numbers(5, 3)
print(f"5 + 3 = {sum_result}")

# Default parameters
def greet_with_title(name, title="Friend"):
    print(f"Hello, {title} {name}!")

greet_with_title("Alice")
greet_with_title("Bob", "Dr.")

# Multiple return values
def get_stats(numbers):
    total = sum(numbers)
    avg = total / len(numbers)
    return total, avg

total, average = get_stats([1, 2, 3, 4, 5])
print(f"Total: {total}, Average: {average}")

# Practice: Create a calculator function!
def calculator(num1, num2, operation):
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        return num1 / num2
    else:
        return "Invalid operation"

print(calculator(10, 5, "+"))
print(calculator(10, 5, "*"))
''',
                "hints": ["def keyword defines functions", "Use return to send back values", "Parameters make functions flexible"]
            }
        ]
    },
    "advanced": {
        "name": "🚀 Advanced Topics",
        "description": "Level up your skills",
        "icon": "🚀",
        "lessons": [
            {
                "id": "dictionaries",
                "title": "Dictionaries",
                "description": "Key-value data structures",
                "code": '''# Lesson 10: Dictionaries
# ==========================================

# Create a dictionary
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York",
    "hobbies": ["coding", "reading", "gaming"]
}

# Access values
print("Name:", person["name"])
print("Age:", person["age"])

# Safe access with get()
print("Country:", person.get("country", "Not specified"))

# Modify dictionary
person["age"] = 26
person["job"] = "Developer"
print("\\nUpdated person:", person)

# Loop through dictionary
print("\\nPerson details:")
for key, value in person.items():
    print(f"  {key}: {value}")

# Nested dictionary
students = {
    "student1": {"name": "Alice", "grade": 90},
    "student2": {"name": "Bob", "grade": 85}
}

print("\\nStudent grades:")
for student_id, info in students.items():
    print(f"{info['name']}: {info['grade']}")

# Practice: Create a phonebook!
phonebook = {
    "Alice": "555-1234",
    "Bob": "555-5678",
    "Charlie": "555-9012"
}

name = "Alice"
print(f"\\n{name}'s number: {phonebook[name]}")
''',
                "hints": ["Dictionaries use key:value pairs", "Keys must be unique", "Use get() to avoid errors"]
            },
            {
                "id": "file_handling",
                "title": "Working with Files",
                "description": "Read and write files",
                "code": '''# Lesson 11: Working with Files
# ==========================================

# Write to a file
filename = "my_notes.txt"

# Writing mode
with open(filename, 'w') as file:
    file.write("Python is awesome!\\n")
    file.write("I love learning!\\n")
    file.write("Keep practicing!\\n")

print(f"✓ Created {filename}")

# Append to file
with open(filename, 'a') as file:
    file.write("This line was added later!\\n")

print(f"✓ Added to {filename}")

# Read from file
print(f"\\nReading {filename}:")
with open(filename, 'r') as file:
    content = file.read()
    print(content)

# Read line by line
print("Reading line by line:")
with open(filename, 'r') as file:
    for line_num, line in enumerate(file, 1):
        print(f"Line {line_num}: {line.strip()}")

# Read into list
with open(filename, 'r') as file:
    lines = file.readlines()
    print(f"\\nTotal lines: {len(lines)}")

# Practice: Create a todo list!
todos = ["Learn Python", "Build projects", "Practice daily"]

with open("todo.txt", 'w') as file:
    for i, todo in enumerate(todos, 1):
        file.write(f"{i}. {todo}\\n")

print("\\n✓ Todo list created!")
''',
                "hints": ["'w' = write, 'r' = read, 'a' = append", "Use 'with' for automatic closing", "Always close files"]
            },
            {
                "id": "classes_oop",
                "title": "Classes & OOP",
                "description": "Object-Oriented Programming",
                "code": '''# Lesson 12: Classes & Object-Oriented Programming
# ==========================================

# Define a class
class Dog:
    # Constructor
    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age
    
    # Method
    def bark(self):
        return f"{self.name} says Woof!"
    
    def info(self):
        return f"{self.name} is a {self.age} year old {self.breed}"

# Create objects
dog1 = Dog("Buddy", "Golden Retriever", 3)
dog2 = Dog("Max", "German Shepherd", 5)

print(dog1.bark())
print(dog2.bark())
print(dog1.info())
print(dog2.info())

# Inheritance
class Puppy(Dog):
    def __init__(self, name, breed):
        super().__init__(name, breed, age=0)
    
    def bark(self):
        return f"{self.name} says Yip yip!"

puppy = Puppy("Tiny", "Poodle")
print(f"\\n{puppy.bark()}")
print(puppy.info())

# Practice: Create a Student class!
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def study(self, subject):
        return f"{self.name} is studying {subject}"
    
    def get_status(self):
        if self.grade >= 90:
            return "Excellent!"
        elif self.grade >= 70:
            return "Good job!"
        else:
            return "Keep practicing!"

student = Student("Alice", 95)
print(f"\\n{student.study('Python')}")
print(f"Status: {student.get_status()}")
''',
                "hints": ["Classes are blueprints for objects", "__init__ is the constructor", "self refers to the instance"]
            }
        ]
    }
}

@app.route('/')
def index():
    # Legacy template expects path.progress metadata on each learning path.
    enriched_paths = {}
    for path_id, path in LEARNING_PATHS.items():
        total = len(path.get("lessons", []))
        progress = {"completed": 0, "total": total, "percentage": 0}
        enriched = dict(path)
        enriched["progress"] = progress
        enriched_paths[path_id] = enriched
    return render_template('unified_index.html', learning_paths=enriched_paths)

@app.route('/path/<path_id>')
def learning_path(path_id):
    path = LEARNING_PATHS.get(path_id)
    if path:
        total = len(path.get("lessons", []))
        progress = {"completed": 0, "total": total, "percentage": 0}
        return render_template('learning_path.html', path=path, path_id=path_id, progress=progress)
    return "Path not found", 404

@app.route('/lesson/<path_id>/<lesson_id>')
def lesson(path_id, lesson_id):
    path = LEARNING_PATHS.get(path_id)
    if not path:
        return "Path not found", 404
    
    lesson_data = next((l for l in path['lessons'] if l['id'] == lesson_id), None)
    if lesson_data:
        return render_template('lesson_view.html', lesson=lesson_data, path=path, path_id=path_id)
    return "Lesson not found", 404

# Compatibility alias so shared templates can call endpoint name "lesson_view"
app.add_url_rule('/lesson/<path_id>/<lesson_id>', endpoint='lesson_view', view_func=lesson)

@app.route('/execute', methods=['POST'])
def execute_code():
    """Execute Python code safely and return output"""
    code = request.json.get('code', '')
    
    output_buffer = StringIO()
    error_output = None
    
    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {'__builtins__': __builtins__})
        
        output = output_buffer.getvalue()
        return jsonify({'success': True, 'output': output})
    
    except Exception as e:
        error_output = traceback.format_exc()
        return jsonify({'success': False, 'output': error_output})
    
    finally:
        output_buffer.close()

@app.route('/playground')
def playground():
    return render_template('playground.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

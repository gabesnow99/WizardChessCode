import os

file_path = 'script.py'

def cls():
    os.system('cls')

def runp():
    cls()
    global file_path
    try:
       with open(file_path, 'r') as file:
           content = file.read()

    except FileNotFoundError:
        print(f'File "{file_path}" not found. Exiting... ')
        return

    message = ('ChatGPT does not recommend running entire scripts through the interpreter.'
               '\nDoing so bypasses security protocal, limits error handling, causes'
               '\nunpredictable timing behavior, and hampers code readability while debugging.\n')
    print(message)
    input('\nPress Enter to execute...\n\n')
    cls()

    exec(content)

def s():
    print("exec(open('script.py', encoding='utf-8').read())")

def p():
    print("exec(open('python_prototype.py', encoding='utf-8').read())")

def g():
    print("exec(open('graphics.py', encoding='utf-8').read())")

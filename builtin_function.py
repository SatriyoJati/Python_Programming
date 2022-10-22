# builthin functin
'''
len()
input()
print()
zip()
range()
enumerate()
max()
min()
upper()

from modules
math :
log2()
power()

random module
randint()
choice()
'''

#use underscores and descriptif
def name_of_func():
    #should indented

#may or maynot include paramters

#includes parameters"
def add_two_nums(num_1, num_2):
    print(num_1 + num_2)

def say_hello():
    '''
    use docstring This function prints hello world
    '''
    print("Hello World!")

#limit function to perform only 1 defined function

def get_input_from_user():
    '''
    this function has its own space
    '''
    name_result = input("Eenter your here -->")
    print(f"Your response was {name_result}")

print("Welcome to program what is your name")
get_input_from_user()

print("What did you think of the food you ate today")
get_input_from_user()

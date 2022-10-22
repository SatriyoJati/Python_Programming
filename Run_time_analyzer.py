#Runtime-analyzer
#Generate random integers
# list specifide by user at runtime
#also range integer
#Run function
# calculate and display the time it took to run the function
# allow for multiple runs


#Method
#select item

#Whwere
import demos
import random
import time

def create_random_list(size , max_val):
    ran_list = []
    for num in range(size):
        ran_list.append(random.randint(1,max_val))
    return ran_list

def analyze_func(func_name, arr):
    tic = time.time()
    func_name(arr)
    toc = time.time()
    seconds = toc - tic
    print(f"{func_name.__name__} Elapsed time -> ", seconds)

size = input("What size list do you want to create?")
max = input("What is the max value of the range?")

l = create_random_list(int(size),int(max))
#Generate pseudo-random numbers : use randint
analyze_func(demos.quicksort, l)
analyze_func(demos.mergesort, l)

from random import randint
#while loops

# break and pass keyword

# generator - zip function

truth_condition = True


l1 = [randint(1,100) for num in range(1000)]
num_to_search = 25
i  = 0
while i < len(l1):
    if l1[i] == num_to_search:
        print(f"{num_to_search} found at index {i}" )
        break #for loop as well
    i += 1

m = 0
for num in l1:
     # needed when use for because no index yielded
    if num == num_to_search:
        print(f"{num_to_search} found at index {m}")
        break
    m+=1

#zip combine lists into tuples
l1 = []

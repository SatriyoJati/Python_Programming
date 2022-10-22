#for loop and generators
from random import randint
l = [6,8,1,4,10,7,8,9,3,2,5]
my_dict = {'py': 'python','rb': 'ruby','js':'javascript'}

#sum of all ints
sum = 0
for _ in l:
    sum += _

print(f"total numbers in list{sum}")


for item in my_dict.items():
    key, value = item
    print(f"key is {key}, value is {value}")

#generate 100 random integer 1 - 100
l1 = []
for num in range(100):
    l1.append(randint(1,100))

print(l1)
